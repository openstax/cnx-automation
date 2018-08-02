# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage
from regions.webview.base import Region

from selenium.webdriver.common.by import By


class WorkspaceCollection(PrivatePage):
    _select_all_checkbox_locator = (By.CSS_SELECTOR, 'input[type="checkbox"][name="selectButton"]')
    _remove_button_locator = (By.CSS_SELECTOR, 'input[type="context"][value="Remove"]')
    _collection_locator = (By.CSS_SELECTOR, 'tr.odd, tr.even')

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
        from pages.legacy.collections_confirm_remove import CollectionsConfirmRemove
        confirm_remove = CollectionsConfirmRemove(self.driver, self.base_url, self.timeout)
        return confirm_remove.wait_for_page_to_load()

    @property
    def collection_list(self):
        return [self.WorkspaceCollectionEdit(self, el) for el in
                self.find_elements(*self._collection_locator)]

    class WorkspaceCollectionEdit(Region):
        _link_locator = (By.CLASS_NAME, 'contenttype-collection')

        @property
        def click_collection_link(self):
            self.find_element(*self._link_locator).click()
            from pages.legacy.collection_edit import CollectionEdit
            return CollectionEdit(self.driver, self.page.base_url,
                                  self.page.timeout).wait_for_page_to_load()
