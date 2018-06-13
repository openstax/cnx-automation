# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import subprocess
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from os.path import join


# Property class methods: https://stackoverflow.com/a/5189765
class MetaNeb(type):
    _version_regex = re.compile('^Nebuchadnezzar (.*)$')

    def run(cls, *args, **kwargs):
        """Runs Neb and returns a tuple containing stdout, stderr and the returncode"""
        if 'stdout' not in kwargs:
            kwargs['stdout'] = subprocess.PIPE
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        if 'universal_newlines' not in kwargs:
            kwargs['universal_newlines'] = True

        completed_process = subprocess.run(['neb', *args], **kwargs)
        return (completed_process.stdout.strip(),
                completed_process.stderr.strip(),
                completed_process.returncode)

    def invoke(cls, *args, **kwargs):
        """Runs Neb and returns stdout; By default throws subprocess.CalledProcessError on error"""
        if 'check' not in kwargs:
            kwargs['check'] = True

        return cls.run(*args, **kwargs)[0]

    @property
    def no_command(cls):
        return cls.invoke()

    @property
    def help(cls):
        return cls.invoke('--help')

    @property
    def version(cls):
        return cls._version_regex.match(cls.invoke('--version'))[1]

    @contextmanager
    def get(cls, *, help=False, verbose=False, env=None, col_id=None, col_version=None, prompt='y'):
        if help:
            yield cls.invoke('get', '--help')
        elif env is None or col_id is None or col_version is None:
            raise(TypeError("get() missing either 1 required keyword-only argument: 'help' or 3"
                            " required keyword-only arguments: 'env', 'col_id', and 'col_version'"))
        else:
            with TemporaryDirectory() as temp_dir:
                # We cannot use temp_dir directly
                # because neb refuses to use a dir that already exists
                neb_dir = join(temp_dir, 'neb')

                options = ['--output-dir', neb_dir]
                if verbose:
                    options.append('--verbose')

                cls.invoke('get', *options, env, col_id, col_version, input=prompt)

                yield neb_dir

    @contextmanager
    def publish(cls, *, help=False, verbose=False, env=None,
                content_dir=None, publication_message=None):
        if help:
            yield cls.invoke('publish', '--help')
        elif env is None or content_dir is None or publication_message is None:
            raise(TypeError("publish() missing either 1 required keyword-only argument: 'help'"
                            " or 3 required keyword-only arguments: 'env', 'content_dir',"
                            " and 'publication_message'"))
        else:
            raise(NotImplementedError)


class Neb(metaclass=MetaNeb):
    pass
