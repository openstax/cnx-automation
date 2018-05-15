# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page, Region
from selenium.webdriver.common.by import By


class Base(Page):

    def __init__(self, selenium, base_url, **kwargs):
        super().__init__(selenium, base_url, timeout=30, **kwargs)

    @property
    def header(self):
        return self.Header(self)

    class Header(Region):
        _root_locator = (By.ID, 'header')
        _nav_locator = (By.ID, 'page-nav')

        @property
        def is_nav_displayed(self):
            return self.is_element_displayed(*self._nav_locator)
