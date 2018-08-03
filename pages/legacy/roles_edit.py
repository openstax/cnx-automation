# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.legacy.base import PrivatePage
from regions.webview.base import Region


class RolesEdit(PrivatePage):
    _role_form_locator = (By.CSS_SELECTOR, 'form[name="people"]')
    _form_title_locator = (By.CSS_SELECTOR, 'h4')
    _submit_button_locator = (By.CSS_SELECTOR, 'input[type="submit"][name="form.button.update"]')
    _author_locator = (By.CSS_SELECTOR, 'tr.even, tr.odd')

    @property
    def role_form(self):
        return self.find_element(*self._role_form_locator)

    @property
    def form_title(self):
        return self.role_form.find_element(*self._form_title_locator)

    @property
    def submit_button(self):
        return self.role_form.find_element(*self._submit_button_locator)

    @property
    def author_list(self):
        return [self.AuthorEdit(self, el) for el in self.find_elements(*self._author_locator)]

    class AuthorEdit(Region):
        _name_locator = (By.CSS_SELECTOR, 'td > strong')
        _id_locator = (By.CSS_SELECTOR, 'td:nth-child(3) > a')
        _order_control_locator = (By.CSS_SELECTOR, 'td:nth-child(1)')

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        @property
        def id(self):
            return self.find_element(*self._id_locator).text

        @property
        def order_control(self):
            return self.Order(self, self.find_element(*self._order_control_locator))

        class Order(Region):
            _top_locator = (By.CSS_SELECTOR, 'a:nth-child(1)')
            _move_item_up_locator = (By.CSS_SELECTOR, 'a:nth-child(2)')
            _move_item_down_locator = (By.CSS_SELECTOR, 'a:nth-child(3)')
            _bottom_locator = (By.CSS_SELECTOR, 'a:nth-child(4)')

            def click_top(self):
                self.find_element(*self._top_locator).click()

            def click_move_item_up(self):
                self.find_element(*self._move_item_up_locator).click()

            def click_move_item_down(self):
                self.find_element(*self._move_item_down_locator).click()

            def click_bottom(self):
                self.find_element(*self._bottom_locator).click()
