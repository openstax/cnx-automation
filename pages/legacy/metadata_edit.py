# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class MetadataEdit(PrivatePage):
    _metadata_form_locator = (By.CSS_SELECTOR, 'form[action="content_title"]')
    _title_field_locator = (By.CSS_SELECTOR, 'input[type="text"][name="title"]')
    _collection_subtype_select_locator = (By.ID, 'collectionType')
    _submit_button_locator = (By.CSS_SELECTOR, 'input[type="submit"][name="form.button.next"]')

    @property
    def metadata_form(self):
        return self.find_element(*self._metadata_form_locator)

    @property
    def title_field(self):
        return self.metadata_form.find_element(*self._title_field_locator)

    @property
    def submit_button(self):
        return self.metadata_form.find_element(*self._submit_button_locator)

    @property
    def is_collection(self):
        return self.is_element_present(*self._collection_subtype_select_locator)

    @property
    def is_module(self):
        return not self.is_collection

    def fill_in_title(self, title):
        self.title_field.clear()
        self.title_field.send_keys(title)
        return self

    def submit(self, max_retries=3):
        is_collection = self.is_collection

        # Unlike the other forms, we actually have to click the submit button here
        # when creating the module, otherwise we end up in the wrong page (metadata edit page)
        self.submit_button.click()

        if is_collection:
            from pages.legacy.collection_edit import CollectionEdit
            edit = CollectionEdit(self.driver, self.base_url, self.timeout)
        else:
            from pages.legacy.module_edit import ModuleEdit
            edit = ModuleEdit(self.driver, self.base_url, self.timeout)

        return edit.wait_for_page_to_load()
