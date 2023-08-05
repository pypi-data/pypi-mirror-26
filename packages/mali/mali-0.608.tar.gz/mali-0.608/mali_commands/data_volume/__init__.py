# coding=utf-8
import os
import errno
import six

from contextlib import closing
import click

from mali_commands.data_volume_config import DataVolumeConfig
from mali_commands.legit.repo import MlRepo
from mali_commands.config import Config


def default_data_volume_path(volume_id):
    return os.path.join(os.path.expanduser('~'), '.MissingLinkAI', 'data_volumes', volume_id)


def create_data_volume(volume_id, data_path, linked, display_name, description):
    path = default_data_volume_path(volume_id)

    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    config = DataVolumeConfig(path)
    config.update_and_save(
        {
            'general': {
                'id': volume_id,
                'embedded': not linked,
                'datapath': data_path,
                'display_name': display_name,
                'description': description
            }
        }
    )

    return config


def with_repo(ctx, volume_id, read_only=False):
    config_prefix = ctx if isinstance(ctx, six.string_types) or ctx is None else ctx.obj.config_prefix

    config = Config(config_prefix)

    repo_root = default_data_volume_path(volume_id)

    return closing(MlRepo(config, repo_root, read_only=read_only))


def validate_repo_data_path(repo, volume_id):
    if not repo.data_path:
        msg = "Data Volume {volume_id} is not mapped to a local folder,\n" \
              "the data root is needed in order to add data to the data volume.\n" \
              "You can run:\n" \
              "mali data get {volume_id} --dataPath <data root folder>".format(volume_id=volume_id)
        click.echo(msg.strip(), err=True)
        exit(1)
