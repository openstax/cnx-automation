# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region

from pages.webview.base import Base

from selenium.webdriver.common.by import By


class AboutUs(Base):
    _about_us_link_locator = (By.CSS_SELECTOR, '#about .about-nav a[href="/about"]')
    _contact_link_locator = (By.CSS_SELECTOR, '#about .about-nav a[href="/about/contact"]')
    _about_content_div_locator = (By.CSS_SELECTOR,
                                  '#about .about-content div[data-l10n-id="about-content"]')

    @property
    def about_us_link(self):
        return self.find_element(*self._about_us_link_locator)

    @property
    def contact_link(self):
        return self.find_element(*self._contact_link_locator)

    @property
    def about_content(self):
        return self.AboutContent(self)

    @property
    def loaded(self):
        return (self.is_element_displayed(*self._about_us_link_locator) and
                self.is_element_displayed(*self._contact_link_locator))

    class AboutContent(Region):
        _root_locator = (By.CSS_SELECTOR, '#about .about-content div[data-l10n-id="about-content"]')
        _learn_more_team_link_locator = (
            By.XPATH,
            './/a[text()="Learn more about the OpenStax team"]'
        )
        _learn_more_foundations_link_locator = (
            By.XPATH,
            './/a[text()="Learn more about the foundations supporting OpenStax projects like CNX"]'
        )

        @property
        def text(self):
            return self.root.text

        @property
        def learn_more_team_link(self):
            return self.find_element(*self._learn_more_team_link_locator)

        @property
        def learn_more_team_url(self):
            return self.learn_more_team_link.get_attribute('href')

        @property
        def learn_more_foundations_link(self):
            return self.find_element(*self._learn_more_foundations_link_locator)

        @property
        def learn_more_foundations_url(self):
            return self.learn_more_foundations_link.get_attribute('href')
