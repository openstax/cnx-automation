# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import subprocess
from contextlib import contextmanager
from os.path import join, isdir
from shutil import rmtree


# Property class methods: https://stackoverflow.com/a/5189765
class MetaNeb(type):
    _version_regex = re.compile('^Nebuchadnezzar (.*)$')
    _tmp_dir = '/tmp'

    def invoke(cls, *args, check=True):
        return subprocess.run(['neb', *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              check=check).stdout.decode().strip()

    @property
    def help(cls):
        return cls.invoke('--help')

    @property
    def version(cls):
        return cls._version_regex.match(cls.invoke('--version'))[1]

    @contextmanager
    def get(cls, *, help=False, verbose=False, env=None, col_id=None, col_version=None):
        if help:
            yield cls.invoke('get', '--help')
            return
        elif env is None or col_id is None or col_version is None:
            raise(TypeError("get() missing either 1 required keyword-only argument: 'help' or 3"
                            " required keyword-only arguments: 'env', 'col_id', and 'col_version'"))

        options = []
        if verbose:
            options.append('--verbose')

        dir = join(cls._tmp_dir, col_id, col_version)

        try:
            cls.invoke(*options, 'get', '--output-dir', dir, env, col_id, col_version)
            yield dir
        finally:
            if isdir(dir):
                rmtree(dir)


class Neb(metaclass=MetaNeb):
    pass
