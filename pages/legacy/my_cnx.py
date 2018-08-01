# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class MyCnx(PrivatePage):
    URL_TEMPLATE = '/mycnx'
    _create_a_new_module_locator = (
        By.CSS_SELECTOR, 'p.createlink a[href$="/mydashboard/cc_license?type_name=Module"')
    _create_a_new_collection_locator = (
        By.CSS_SELECTOR, 'p.createlink a[href$="/mydashboard/cc_license?type_name=Collection"')
    _workspace_link_locator = (By.CSS_SELECTOR, '#cnx_by_location_contents li a')
    _go_to_collections_link_locator = (By.CSS_SELECTOR, '#cnx_by_type_contents > '
                                                        'li:nth-child(2) > a')

    @property
    def create_a_new_collection_link(self):
        return self.find_element(*self._create_a_new_collection_locator)

    @property
    def create_a_new_module_link(self):
        return self.find_element(*self._create_a_new_module_locator)

    @property
    def go_to_collections_link(self):
        return self.find_element(*self._go_to_collections_link_locator)

    @property
    def workspace_link(self):
        return self.find_element(*self._workspace_link_locator)

    def create_collection(self):
        self.create_a_new_collection_link.click()
        from pages.legacy.cc_license import CcLicense
        cc_license = CcLicense(self.driver, self.base_url, self.timeout)
        return cc_license.wait_for_page_to_load()

    def create_module(self):
        self.create_a_new_module_link.click()
        from pages.legacy.cc_license import CcLicense
        cc_license = CcLicense(self.driver, self.base_url, self.timeout)
        return cc_license.wait_for_page_to_load()

    def workspace(self):
        self.workspace_link.click()
        from pages.legacy.workspace import Workspace
        workspace = Workspace(self.driver, self.base_url, self.timeout)
        return workspace.wait_for_page_to_load()

    def workspace_collection(self):
        self.go_to_collections_link.click()
        from pages.legacy.workspace_collection import WorkspaceCollection
        collections = WorkspaceCollection(self.driver, self.base_url, self.timeout)
        return collections.wait_for_page_to_load()
