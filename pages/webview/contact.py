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
        _root_locator = (By.CSS_SELECTOR, '#about .about-content div.contact')
        _email_link_locator = (By.CSS_SELECTOR, 'a[href="mailto:support@openstax.org"]')
        _map_img_locator = (By.CSS_SELECTOR, 'img[src="/locale/en-US/images/map.png"]')
        _questions_header_locator = (
            By.CSS_SELECTOR, '[data-l10n-id="about-contact-questions-header"]')
        _technical_support_header_locator = (
            By.CSS_SELECTOR, '[data-l10n-id="about-contact-technical-support-header"]')
        _general_questions_header_locator = (
            By.CSS_SELECTOR, '[data-l10n-id="about-contact-general-questions-header"]')

        @property
        def is_email_displayed(self):
            return self.is_element_displayed(*self._email_link_locator)

        @property
        def is_map_displayed(self):
            return self.is_element_displayed(*self._map_img_locator)

        @property
        def questions_header(self):
            return self.find_element(*self._questions_header_locator)

        @property
        def technical_support_header(self):
            return self.find_element(*self._technical_support_header_locator)

        @property
        def general_questions_header(self):
            return self.find_element(*self._general_questions_header_locator)

        @property
        def loaded(self):
            # super().loaded checks that the Region root element is present
            # is_map_displayed waits until the map has at least started loading
            return super().loaded and self.is_map_displayed
