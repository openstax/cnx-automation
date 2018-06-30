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

    def wait_for_region_to_display(self, region):
        self.wait.until(lambda _: region.is_displayed)
        return self

    def wait_for_element_to_display(self, element):
        self.wait.until(lambda _: element.is_displayed())
        return self

    def scroll_to(self, element=None):
        """Scrolls to the given element. Returns the element."""
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_to_element(element).perform()
        return element

    def focus(self, element):
        """Focus (and scrolls to) the given element.

        Focus (and scrolls to) the given element.
        More reliable than scroll_to(), but can only be used on focusable elements.
        Returns the element.
        """
        element.send_keys('')
        return element

    def offscreen_click(self, element):
        """Clicks an offscreen element.

        Clicks the given element, even if it is offscreen, by sending the ENTER key.
        Returns the element.
        """
        # We actually navigate using the ENTER key because scrolling the page can be flaky
        # https://stackoverflow.com/a/39918249
        from selenium.webdriver.common.keys import Keys
        element.send_keys(Keys.ENTER)
        return element

    class Header(Region):
        _root_locator = (By.ID, 'header')
        _support_link_locator = (By.CSS_SELECTOR, 'a[data-l10n-id="all-header-support"]')
        _legacy_site_link_locator = (By.CSS_SELECTOR,
                                     'a[data-l10n-id="all-cnx-author-legacy-site"]')
        # This is the CSS selector that currently applies the CNX logo background-image
        _cnx_logo_locator = (
            By.CSS_SELECTOR,
            '.page-header > .navbar > .container-fluid > .navbar-header > .navbar-brand'
        )
        _nav_button_locator = (By.CSS_SELECTOR,
                               '#header button.navbar-toggle[data-target="#page-nav"]')
        _browse_link_locator = (By.CSS_SELECTOR, '#page-nav #nav-browse a')
        _about_us_link_locator = (By.CSS_SELECTOR, '#page-nav #nav-about a')
        _donate_link_locator = (By.CSS_SELECTOR, '#page-nav #nav-donate a')
        _rice_logo_locator = (By.XPATH, ".//a[.//img[@src='/images/rice.png']]")

        @property
        def support_link(self):
            return self.find_element(*self._support_link_locator)

        @property
        def is_support_link_displayed(self):
            return self.is_element_displayed(*self._support_link_locator)

        @property
        def support_url(self):
            return self.support_link.get_attribute('href')

        @property
        def legacy_site_link(self):
            return self.find_element(*self._legacy_site_link_locator)

        @property
        def is_legacy_site_link_displayed(self):
            return self.is_element_displayed(*self._legacy_site_link_locator)

        @property
        def legacy_site_url(self):
            return self.legacy_site_link.get_attribute('href')

        @property
        def cnx_logo(self):
            return self.find_element(*self._cnx_logo_locator)

        @property
        def is_cnx_logo_displayed(self):
            return self.is_element_displayed(*self._cnx_logo_locator)

        @property
        def cnx_logo_url(self):
            return self.cnx_logo.get_attribute('href')

        @property
        def nav_button(self):
            return self.find_element(*self._nav_button_locator)

        @property
        def is_nav_button_displayed(self):
            return self.is_element_displayed(*self._nav_button_locator)

        @property
        def browse_link(self):
            return self.find_element(*self._browse_link_locator)

        @property
        def is_browse_link_displayed(self):
            return self.is_element_displayed(*self._browse_link_locator)

        @property
        def browse_url(self):
            return self.browse_link.get_attribute('href')

        @property
        def about_us_link(self):
            return self.find_element(*self._about_us_link_locator)

        @property
        def is_about_us_link_displayed(self):
            return self.is_element_displayed(*self._about_us_link_locator)

        @property
        def about_us_url(self):
            return self.about_us_link.get_attribute('href')

        @property
        def donate_link(self):
            return self.find_element(*self._donate_link_locator)

        @property
        def is_donate_link_displayed(self):
            return self.is_element_displayed(*self._donate_link_locator)

        @property
        def donate_url(self):
            return self.donate_link.get_attribute('href')

        @property
        def are_nav_links_displayed(self):
            return (self.is_browse_link_displayed and
                    self.is_about_us_link_displayed and
                    self.is_donate_link_displayed)

        @property
        def is_nav_displayed(self):
            return self.is_nav_button_displayed or self.are_nav_links_displayed

        @property
        def rice_logo(self):
            return self.find_element(*self._rice_logo_locator)

        @property
        def is_rice_logo_displayed(self):
            return self.is_element_displayed(*self._rice_logo_locator)

        @property
        def rice_logo_url(self):
            return self.rice_logo.get_attribute('href')

        @property
        def is_displayed(self):
            return (self.is_support_link_displayed and
                    self.is_legacy_site_link_displayed and
                    self.is_cnx_logo_displayed and
                    self.is_nav_displayed)

        def wait_for_nav_links_to_display(self):
            self.wait.until(lambda _: self.are_nav_links_displayed)
            return self

        def click_cnx_logo(self):
            self.cnx_logo.click()
            from pages.webview.home import Home
            return Home(self.driver, self.page.base_url, self.page.timeout).wait_for_page_to_load()

        def click_nav_button(self):
            self.nav_button.click()
            return self.wait_for_nav_links_to_display()

        def click_search(self):
            self.find_element(*self._browse_link_locator).click()
            from pages.webview.browse import Browse
            browse = Browse(self.driver, self.page.base_url, self.page.timeout)
            return browse.wait_for_page_to_load()

        def click_about_us(self):
            self.find_element(*self._about_us_link_locator).click()
            from pages.webview.about_us import AboutUs
            about_us = AboutUs(self.driver, self.page.base_url, self.page.timeout)
            return about_us.wait_for_page_to_load()

        def click_donate(self):
            self.find_element(*self._donate_link_locator).click()
            from pages.webview.donate import Donate
            donate = Donate(self.driver, self.page.base_url, self.page.timeout)
            return donate.wait_for_page_to_load()
