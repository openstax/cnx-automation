# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from parsers.cnx_deploy.version import VersionParser


class Version(Page):
    URL_TEMPLATE = '/version.txt'
    _pre_locator = (By.TAG_NAME, 'pre')

    @property
    def text(self):
        return self.find_element(*self._pre_locator).text

    @property
    def version_parser(self):
        return VersionParser(self.text)
