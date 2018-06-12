# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import subprocess


# Property class methods: https://stackoverflow.com/a/5189765
class MetaNeb(type):
    _version_regex = re.compile('^Nebuchadnezzar (.*)$')

    def run(cls, *args, check=True):
        return subprocess.run(['neb', *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              check=check).stdout.decode().strip()

    @property
    def help(cls):
        return cls.run('--help')

    @property
    def version(cls):
        return cls._version_regex.match(cls.run('--version'))[1]

    def get(cls, *, help=False, env=None, col_id=None, col_version=None):
        if help:
            return cls.run('get', '--help')
        elif env is None or col_id is None or col_version is None:
            raise(TypeError("get() missing either 1 required keyword-only argument: 'help' or 3"
                            " required keyword-only arguments: 'env', 'col_id', and 'col_version'"))

        return cls.run('get', env, col_id, col_version)


class Neb(metaclass=MetaNeb):
    pass
