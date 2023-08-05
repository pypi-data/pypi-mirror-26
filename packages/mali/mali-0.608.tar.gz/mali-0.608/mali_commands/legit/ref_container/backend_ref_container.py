# coding=utf-8
from ..backend_mixin import BackendMixin
from ..dulwich.refs import RefsContainer


SYMREF = b'ref: '


class BackendRefContainer(BackendMixin, RefsContainer):
    def __init__(self, connection, config, handle_api):
        super(BackendRefContainer, self).__init__(connection, config, handle_api)

    def __build_key(self, datastore, name):
        org_name = self.__connection.data_volume_config.org
        parent_key = datastore.key('DataVolume', self.__connection.data_volume_config.name, namespace=org_name)

        return datastore.key('DataVolumeRef', name, parent=parent_key, namespace=org_name)

    def get_packed_refs(self):
        return {}

    def set_if_equals(self, name, old_ref, new_ref):
        raise NotImplementedError(self.set_if_equals)

    def add_if_new(self, name, ref):
        raise NotImplementedError(self.add_if_new)

    def read_loose_ref(self, name):
        with self._connection.get_cursor() as session:
            url = 'data_volumes/%s/ref/%s' % (self._volume_id, name)

            result = self._handle_api(self._config, session.get, url)

            return result['commit_sha']

    def set_symbolic_ref(self, name, other):
        raise NotImplementedError(self.set_symbolic_ref)

    def allkeys(self):
        raise NotImplementedError(self.allkeys)

    def remove_if_equals(self, name, old_ref):
        raise NotImplementedError(self.remove_if_equals)
