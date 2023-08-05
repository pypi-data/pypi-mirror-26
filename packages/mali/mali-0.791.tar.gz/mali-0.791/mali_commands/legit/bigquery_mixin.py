# coding=utf-8
import json
import logging
import uuid
import os
from .connection_mixin import ConnectionMixin


class BigQueryOperationError(Exception):
    pass


class BigQueryMixin(ConnectionMixin):
    @classmethod
    def handle_bq_errors(cls, async_job_or_errors):
        logging.debug('finish job %s', async_job_or_errors)
        if isinstance(async_job_or_errors, list):
            errors = async_job_or_errors
        else:
            errors = async_job_or_errors.errors

        if not errors:
            return

        error_msg = json.dumps(errors)

        raise BigQueryOperationError(error_msg)

    def _query_async(self, query, query_parameters=(), use_legacy_sql=False):
        logging.info('query async: %s, params: %s, legacy_sql: %s', query, query_parameters, use_legacy_sql)
        query_id = str(uuid.uuid4())

        bq_client = self._connection

        query_job = bq_client.run_async_query(query_id, query, query_parameters=query_parameters)
        query_job.use_legacy_sql = use_legacy_sql

        return query_job

    def _query_sync(self, query, query_parameters=(), use_legacy_sql=False, process_row=None):
        query_job = self._query_async(query, query_parameters, use_legacy_sql=use_legacy_sql)
        query_job.begin()
        self.handle_bq_errors(query_job.result())

        destination_table = query_job.destination
        destination_table.reload()

        for result in destination_table.fetch_data():
            if not process_row:
                yield result
                continue

            yield process_row(result, query_job)

    def _copy_table(self, dest_table, src_table, write_disposition, create_disposition):
        logging.info(
            'copy %s => %s write_disposition: %s, create_disposition: %s',
            src_table.name, dest_table.name, write_disposition, create_disposition)

        copy_id = str(uuid.uuid4())

        bq_client = self._connection

        copy_job = bq_client.copy_table(copy_id, dest_table, src_table)
        copy_job.write_disposition = write_disposition
        copy_job.create_disposition = create_disposition

        return copy_job

    def _sync_copy_table(self, dest_table, src_table, write_disposition, create_disposition):
        copy_job = self._copy_table(dest_table, src_table, write_disposition, create_disposition)
        copy_job.begin()

        self.handle_bq_errors(copy_job.result())

    @classmethod
    def valid_table_name_random_token(cls, size=8):
        from base58 import b58encode

        return b58encode(os.urandom(size))

    @classmethod
    def _get_table_name(cls, prefix, name):
        table_full_name = '{prefix}_{name}'.format(prefix=prefix, name=name)

        return table_full_name

    def _get_table(self, name, schema=()):
        table_full_name = self._get_table_name(self._connection.table_prefix, name)

        with self._connection.get_cursor() as bq_dataset:
            return bq_dataset.table(table_full_name, schema=schema)

    def _create_specific_table(self, name, schema):
        import google.api.core.exceptions

        table = self._get_table(name)
        table.schema = schema

        try:
            table.create()
        except google.api.core.exceptions.Conflict:
            table.reload()

        return table

    def _copy_table_data(self, src_query, src_query_params, dest_table, write_disposition=None):
        from google.cloud.bigquery.job import WriteDisposition

        write_disposition = write_disposition or WriteDisposition.WRITE_APPEND

        logging.info(
            'copy_table_data to %s filter query: %s params: %s (%s)',
            dest_table.name, src_query, src_query_params, write_disposition)

        query_job = self._query_async(src_query, query_parameters=src_query_params)
        query_job.destination = dest_table
        query_job.write_disposition = write_disposition
        query_job.begin()
        self.handle_bq_errors(query_job.result())

    @classmethod
    def bq_field_name_to_common_name(cls, name):
        return '@' + name[1:] if name in ['_commit_sha', '_sha'] else name

    @classmethod
    def common_name_to_bq_field_name(cls, name):
        return '_' + name[1:] if name.startswith('@') else name

    @classmethod
    def build_dict(cls, row, query_job):
        destination_table = query_job.destination
        return {
            cls.bq_field_name_to_common_name(field.name): val for field, val in zip(destination_table.schema, row)
        }
