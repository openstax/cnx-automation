# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from parsers.cnx_deploy.base import Parser
from parsers.cnx_deploy.version import VersionParser
from parsers.cnx_deploy.requirements import RequirementsParser


class ReleaseParser(Parser):
    _requirements_separator = '-------------------------------'

    @property
    def version_text(self):
        """Returns the version (JSON) part of the release as text."""
        return self.text.split(self._requirements_separator)[0].strip()

    @property
    def version_parser(self):
        """Returns a parser for the version (JSON) part of the release."""
        return VersionParser(self.version_text)

    @property
    def requirements_text(self):
        """Returns the requirements.txt part of the release as text."""
        return self.text.split(self._requirements_separator)[1].strip()

    @property
    def requirements_parser(self):
        """Returns parser for the requirements.txt part of the release."""
        return RequirementsParser(self.requirements_text)
