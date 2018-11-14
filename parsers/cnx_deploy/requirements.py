# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from re import compile

from parsers.cnx_deploy.base import Parser


class RequirementsParser(Parser):
    _git_requirement_regex = compile(
        r'^(?:-e )?git\+(?P<repository>[^@]+)(?:@(?P<version>[^#]+))?#egg=(?P<name>.+)$')

    def is_blank(self, line):
        """Returns whether or not the line is blank."""
        return not line or line.startswith('#')

    def split_requirement(self, line):
        """Splits a requirement into a tuple containing (name, repository, version)."""
        match = self._git_requirement_regex.match(line)
        if match:
            return (match['name'], match['repository'], match['version'])
        else:
            split = line.split('==', 1)
            return (split[0], None, split[1])

    @property
    def requirements_list(self):
        """Returns the requirements as a list of tuples."""
        lines = self.text.splitlines()
        return [self.split_requirement(line) for line in lines if not self.is_blank(line)]

    @property
    def requirements(self):
        """Returns the requirements as a list of dicts."""
        return [{'name': name, 'version': version, 'repository': repository}
                for name, repository, version in self.requirements_list]

    def has_same_versions_as(self, other_parser):
        return self.requirements == other_parser.requirements
