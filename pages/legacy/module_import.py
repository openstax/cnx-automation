# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from selenium.webdriver.common.keys import Keys

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ModuleImport(PrivatePage):
    _import_form_locator = (By.CSS_SELECTOR, 'form[action="module_import_form"][name="import"]')
    _import_file_field_locator = (By.CSS_SELECTOR, 'input[type="file"][name="importFile"]')
    _import_submit_button_locator = (
        By.CSS_SELECTOR,
        "#region-content > div > div > form > input.context.uploadButton",
    )

    @property
    def import_form(self):
        return self.find_element(*self._import_form_locator)

    @property
    def import_file_field(self):
        return self.import_form.find_element(*self._import_file_field_locator)

    def fill_in_filename(self, filename):
        self.import_file_field.send_keys(filename)
        return self

    @property
    def submit_button(self):
        return self.find_element(*self._import_submit_button_locator)

    def submit(self):
        self.submit_button.click()
        from pages.legacy.module_edit import ModuleEdit

        module_edit = ModuleEdit(self.driver, self.base_url, self.timeout)
        return module_edit.wait_for_page_to_load()
