# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess


# Property class methods: https://stackoverflow.com/a/5189765
class MetaNeb(type):

    def run(cls, *args):
        return subprocess.run(['neb', *args], stdout=subprocess.PIPE,
                              check=True).stdout.decode('ascii').strip()

    @property
    def help(cls):
        return cls.run('--help')

    @property
    def version(cls):
        return cls.run('--version').replace('Nebuchadnezzar ', '')


class Neb(metaclass=MetaNeb):
    pass
