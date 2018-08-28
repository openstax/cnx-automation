# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.about_page import AboutPage
from regions.webview.base import Region


class Contact(AboutPage):

    @property
    def contact_content(self):
        return self.ContactContent(self)

    @property
    def loaded(self):
        # super().loaded checks that the about us/contact links are displayed
        return self.contact_content.loaded and super().loaded

    class ContactContent(Region):
        _root_locator = (By.ID, 'about')
        _email_link_locator = (By.CSS_SELECTOR, '.contact > p:nth-child(5) > a')
        _questions_header_locator = (
            By.CSS_SELECTOR, '[data-l10n-id="about-contact-questions-header"]')

        @property
        def is_email_displayed(self):
            return self.is_element_displayed(*self._email_link_locator)

        @property
        def email_link(self):
            return self.find_element(*self._email_link_locator)

        @property
        def email_url(self):
            return self.email_link.get_attribute('href')

        @property
        def questions_header(self):
            return self.find_element(*self._questions_header_locator)
