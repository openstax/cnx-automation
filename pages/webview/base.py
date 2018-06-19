# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pypom

from selenium.webdriver.common.by import By

from regions.webview.base import Region


class Page(pypom.Page):

    # Default to a 60 second timeout for CNX webview
    def __init__(self, driver, base_url=None, timeout=60, **url_kwargs):
        super().__init__(driver, base_url, timeout, **url_kwargs)

    @property
    def header(self):
        # Need to wait for the header to display because the nav menu initially loads with 0 height
        return self.Header(self).wait_for_region_to_display()

    class Header(Region):
        _root_locator = (By.ID, 'header')
        # This is the CSS selector that currently applies the logo background-image
        _logo_locator = (
            By.CSS_SELECTOR,
            '.page-header > .navbar > .container-fluid > .navbar-header > .navbar-brand'
        )
        _browse_locator = (By.CSS_SELECTOR, '#page-nav #nav-browse a')
        _about_us_locator = (By.CSS_SELECTOR, '#page-nav #nav-about a')
        _donate_locator = (By.CSS_SELECTOR, '#page-nav #nav-donate a')

        @property
        def logo(self):
            return self.find_element(*self._logo_locator)

        @property
        def is_logo_displayed(self):
            return self.is_element_displayed(*self._logo_locator)

        @property
        def is_nav_displayed(self):
            return (self.is_element_displayed(*self._browse_locator) and
                    self.is_element_displayed(*self._about_us_locator) and
                    self.is_element_displayed(*self._donate_locator))

        @property
        def is_displayed(self):
            return self.is_logo_displayed and self.is_nav_displayed

        def click_logo(self):
            self.logo.click()
            from pages.webview.home import Home
            return Home(self.driver, self.page.base_url, self.page.timeout).wait_for_page_to_load()

        def click_search(self):
            self.find_element(*self._browse_locator).click()
            from pages.webview.browse import Browse
            browse = Browse(self.driver, self.page.base_url, self.page.timeout)
            return browse.wait_for_page_to_load()

        def click_about_us(self):
            self.find_element(*self._about_us_locator).click()
            from pages.webview.about_us import AboutUs
            about_us = AboutUs(self.driver, self.page.base_url, self.page.timeout)
            return about_us.wait_for_page_to_load()

        def click_donate(self):
            self.find_element(*self._donate_locator).click()
            from pages.webview.donate import Donate
            donate = Donate(self.driver, self.page.base_url, self.page.timeout)
            return donate.wait_for_page_to_load()
