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

    class ContactContent(Region):
        _root_locator = (By.CSS_SELECTOR, '#about .about-content div.contact')
        _map_img_locator = (By.CSS_SELECTOR, 'img[src="/locale/en-US/images/map.png"]')

        @property
        def is_map_displayed(self):
            return self.is_element_displayed(*self._map_img_locator)
