# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.webview.base import Base

from selenium.webdriver.common.by import By


class AboutUs(Base):
    _about_us_link_locator = (By.CSS_SELECTOR, '#about .about-nav a[href="/about"]')
    _contact_link_locator = (By.CSS_SELECTOR, '#about .about-nav a[href="/about/contact"]')

    @property
    def about_us_link(self):
        return self.find_element(*self._about_us_link_locator)

    @property
    def contact_link(self):
        return self.find_element(*self._contact_link_locator)

    @property
    def loaded(self):
        return (self.is_element_displayed(*self._about_us_link_locator) and
                self.is_element_displayed(*self._contact_link_locator))
