# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.archive.base import Page

from selenium.webdriver.common.by import By


class LegacyContent(Page):

    URL_TEMPLATE = '/content/{module_id}'

    _title_locator = (By.CSS_SELECTOR, 'div[data-type="document-title"]')

    @property
    def uuid_and_version(self):
        import re
        from urllib.parse import urlsplit
        return re.sub('/contents/', '', urlsplit(self.driver.current_url)[2])

    @property
    def loaded(self):
        return super().loaded and self.is_element_displayed(*self._title_locator)

    def open(self):
        super().open()
        from pages.archive.content import Content
        return Content(self.driver, self.base_url, self.timeout,
                       uuid_and_version=self.uuid_and_version).open()
