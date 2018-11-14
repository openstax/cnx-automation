# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class Workspace(PrivatePage):
    _select_all_checkbox_locator = (By.CSS_SELECTOR, 'input[type="checkbox"][name="selectButton"]')
    _remove_button_locator = (By.CSS_SELECTOR, 'input[type="submit"][value="Remove"]')

    @property
    def has_content(self):
        return self.is_element_displayed(*self._select_all_checkbox_locator)

    @property
    def select_all_checkbox(self):
        return self.find_element(*self._select_all_checkbox_locator)

    @property
    def remove_button(self):
        return self.find_element(*self._remove_button_locator)

    def select_all(self):
        self.select_all_checkbox.click()
        return self

    def remove(self):
        self.remove_button.click()
        from pages.legacy.confirm_remove import ConfirmRemove

        confirm_remove = ConfirmRemove(self.driver, self.base_url, self.timeout)
        return confirm_remove.wait_for_page_to_load()
