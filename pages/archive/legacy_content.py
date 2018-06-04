# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from pages.archive.base import Page


class LegacyContent(Page):
    URL_TEMPLATE = '/content/{legacy_id}'
    _uuid_and_version_regex = re.compile('^/contents/(.*)$')

    @property
    def uuid_and_version(self):
        """Extracts and returns the collection or page uuid and version from the url."""
        from urllib.parse import urlsplit
        return re.match(self._uuid_and_version_regex, urlsplit(self.driver.current_url)[2]).group(1)

    def open(self):
        """Opens the legacy archive url and follows the redirect to the non-legacy archive url.
           Returns an instance of pages.archive.content.Content
        """
        super().open()
        from pages.archive.content import Content
        return Content(self.driver, self.base_url, self.timeout,
                       uuid_and_version=self.uuid_and_version).open()
