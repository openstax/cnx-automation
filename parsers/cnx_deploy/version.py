# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from functools import lru_cache

from parsers.cnx_deploy.base import Parser


class VersionParser(Parser):
    @property
    @lru_cache(maxsize=None)
    def dict(self):
        """Returns the json text as a dict."""
        import json
        return json.loads(self.text.strip())

    @property
    @lru_cache(maxsize=None)
    def dateless_dict(self):
        """Returns the json text as a dict, omitting the "date" key."""
        return {k: v for (k, v) in self.dict.items() if k != 'date'}

    @property
    def date(self):
        """Returns the value of the "date" field."""
        return self.dict['date']

    @property
    def webview(self):
        """Returns the value of the "webview" field."""
        return self.dict['webview']

    @property
    def webview_sha(self):
        """Returns the SHA in the "webview" field."""
        return self.webview.split()[0]

    @property
    def webview_tag(self):
        """Returns the tag name in the "webview" field."""
        return self.webview.split()[1]

    @property
    def cnx_archive(self):
        """Returns the value of the "cnx-archive" field."""
        return self.dict['cnx-archive']

    @property
    def cnx_publishing(self):
        """Returns the value of the "cnx-publishing" field."""
        return self.dict['cnx-publishing']

    @property
    def oer_exports(self):
        """Returns the value of the "oer.exports" field."""
        return self.dict['oer.exports']

    @property
    def oer_exports_release(self):
        """Returns the release name in the "oer.exports" field."""
        return self.oer_exports.split()[0]

    @property
    def oer_exports_tag(self):
        """Returns the tag name in the "oer.exports" field."""
        return self.oer_exports.split()[1]

    @property
    def cnx_deploy(self):
        """Returns the value of the "cnx-deploy" field."""
        return self.dict['cnx-deploy']

    def has_same_versions_as(self, other_parser):
        return self.dateless_dict == other_parser.dateless_dict
