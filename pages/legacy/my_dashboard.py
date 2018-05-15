# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class MyDashboard(PrivatePage):

    URL_TEMPLATE = '/mydashboard'

    _create_a_new_module_locator = (By.CSS_SELECTOR, 'p.createlink a')
    _last_modified_module_link_locator = (By.CSS_SELECTOR, '#lastmodified ul.latest li.module a')

    @property
    def create_a_new_module_link(self):
        return self.find_element(*self._create_a_new_module_locator)

    @property
    def last_modified_module_link(self):
        return self.find_element(*self._last_modified_module_link_locator)

    @property
    def last_modified_module_title(self):
        return self.last_modified_module_link.text

    @property
    def loaded(self):
        return super().loaded and self.is_element_displayed(*self._create_a_new_module_locator)

    def create_module(self):
        self.create_a_new_module_link.click()
        from pages.legacy.cc_license import CcLicense
        cc_license = CcLicense(self.driver, self.base_url, self.timeout)
        return cc_license.wait_for_page_to_load()

    def edit_last_modified_module(self):
        self.last_modified_module_link.click()
        from pages.legacy.module_edit import ModuleEdit
        module_edit = ModuleEdit(self.driver, self.base_url, self.timeout)
        return module_edit.wait_for_page_to_load()
