# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from regions.legacy.content import Content

from selenium.webdriver.common.by import By


class Collection(Content):

    _add_subcollections_link_locator = (By.CSS_SELECTOR, 'a.action_collection_subcollection')
    _add_modules_link_locator = (By.CSS_SELECTOR, 'a.action_collection_module')

    @property
    def is_empty(self):
        return not self.is_element_present(*self._content_node_locator)

    @property
    def content_nodes(self):
        return self.find_elements(*self._content_node_locator)

    def add_subcollections(self):
        self.hover().find_element(*self._add_subcollections_link_locator).click()
        from regions.legacy.add_subcollections import AddSubcollections
        add_subcollections = AddSubcollections(self, self.page.modal)
        return add_subcollections.wait_for_region_to_load()

    def add_modules(self):
        self.hover().find_element(*self._add_modules_link_locator).click()
        from regions.legacy.add_modules import AddModules
        add_modules = AddModules(self, self.page.modal)
        return add_modules.wait_for_region_to_load()
