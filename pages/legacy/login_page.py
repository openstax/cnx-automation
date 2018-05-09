# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.legacy.base import Base

# Cyclic import
import pages.legacy.dashboard


class LoginPage(Base):

    URL_TEMPLATE = '/login_form'

    _LOGIN_FORM_LOCATOR_ = (By.ID, 'login_form')
    _USERNAME_FIELD_LOCATOR_ = (By.ID, '__ac_name')
    _PASSWORD_FIELD_LOCATOR_ = (By.ID, '__ac_password')

    @property
    def login_form(self):
        return self.find_element(*self._LOGIN_FORM_LOCATOR_)

    @property
    def username_field(self):
        return self.find_element(*self._USERNAME_FIELD_LOCATOR_)

    @property
    def password_field(self):
        return self.find_element(*self._PASSWORD_FIELD_LOCATOR_)

    @property
    def loaded(self):
        return self.is_element_displayed(*self._LOGIN_FORM_LOCATOR_) and \
               self.is_element_displayed(*self._USERNAME_FIELD_LOCATOR_) and \
               self.is_element_displayed(*self._PASSWORD_FIELD_LOCATOR_)

    def login(self, username, password):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.login_form.submit()
        dashboard = pages.legacy.dashboard.Dashboard(self.driver,
                                                     self.base_url,
                                                     self.timeout)
        return dashboard.wait_for_page_to_load()
