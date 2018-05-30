# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class CcLicense(PrivatePage):
    _cc_license_form_locator = (By.CSS_SELECTOR, 'form[action="cc_license"]')
    _agree_checkbox_locator = (By.CSS_SELECTOR, 'input[type="checkbox"][name="agree"]')

    @property
    def cc_license_form(self):
        return self.find_element(*self._cc_license_form_locator)

    @property
    def agree_checkbox(self):
        return self.cc_license_form.find_element(*self._agree_checkbox_locator)

    def agree(self):
        self.agree_checkbox.click()
        return self

    def submit(self):
        self.cc_license_form.submit()
        from pages.legacy.module_metadata import ModuleMetadata
        module_metadata = ModuleMetadata(self.driver, self.base_url, self.timeout)
        return module_metadata.wait_for_page_to_load()
