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
    _version_regex = re.compile(r"^Nebuchadnezzar (.*)$")

    def run(cls, *args, **kwargs):
        """Runs Neb and returns a tuple containing stdout, stderr and the returncode"""
        if "stdout" not in kwargs:
            kwargs["stdout"] = subprocess.PIPE
        if "stderr" not in kwargs:
            kwargs["stderr"] = subprocess.PIPE
        if "universal_newlines" not in kwargs:
            kwargs["universal_newlines"] = True

        completed_process = subprocess.run(["neb", *args], **kwargs)
        return (
            completed_process.stdout.strip(),
            completed_process.stderr.strip(),
            completed_process.returncode,
        )

    def invoke(cls, *args, **kwargs):
        """Runs Neb and returns stdout; By default throws subprocess.CalledProcessError on error"""
        if "check" not in kwargs:
            kwargs["check"] = True

        return cls.run(*args, **kwargs)[0]

    @property
    def no_command(cls, **kwargs):
        """Runs `neb` without a command"""
        return cls.invoke(**kwargs)

    @property
    def help(cls, **kwargs):
        """Runs `neb --help` and returns the output"""
        return cls.invoke("--help", **kwargs)

    @property
    def version(cls, **kwargs):
        """Runs `neb --version` and returns the version number"""
        return cls._version_regex.match(cls.invoke("--version", **kwargs))[1]

    @contextmanager
    def get(cls, *, help=False, verbose=False, env=None, col_id=None, col_version=None, **kwargs):
        """Creates a temp dir, runs `neb get` with the given arguments, then yields the temp dir.

        Usage:
        with Neb.get(verbose=True, env=neb_env, col_id=col_id, col_version=col_version) as temp_dir:
            # Do something in temp_dir
        """
        if help:
            yield cls.invoke("get", "--help", **kwargs)
        elif env and col_id and col_version:
            with TemporaryDirectory() as temp_dir:
                # We cannot use temp_dir directly
                # because neb refuses to use a dir that already exists
                neb_dir = join(temp_dir, "neb")

                options = ["--output-dir", neb_dir]
                if verbose:
                    options.append("--verbose")

                cls.invoke("get", *options, env, col_id, col_version, **kwargs)

                yield neb_dir
        else:
            raise (
                TypeError(
                    "get() missing either 1 required keyword-only argument: 'help' or 3"
                    " required keyword-only arguments: 'env', 'col_id', and 'col_version'"
                )
            )

    @contextmanager
    def publish(
        cls,
        *,
        help=False,
        verbose=False,
        env=None,
        content_dir=None,
        publication_message=None,
        **kwargs,
    ):
        """Yields the content_dir (or a temp dir), then runs `neb publish` on the given dir.

        Usage (with existing dir):
        with Neb.publish(verbose=True, env=neb_env, content_dir=some_dir,
                         publication_message='changed something'):
            pass

        Usage (with temp dir):
        with Neb.publish(verbose=True, env=neb_env,
                         publication_message='changed something') as temp_dir:
            # Add content to publish to temp_dir
        """
        if help:
            yield cls.invoke("publish", "--help", **kwargs)
        elif env and publication_message:
            options = []
            if verbose:
                options.append("--verbose")

            if content_dir:
                yield content_dir

                cls.invoke("publish", *options, env, content_dir, publication_message, **kwargs)
            else:
                with TemporaryDirectory() as temp_dir:
                    yield temp_dir

                    cls.invoke("publish", *options, env, temp_dir, publication_message, **kwargs)
        else:
            raise (
                TypeError(
                    "publish() missing either 1 required keyword-only argument: 'help'"
                    " or 2 required keyword-only arguments: 'env',"
                    " and 'publication_message'"
                )
            )


class Neb(metaclass=MetaNeb):
    pass
