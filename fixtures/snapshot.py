# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import json
import tarfile

import pytest

__all__ = ['snapshot']

SNAPSHOT_BASE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), '../snapshots')


class Snapshot(object):

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_snapshot_path_and_ensure_dir_exists(self, category, name):
        snapshot_path = os.path.join(self.base_dir, category, name)

        snapshot_dir = os.path.dirname(snapshot_path)
        if not os.path.isdir(snapshot_dir):
            os.makedirs(snapshot_dir, 0o755)

        return snapshot_path

    def assert_json_match(self, value, name):
        snapshot_path = self.get_snapshot_path_and_ensure_dir_exists('json', name)

        with open(snapshot_path, 'a+') as snapshot_file:
            snapshot_file.seek(0)
            snapshot = snapshot_file.read()
            if snapshot:
                assert value == json.loads(snapshot), \
                       ("Value did not match snapshot.\n\n"
                        "Value:\n\n{value}\n\n"
                        "Snapshot:\n\n{snapshot}".format(value=value, snapshot=snapshot))
            else:
                json.dump(value, snapshot_file)

    def assert_tar_gz_match(self, path, name):
        snapshot_path = self.get_snapshot_path_and_ensure_dir_exists('tar_gz', name)

        if os.path.isfile(snapshot_path):
            with tarfile.open(snapshot_path, 'r|gz') as snapshot_tar:
                for snapshot_tarinfo in snapshot_tar:
                    subpath = os.path.join(path, snapshot_tarinfo.name)

                    if snapshot_tarinfo.isdir():
                        assert os.path.isdir(subpath)
                    else:
                        with snapshot_tar.extractfile(snapshot_tarinfo) as snapshot_file:
                            snapshot_value = snapshot_file.read()
                        with open(subpath, 'rb') as file:
                            value = file.read()
                        assert value == snapshot_value
        else:
            with tarfile.open(snapshot_path, 'w|gz') as snapshot_tar:
                # arcname='.' makes tar not save the absolute path (/tmp/whatever)
                # See comments in https://stackoverflow.com/a/2239679
                snapshot_tar.add(path, arcname='.')


@pytest.fixture(scope='session')
def snapshot(request):
    """Return an object that can save and compare snapshots"""
    return Snapshot(SNAPSHOT_BASE_DIR)
