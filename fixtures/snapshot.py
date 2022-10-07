# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import json
import tarfile

import pytest

from deepdiff import DeepDiff

__all__ = ["snapshot"]

SNAPSHOT_BASE_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "../snapshots")


class Snapshot(object):
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_snapshot_path(self, category, name):
        return os.path.join(self.base_dir, category, name)

    def ensure_dir_exists(self, path):
        dir = os.path.dirname(path)
        if not os.path.isdir(dir):
            os.makedirs(dir, 0o755)

        return dir

    def get_snapshot_path_and_ensure_dir_exists(self, category, name):
        snapshot_path = os.path.join(self.base_dir, category, name)

        snapshot_dir = os.path.dirname(snapshot_path)
        if not os.path.isdir(snapshot_dir):
            os.makedirs(snapshot_dir, 0o755)

        return snapshot_path

    def assert_dict_match(self, value, name):
        snapshot_path = self.get_snapshot_path_and_ensure_dir_exists("json", name)

        with open(snapshot_path, "a+") as snapshot_file:
            snapshot_file.seek(0)
            snapshot = snapshot_file.read()
            if snapshot:
                assert value == json.loads(snapshot), (
                    "Value did not match snapshot.\n\n"
                    "Value:\n\n{value}\n\n"
                    "Snapshot:\n\n{snapshot}".format(value=value, snapshot=snapshot)
                )
            else:
                json.dump(value, snapshot_file)

    def assert_file_or_dir_match(self, path, name):

        snapshot_path = self.get_snapshot_path_and_ensure_dir_exists("tar_gz", name)

        if os.path.isfile(snapshot_path):
            with tarfile.open(snapshot_path, "r|gz", encoding="utf-8") as snapshot_tar:
                for snapshot_tarinfo in snapshot_tar:
                    name = snapshot_tarinfo.name
                    subpath = os.path.join(path, name)
                    if snapshot_tarinfo.isdir():
                        assert os.path.isdir(subpath)
                        continue
                    with snapshot_tar.extractfile(snapshot_tarinfo) as snapshot_file:
                        snapshot_value = snapshot_file.read()
                    with open(subpath, "rb") as new_file:
                        value = new_file.read()
                    if ".sha1sum" in name:
                        assert (sorted(snapshot_value.split(b"\n")) == sorted(value.split(b"\n")))
                        continue
                    if ".json" in name:
                        value_data = json.loads(value)
                        snapshot_data = json.loads(snapshot_value)
                        # Ignore `canon_url` in comparison
                        value_data.pop('canon_url')
                        snapshot_data.pop('canon_url')
                        diff = DeepDiff(value_data, snapshot_data, ignore_order=True)
                        assert diff == {}
                        continue
                    assert value == snapshot_value, "{name} did not match the snapshot.".format(
                        name=name
                    )
        else:
            with tarfile.open(snapshot_path, "w|gz", encoding="utf-8") as snapshot_tar:
                # arcname='.' makes tar not save the absolute path
                # See comments in https://stackoverflow.com/a/2239679
                snapshot_tar.add(path, arcname=".")

    def extract(self, name, path):
        snapshot_path = self.get_snapshot_path("tar_gz", name)
        self.ensure_dir_exists(path)

        with tarfile.open(snapshot_path, "r|gz") as snapshot_tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(snapshot_tar, path=path)


@pytest.fixture(scope="session")
def snapshot(request):
    """Return an object that can save and compare snapshots"""
    return Snapshot(SNAPSHOT_BASE_DIR)
