# coding=utf-8
import datetime
import six
from ..bigquery_mixin import BigQueryMixin
from .base_metadata_db import BaseMetadataDB, MetadataTypeNotSupported
from flatten_json import unflatten


# noinspection SqlNoDataSourceInspection
class BigQueryMetadataDB(BaseMetadataDB, BigQueryMixin):
    def get_all_data(self, sha):
        pass

    def get_data_for_commit(self, sha, commit_sha):
        pass

    STAGING_TABLE_NAME = 'staging'
    METADATA_TABLE_NAME = 'metadata'

    def __init__(self, connection):
        self.__staging_table = None
        self.__metadata_table = None
        self.__prev_table_info = None
        super(BigQueryMetadataDB, self).__init__(connection)

    def _create_table(self):
        from google.cloud import bigquery

        schema = (
            bigquery.SchemaField('_sha', 'STRING', 'REQUIRED'),
            bigquery.SchemaField('_commit_sha', 'STRING', 'REQUIRED'),
            bigquery.SchemaField('_ts', 'TIMESTAMP'),
        )

        self.__staging_table = self._create_specific_table(self.STAGING_TABLE_NAME, schema)
        self.__metadata_table = self._create_specific_table(self.METADATA_TABLE_NAME, schema)

    def __has_column(self, column_name):
        for field in self.__metadata_table.schema:
            if column_name == field.name:
                return True

        return False

    @classmethod
    def __value_to_sql_type(cls, column_value):
        if isinstance(column_value, six.string_types):
            return 'STRING'

        if isinstance(column_value, six.integer_types):
            return 'INTEGER'

        if isinstance(column_value, float):
            return 'FLOAT'

        raise MetadataTypeNotSupported('UNKNOWN TYPE %s' % type(column_value))

    @classmethod
    def _patch_table_with_new_schema(cls, table, schema):
        table.patch(schema=schema)

    def _add_missing_columns(self, data_object):
        from google.cloud import bigquery

        new_columns = []
        for column_name, column_value in data_object.items():
            column_name = self.common_name_to_bq_field_name(column_name)
            if self.__has_column(column_name):
                continue

            new_columns.append(bigquery.SchemaField(column_name, self.__value_to_sql_type(column_value)))

        if len(new_columns) > 0:
            schema = self.__staging_table.schema[:]
            new_columns = sorted(new_columns, key=lambda field: field.name)
            schema.extend(new_columns)
            self._patch_table_with_new_schema(self.__staging_table, schema)
            self._patch_table_with_new_schema(self.__metadata_table, schema)

    def _add_data(self, flatten_data_list):
        rows = []

        now = datetime.datetime.utcnow()

        for flatten_data_list in flatten_data_list:
            row = []
            for field in self.__staging_table.schema:
                common_field_name = self.bq_field_name_to_common_name(field.name)
                if common_field_name == '_ts':
                    row.append(now)
                else:
                    row.append(flatten_data_list[common_field_name])

            rows.append(row)

        self.handle_bq_errors(self.__staging_table.insert_data(rows))

    def __truncate_staging(self):
        schema = self.__staging_table.schema
        self.__staging_table.delete()
        self.__staging_table = self._create_specific_table(self.__staging_table.name, schema)

    def commit(self, commit_sha, tree_id):
        from google.cloud import bigquery

        with self._connection.get_cursor() as bq_dataset:
            src_query = """
                #standardSQL
                SELECT _sha, @commit_sha as _commit_sha, *  EXCEPT(_sha, _commit_sha) FROM (
                  SELECT * EXCEPT(_max_sha, _max_ts) FROM {dataset_name}.{staging_table_name}
                  INNER JOIN (
                    SELECT _sha as _max_sha, MAX(_ts) as _max_ts
                    FROM {dataset_name}.{staging_table_name}
                    GROUP BY _sha
                  ) ON _sha = _max_sha
                  WHERE _max_ts = _ts
                )
            """.format(
                dataset_name=bq_dataset.name,
                staging_table_name=self.__staging_table.name)

            src_query_parameters = (
                bigquery.ScalarQueryParameter('commit_sha', 'STRING', commit_sha),
            )

            self._copy_table_data(self.__staging_table, src_query, src_query_parameters, self.__metadata_table, tree_id)
            self.__truncate_staging()

    def _query_head_data(self, sha_list):
        from google.cloud import bigquery

        bq_client = self._connection

        with bq_client.get_cursor() as bq_dataset:
            query = """
            #standardSQL
            SELECT * EXCEPT(_max_sha, _max_ts, _ts) FROM (SELECT *
              FROM {dataset_name}.{staging_table_name} WHERE _sha IN UNNEST(@sha_list)
              UNION ALL
                SELECT * FROM {dataset_name}.{metadata_table_name} WHERE _sha IN UNNEST(@sha_list)) as metadata_staging_combine
              INNER JOIN (
                SELECT  _sha as _max_sha, MAX(_ts) as _max_ts FROM {dataset_name}.{staging_table_name} WHERE _sha IN UNNEST(@sha_list) GROUP BY _sha
                UNION ALL
                  SELECT  _sha as _max_sha, MAX(_ts) as _max_ts FROM {dataset_name}.{metadata_table_name} WHERE _sha IN UNNEST(@sha_list) GROUP BY _sha
              ) _max_metadata
            ON
              metadata_staging_combine._sha = _max_sha
            WHERE
              metadata_staging_combine._ts = _max_ts;
            """.format(
                dataset_name=bq_dataset.name,
                staging_table_name=self._get_table_name(bq_client.table_prefix, self.STAGING_TABLE_NAME),
                metadata_table_name=self._get_table_name(bq_client.table_prefix, self.METADATA_TABLE_NAME))

            query_parameters = (
                bigquery.ArrayQueryParameter('sha_list', 'STRING', sha_list),
            )

            return self._query_sync(query, query_parameters, process_row=self.build_dict)

    def _query(self, sql_vars, select_fields, where):
        bq_client = self._connection

        with bq_client.get_cursor() as bq_dataset:
            query_sql = """
                 #Legacy SQL
                 select {select}
                  from {dataset_name}.{metadata_table_name}
                 where _ts IN (
                   SELECT MAX(_ts)
                   FROM {dataset_name}.{metadata_table_name}
                   GROUP BY _sha
                 ) AND {where}
                 ORDER BY _sha
             """.format(
                dataset_name=bq_dataset.name,
                metadata_table_name=self._get_table_name(bq_client.table_prefix, self.METADATA_TABLE_NAME),
                where=where,
                select=','.join(select_fields))

            query_sql = self.fill_in_vars(query_sql, sql_vars)

            data = self._query_sync(query_sql, use_legacy_sql=True, process_row=self.build_dict)

            for result in data:
                yield unflatten(result, separator='.')
