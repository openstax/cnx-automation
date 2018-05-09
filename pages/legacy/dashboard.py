# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.legacy.base import Base

# Cyclic import
import pages.legacy.login_page


class Dashboard(Base):

    _USERNAME_SPAN_LOCATOR_ = (By.ID, 'user-name')
    _LOGOUT_FORM_LOCATOR_ = (By.CSS_SELECTOR, 'form[action$="logout"]')

    @property
    def username_span(self):
        return self.find_element(*self._USERNAME_SPAN_LOCATOR_)

    @property
    def username(self):
        return self.username_span.text

    @property
    def logout_form(self):
        return self.find_element(*self._LOGOUT_FORM_LOCATOR_)

    @property
    def loaded(self):
        return self.is_element_displayed(*self._USERNAME_SPAN_LOCATOR_) and \
               self.is_element_displayed(*self._LOGOUT_FORM_LOCATOR_)

    def logout(self):
        self.logout_form.submit()
        login_page = pages.legacy.login_page.LoginPage(self.driver,
                                                       self.base_url,
                                                       self.timeout)
        return login_page.wait_for_page_to_load()
