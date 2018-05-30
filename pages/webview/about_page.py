# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page


class AboutPage(Page):
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

    def click_about_us(self):
        self.about_us_link.click()
        from pages.webview.about_us import AboutUs
        return AboutUs(self.driver, self.base_url, self.timeout).wait_for_page_to_load()

    def click_contact(self):
        self.contact_link.click()
        from pages.webview.contact import Contact
        return Contact(self.driver, self.base_url, self.timeout).wait_for_page_to_load()
