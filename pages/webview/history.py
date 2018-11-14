# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from parsers.cnx_deploy.release import ReleaseParser


class History(Page):
    URL_TEMPLATE = "/history.txt"
    _pre_locator = (By.TAG_NAME, "pre")
    _releases_separator = "==============================="

    @property
    def text(self):
        return self.find_element(*self._pre_locator).text

    @property
    def releases(self):
        return self.text.split(self._releases_separator)

    @property
    def release_parsers(self):
        return [ReleaseParser(release) for release in self.releases if release.strip()]
