# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pypom
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from regions.webview.base import Region

from time import sleep


class Page(pypom.Page):
    _canonical_link_locator = (By.CSS_SELECTOR, 'head link[rel="canonical"]')

    # Default to a 60 second timeout for CNX webview
    def __init__(self, driver, base_url=None, timeout=60, **url_kwargs):
        super().__init__(driver, base_url, timeout, **url_kwargs)

    @property
    def canonical_link(self):
        return self.find_element(*self._canonical_link_locator)

    @property
    def canonical_url(self):
        return self.canonical_link.get_attribute('href')

    @property
    def header(self):
        # Need to wait for the header to display because the nav menu initially loads with 0 height
        return self.Header(self).wait_for_region_to_display()

    @property
    def footer(self):
        return self.Footer(self)

    @property
    def active_element(self):
        return self.driver.switch_to.active_element

    def wait_for_region_to_display(self, region):
        self.wait.until(lambda _: region.is_displayed)
        return self

    def wait_for_element_to_display(self, element):
        self.wait.until(lambda _: element.is_displayed())
        return self

    def scroll_down(self):
        """Scrolls using page down once. Returns the active element."""
        active_element = self.active_element
        active_element.send_keys(Keys.PAGE_DOWN)
        return active_element

    def scroll_up(self):
        """Scrolls using page up once. Returns the active element."""
        active_element = self.active_element
        active_element.send_keys(Keys.PAGE_UP)
        return active_element

    def scroll_to(self, element=None):
        """Scrolls to the given element. Returns the element."""
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_to_element(element).perform()
        return element

    def offscreen_click(self, element):
        """Clicks an offscreen element.

        Clicks the given element, even if it is offscreen, by sending the ENTER key.
        Returns the element.
        """
        # We actually navigate using the ENTER key because scrolling the page can be flaky
        # https://stackoverflow.com/a/39918249
        element.send_keys(Keys.ENTER)
        return element

    def get_window_size(self, dimension=None):
        """Return the current window dimensions."""
        get_size = self.driver.get_window_size()
        if not dimension:
            return get_size
        if dimension not in get_size:
            raise IndexError('Unknown dimension: %s' % dimension)
        return get_size[dimension]

    def set_window_size(self, width=0, height=0):
        """Attempt to change the browser window size."""
        if width >= 1 and height >= 1:
            self.driver.set_window_size(width, height)
            sleep(1.0)

    def set_window_position(self, x_=0, y_=0):
        """Move the browser window anchor."""
        if x_ >= 0 and y_ >= 0:
            self.driver.set_window_position(x_, y_)
            sleep(1.0)

    def refresh(self):
        """Refresh the current page"""
        self.driver.refresh()

    class Header(Region):
        _root_locator = (By.CSS_SELECTOR, 'header#header div.page-header')
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

    class Footer(Region):
        _root_locator = (By.CSS_SELECTOR, 'footer.footer div.page-footer')
        _licensing_link_locator = (By.CSS_SELECTOR, 'a[data-l10n-id="all-footer-licensing"]')
        _terms_of_use_link_locator = (By.CSS_SELECTOR, 'a[data-l10n-id="all-footer-terms-of-use"]')
        _accessibility_statement_link_locator = (By.CSS_SELECTOR,
                                                 'a[data-l10n-id="all-footer-accessibility"]')
        _contact_link_locator = (By.CSS_SELECTOR, 'a[data-l10n-id="all-footer-contact"]')
        _foundation_support_paragraph_locator = (
            By.CSS_SELECTOR, 'div[data-l10n-id="all-footer-support"]')
        _ap_paragraph_locator = (By.CSS_SELECTOR, 'div[data-l10n-id="all-footer-ap"]')
        _copyright_statement_paragraph_locator = (
            By.XPATH, ".//div[.//span[@data-l10n-id='all-footer-creative-commons']]")
        _android_app_link_locator = (
            By.CSS_SELECTOR, 'section.connect ul li a[data-l10n-id="all-footer-android-app"]')
        _facebook_link_locator = (
            By.XPATH, (".//section[contains(@class, 'share')]"
                       "//ul//li//a[.//span[contains(@class, 'facebook')]]"))
        _twitter_link_locator = (
            By.XPATH, (".//section[contains(@class, 'share')]"
                       "//ul//li//a[.//span[contains(@class, 'twitter')]]"))
        _email_link_locator = (
            By.XPATH, (".//section[contains(@class, 'share')]"
                       "//ul//li//a[.//span[contains(@class, 'mail')]]"))

        @property
        def is_licensing_link_displayed(self):
            return self.is_element_displayed(*self._licensing_link_locator)

        @property
        def licensing_link(self):
            return self.find_element(*self._licensing_link_locator)

        @property
        def licensing_url(self):
            return self.licensing_link.get_attribute('href')

        @property
        def is_terms_of_use_link_displayed(self):
            return self.is_element_displayed(*self._terms_of_use_link_locator)

        @property
        def terms_of_use_link(self):
            return self.find_element(*self._terms_of_use_link_locator)

        @property
        def terms_of_use_url(self):
            return self.terms_of_use_link.get_attribute('href')

        @property
        def is_accessibility_statement_link_displayed(self):
            return self.is_element_displayed(*self._accessibility_statement_link_locator)

        @property
        def accessibility_statement_link(self):
            return self.find_element(*self._accessibility_statement_link_locator)

        @property
        def accessibility_statement_url(self):
            return self.accessibility_statement_link.get_attribute('href')

        @property
        def is_contact_link_displayed(self):
            return self.is_element_displayed(*self._contact_link_locator)

        @property
        def contact_link(self):
            return self.find_element(*self._contact_link_locator)

        @property
        def contact_url(self):
            return self.contact_link.get_attribute('href')

        @property
        def is_foundation_support_paragraph_displayed(self):
            return self.is_element_displayed(*self._foundation_support_paragraph_locator)

        @property
        def foundation_support_paragraph(self):
            return self.find_element(*self._foundation_support_paragraph_locator)

        @property
        def foundation_support_text(self):
            return self.foundation_support_paragraph.text

        @property
        def is_ap_paragraph_displayed(self):
            return self.is_element_displayed(*self._ap_paragraph_locator)

        @property
        def ap_paragraph(self):
            return self.find_element(*self._ap_paragraph_locator)

        @property
        def ap_text(self):
            return self.ap_paragraph.text

        @property
        def is_copyright_statement_paragraph_displayed(self):
            return self.is_element_displayed(*self._copyright_statement_paragraph_locator)

        @property
        def copyright_statement_paragraph(self):
            return self.find_element(*self._copyright_statement_paragraph_locator)

        @property
        def copyright_statement_text(self):
            return self.copyright_statement_paragraph.text

        @property
        def is_android_app_link_displayed(self):
            return self.is_element_displayed(*self._android_app_link_locator)

        @property
        def android_app_link(self):
            return self.find_element(*self._android_app_link_locator)

        @property
        def android_app_url(self):
            return self.android_app_link.get_attribute('href')

        @property
        def is_facebook_link_displayed(self):
            return self.is_element_displayed(*self._facebook_link_locator)

        @property
        def facebook_link(self):
            return self.find_element(*self._facebook_link_locator)

        @property
        def facebook_url(self):
            return self.facebook_link.get_attribute('href')

        @property
        def is_twitter_link_displayed(self):
            return self.is_element_displayed(*self._twitter_link_locator)

        @property
        def twitter_link(self):
            return self.find_element(*self._twitter_link_locator)

        @property
        def twitter_url(self):
            return self.twitter_link.get_attribute('href')

        @property
        def is_email_link_displayed(self):
            return self.is_element_displayed(*self._email_link_locator)

        @property
        def email_link(self):
            return self.find_element(*self._email_link_locator)

        @property
        def email_url(self):
            return self.email_link.get_attribute('href')
