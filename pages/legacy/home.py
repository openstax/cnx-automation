# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.legacy.login_page import LoginPage


class Home(LoginPage):

    URL_TEMPLATE = None

    _LOGIN_FORM_LOCATOR_ = (By.CSS_SELECTOR, 'form[action$="login_form"]')

    @property
    def loaded(self):
        return self.is_element_displayed(*self._LOGIN_FORM_LOCATOR_)
