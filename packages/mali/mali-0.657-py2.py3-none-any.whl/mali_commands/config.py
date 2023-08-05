# coding=utf-8
import os

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

_missing_link_config = 'missinglink.cfg'


default_api_host = 'https://missinglinkai.appspot.com'
default_host = 'https://missinglink.ai'
default_client_id = 'nbkyPAMoxj5tNzpP07vyrrsVZnhKYhMj'
default_auth0 = 'missinglink'


def find_first_file(config_prefix, filename):
    filename_with_prefix = '%s-%s' % (config_prefix, filename) if config_prefix else filename

    possible_paths = [os.getcwd(), os.path.expanduser('~')]

    for possible_path in possible_paths:
        candidate_config_file = os.path.join(possible_path, filename_with_prefix)

        if os.path.isfile(candidate_config_file):
            return candidate_config_file

    return filename_with_prefix


class Config(object):
    def __init__(self, config_prefix):
        self.config_prefix = config_prefix

        config_file_abs_path = find_first_file(self.config_prefix, _missing_link_config)

        parser = configparser.RawConfigParser()
        parser.read([config_file_abs_path])

        self.parser = parser

        readonly_parser = configparser.RawConfigParser()
        readonly_parser.read([self.prefixed_config_name])

        self.readonly_parser = readonly_parser

    @property
    def prefixed_config_name(self):
        return '%s-%s' % (self.config_prefix, _missing_link_config)

    @property
    def api_host(self):
        return self.general_config.get('api_host', default_api_host)

    @property
    def host(self):
        return self.general_config.get('host', default_host)

    @property
    def client_id(self):
        return self.general_config.get('client_id', default_client_id)

    @property
    def auth0(self):
        return self.general_config.get('auth0', default_auth0)

    def get_prefix_section(self, section):
        from mali_commands.commons import get_prefix_section

        return get_prefix_section(self.config_prefix, section)

    @property
    def token_config(self):
        section_name = self.get_prefix_section('token')
        return self.items(section_name, most_exists=False)

    @property
    def general_config(self):
        return self.readonly_items('general', most_exists=self.config_prefix is not None)

    @property
    def refresh_token(self):
        return self.token_config.get('refresh_token')

    @property
    def id_token(self):
        return self.token_config.get('id_token')

    @property
    def user_id(self):
        import jwt

        data = jwt.decode(self.id_token, verify=False) if self.id_token else {}

        return data.get('user_external_id')

    @classmethod
    def items_from_parse(cls, parser, section, most_exists):
        try:
            return dict(parser.items(section))
        except configparser.NoSectionError:
            if most_exists:
                raise

            return {}

    def items(self, section, most_exists=False):
        return self.items_from_parse(self.parser, section, most_exists=most_exists)

    def readonly_items(self, section, most_exists=False):
        return self.items_from_parse(self.readonly_parser, section, most_exists=most_exists)

    def set(self, section, key, val):
        try:
            self.parser.add_section(section)
        except configparser.DuplicateSectionError:
            pass

        self.parser.set(section, key, val)

    def _write(self, fo):
        self.parser.write(fo)

    def save(self):
        config_file_abs_path = find_first_file(self.config_prefix, _missing_link_config)

        with open(config_file_abs_path, 'w') as configfile:
            self._write(configfile)

    def update_and_save(self, d):
        for section, section_values in d.items():
            section_name_with_prefix = self.get_prefix_section(section)
            for key, val in section_values.items():
                self.set(section_name_with_prefix, key, val)

        self.save()
