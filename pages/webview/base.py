# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page, Region
from selenium.webdriver.common.by import By


class Base(Page):

    # Default to a 30 second timeout for CNX webview
    def __init__(self, driver, base_url=None, timeout=30, **url_kwargs):
        super().__init__(driver, base_url, timeout, **url_kwargs)

    @property
    def header(self):
        return self.Header(self)

    class Header(Region):
        _root_locator = (By.ID, 'header')
        # This is the CSS selector that currently applies the logo background-image
        _logo_locator = (
            By.CSS_SELECTOR,
            '.page-header > .navbar > .container-fluid > .navbar-header > .navbar-brand'
        )
        _nav_locator = (By.ID, 'page-nav')
        _browse_locator = (By.CSS_SELECTOR, '#nav-browse a')
        _about_us_locator = (By.CSS_SELECTOR, '#nav-about a')

        @property
        def logo(self):
            return self.find_element(*self._logo_locator)

        @property
        def is_nav_displayed(self):
            return self.is_element_displayed(*self._nav_locator)

        def click_logo(self):
            self.logo.click()
            from pages.webview.home import Home
            return Home(self.driver, self.page.base_url, self.page.timeout).wait_for_page_to_load()

        def click_browse(self):
            self.find_element(*self._browse_locator).click()
            from pages.webview.browse import Browse
            browse = Browse(self.driver, self.page.base_url, self.page.timeout)
            return browse.wait_for_page_to_load()

        def click_about_us(self):
            self.find_element(*self._about_us_locator).click()
            from pages.webview.about_us import AboutUs
            about_us = AboutUs(self.driver, self.page.base_url, self.page.timeout)
            return about_us.wait_for_page_to_load()
