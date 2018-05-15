# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Base


class Content(Base):
    _title_locator = (By.CLASS_NAME, 'large-header')
    _ncy_locator = (By.CLASS_NAME, 'not-converted-yet')

    @property
    def loaded(self):
        return '@' in self.driver.current_url

    @property
    def title(self):
        return self.find_element(*self._title_locator).text

    @property
    def is_ncy_displayed(self):
        return self.is_element_displayed(*self._ncy_locator)
