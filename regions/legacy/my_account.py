# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from regions.legacy.base import Region
from pages.legacy.my_dashboard import MyDashboard
from pages.legacy.login_form import LoginForm


class MyAccount(Region):

    _LOGIN_FORM_LOCATOR_ = (By.CSS_SELECTOR, 'form[action$="login_form"]')
    _USERNAME_FIELD_LOCATOR_ = (By.ID, '__ac_name')
    _PASSWORD_FIELD_LOCATOR_ = (By.ID, '__ac_password')

    _USERNAME_SPAN_LOCATOR_ = (By.ID, 'user-name')
    _LOGOUT_FORM_LOCATOR_ = (By.CSS_SELECTOR, 'form[action$="logout"]')

    @property
    def can_login(self):
        return self.is_element_displayed(*self._LOGIN_FORM_LOCATOR_) and \
               self.is_element_displayed(*self._USERNAME_FIELD_LOCATOR_) and \
               self.is_element_displayed(*self._PASSWORD_FIELD_LOCATOR_)

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
    def has_username(self):
        return self.is_element_displayed(*self._USERNAME_SPAN_LOCATOR_)

    @property
    def username_span(self):
        return self.find_element(*self._USERNAME_SPAN_LOCATOR_)

    @property
    def username(self):
        return self.username_span.text if self.has_username else None

    @property
    def can_logout(self):
        return self.is_element_displayed(*self._LOGOUT_FORM_LOCATOR_)

    @property
    def logout_form(self):
        return self.find_element(*self._LOGOUT_FORM_LOCATOR_)

    @property
    def loaded(self):
        return self.can_login or (self.has_username and self.can_logout)

    def login(self, username, password):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.login_form.submit()
        my_dashboard = MyDashboard(self.page.driver, self.page.base_url, self.page.timeout)
        return my_dashboard.wait_for_page_to_load()

    def logout(self):
        self.logout_form.submit()
        login_form = LoginForm(self.page.driver, self.page.base_url, self.page.timeout)
        return login_form.wait_for_page_to_load()
