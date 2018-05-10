# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pypom

from selenium.webdriver.common.by import By


class Page(pypom.Page):

    _REGION_CONTENT_LOCATOR_ = (By.ID, 'region-content')
    _MY_ACCOUNT_LOCATOR_ = (By.CSS_SELECTOR, '#portlet-login, #portlet-loggedin')

    def __init__(self, driver, base_url, timeout=15):
        super().__init__(driver, base_url, timeout)

    @property
    def my_account(self):
        return MyAccount(self, self.find_element(*self._MY_ACCOUNT_LOCATOR_))

    @property
    def can_logout(self):
        return self.my_account.can_logout

    @property
    def has_username(self):
        return self.my_account.has_username

    @property
    def username(self):
        return self.my_account.username

    def logout(self):
        return self.my_account.logout()

    @property
    def loaded(self):
        return self.is_element_displayed(*self._REGION_CONTENT_LOCATOR_)

    # Backported from PyPOM 2.0.0. Remove when upgrading to PyPOM 2.0.0+
    def wait_for_page_to_load(self):
        """Wait for the page to load."""
        self.wait.until(lambda _: self.loaded)
        return super().wait_for_page_to_load()


class PublicPage(Page):

    @property
    def can_login(self):
        return self.my_account.can_login

    def login(self, username, password):
        return self.my_account.login(username, password)


class PrivatePage(Page):

    # These pages require you to be logged in already
    @property
    def can_login(self):
        return False

    @property
    def loaded(self):
        return super().loaded and self.has_username and self.can_logout


class Region(pypom.Region):

    # Backported from PyPOM 2.0.0. Remove when upgrading to PyPOM 2.0.0+
    @property
    def loaded(self):
        return True

    # Backported from PyPOM 2.0.0. Remove when upgrading to PyPOM 2.0.0+
    def wait_for_region_to_load(self):
        """Wait for the page to load."""
        self.wait.until(lambda _: self.loaded)
        return super().wait_for_region_to_load()


# Cyclic import has to be at the end of the file
from pages.legacy.my_account import MyAccount # noqa
