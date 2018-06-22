# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tempfile import TemporaryDirectory
import subprocess
from functools import lru_cache


class Git(TemporaryDirectory):
    """Creates a temp dir, checks out a git repository, and runs git commands on it.

    Usage example:
    with Git('https://github.com/Connexions/webview.git') as webview_git:
        print(webview_git.latest_tag)
    """

    def run(self, *args, **kwargs):
        """Runs git and returns a tuple containing stdout, stderr and the returncode"""
        if 'stdout' not in kwargs:
            kwargs['stdout'] = subprocess.PIPE
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        if 'cwd' not in kwargs:
            kwargs['cwd'] = self.name
        if 'universal_newlines' not in kwargs:
            kwargs['universal_newlines'] = True

        completed_process = subprocess.run(['git', *args], **kwargs)
        return (completed_process.stdout.strip(),
                completed_process.stderr.strip(),
                completed_process.returncode)

    def invoke(self, *args, **kwargs):
        """Runs git and returns stdout; By default throws subprocess.CalledProcessError on error"""
        if 'check' not in kwargs:
            kwargs['check'] = True

        return self.run(*args, **kwargs)[0]

    def __init__(self, repository_url):
        super().__init__()
        # https://stackoverflow.com/a/8055594
        self.invoke('clone', '--shallow-submodules', repository_url, '.')

    def __enter__(self):
        super().__enter__()
        return self

    @property
    @lru_cache(maxsize=None)
    def latest_tag(self):
        return self.invoke('describe', '--abbrev=0', '--tags')

    def tag_hash(self, tag):
        return self.invoke('rev-list', '--max-count=1', tag)

    @property
    def latest_tag_hash(self):
        return self.tag_hash(self.latest_tag)

    @classmethod
    def shorten_tag(cls, tag):
        return tag.split('-')[0]
