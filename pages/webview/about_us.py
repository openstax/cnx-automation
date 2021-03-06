# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.about_page import AboutPage
from regions.webview.base import Region


class AboutUs(AboutPage):
    @property
    def about_content(self):
        return self.AboutContent(self)

    @property
    def loaded(self):
        # super().loaded checks that the about us/contact links are displayed
        return self.about_content.loaded and super().loaded

    class AboutContent(Region):
        _root_locator = (By.CSS_SELECTOR, '#about .about-content div[data-l10n-id="about-content"]')
        _learn_more_team_link_locator = (By.CSS_SELECTOR, 'a[href="https://openstax.org/about"]')
        _learn_more_foundations_link_locator = (
            By.CSS_SELECTOR,
            'a[href="https://openstax.org/foundation"]',
        )

        @property
        def learn_more_team_link(self):
            return self.find_element(*self._learn_more_team_link_locator)

        @property
        def learn_more_team_text(self):
            return self.learn_more_team_link.text

        @property
        def learn_more_foundations_link(self):
            return self.find_element(*self._learn_more_foundations_link_locator)

        @property
        def learn_more_foundations_text(self):
            return self.learn_more_foundations_link.text
