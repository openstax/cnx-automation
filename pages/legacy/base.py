# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pypom

from selenium.webdriver.common.by import By


class Page(pypom.Page):
    _region_content_locator = (By.ID, 'region-content')
    _my_account_locator = (By.CSS_SELECTOR, '#portlet-login, #portlet-loggedin')

    # Default to a 30 second timeout for CNX legacy
    def __init__(self, driver, base_url=None, timeout=60, **url_kwargs):
        super().__init__(driver, base_url, timeout, **url_kwargs)

    @property
    def my_account(self):
        from regions.legacy.my_account import MyAccount
        return MyAccount(self, self.find_element(*self._my_account_locator))

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
