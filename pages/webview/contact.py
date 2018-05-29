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
        _questions_header_locator = (By.XPATH, './h2[text()="Questions?"]')
        _technical_support_header_locator = (
            By.XPATH, './h2[text()="Questions?"]/following-sibling::h3[text()="Technical Support"]')
        _general_questions_header_locator = (
            By.XPATH, './h2[text()="Questions?"]/following-sibling::h3[text()="General Questions"]')

        @property
        def is_email_displayed(self):
            return self.is_element_displayed(*self._email_link_locator)

        @property
        def is_map_displayed(self):
            return self.is_element_displayed(*self._map_img_locator)

        @property
        def is_questions_header_displayed(self):
            return self.is_element_displayed(*self._questions_header_locator)

        @property
        def is_technical_support_header_displayed(self):
            return self.is_element_displayed(*self._technical_support_header_locator)

        @property
        def is_general_questions_header_displayed(self):
            return self.is_element_displayed(*self._general_questions_header_locator)
