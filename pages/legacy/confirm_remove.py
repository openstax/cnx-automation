# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ConfirmRemove(PrivatePage):

    _form_locator = (By.CSS_SELECTOR, 'form[action="folder_delete_confirm"]')
    _remove_button_locator = (By.CSS_SELECTOR, 'input[type="submit"][name="form.button.delete"]')

    @property
    def form(self):
        return self.find_element(*self._form_locator)

    @property
    def remove_button(self):
        return self.form.find_element(*self._remove_button_locator)

    def confirm(self):
        self.remove_button.click()
        from pages.legacy.workspace import Workspace
        workspace = Workspace(self.driver, self.base_url, self.timeout)
        return workspace.wait_for_page_to_load()
