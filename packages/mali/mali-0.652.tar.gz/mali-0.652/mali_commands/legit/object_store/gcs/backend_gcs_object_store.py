# coding=utf-8
import requests

from ...backend_mixin import BackendMixin
from .gcs_object_store import GCSObjectStore
from six.moves.urllib import parse


class BackendGCSSignedUrlService(BackendMixin):
    def __init__(self, connection, config, handle_api):
        super(BackendGCSSignedUrlService, self).__init__(connection, config, handle_api)

    def get_signed_urls(self, method, object_names):
        params = {
            'method': method,
            'paths': object_names
        }
        url = 'data_volumes/{volume_id}/gcs_urls?{query_params}'.format(
            volume_id=self._volume_id, query_params=parse.urlencode(params, True))

        result = self._handle_api(self._config, requests.get, url)

        return result.get('urls', [])


class BackendGCSObjectStore(BackendMixin, GCSObjectStore):
    def __init__(self, connection, config, handle_api):
        super(BackendGCSObjectStore, self).__init__(connection, config, handle_api)
        self.__bucket_name = None
        self._signed_url_service = BackendGCSSignedUrlService(connection, config, handle_api)

    def __iter__(self):
        return super(BackendGCSObjectStore, self).__iter__()

    def add_objects(self, objects):
        return super(BackendGCSObjectStore, self).add_objects(self)

    @property
    def packs(self):
        return super(BackendGCSObjectStore, self).packs

    def contains_loose(self, sha):
        return super(BackendGCSObjectStore, self).contains_loose(sha)

    def contains_packed(self, sha):
        return super(BackendGCSObjectStore, self).contains_packed(sha)
