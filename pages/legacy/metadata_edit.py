# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

from pages.legacy.base import PrivatePage


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

    def submit(self, max_attempts=3):
        if self.is_collection:
            from pages.legacy.collection_edit import CollectionEdit
            edit = CollectionEdit(self.driver, self.base_url, self.timeout)
        else:
            from pages.legacy.module_edit import ModuleEdit
            edit = ModuleEdit(self.driver, self.base_url, self.timeout)

        # Unlike the other forms, we actually have to click the submit button here
        # when creating the module, otherwise we end up in the wrong page (metadata edit page)
        self.submit_button.click()

        for i in range(max_attempts):
            try:
                edit = edit.wait_for_page_to_load()

                if not edit.has_site_error:
                    return edit
                elif i < max_attempts - 1:
                    # Sometimes creating a module or collection fails with a SiteError
                    # In those cases, we retry creating them a few times
                    self.driver.back()
                    self = self.wait_for_page_to_load()
                    self.submit_button.click()
            except UnexpectedAlertPresentException:
                # When creating a module or collection we sometimes get an error alert
                # In that case we dismiss it, which causes the page to actually load, and wait
                if i < max_attempts - 1:
                    self.driver.switch_to.alert.dismiss()

        from pytest import fail
        fail('Maximum number of attempts exceeded for metadata form submission'
             ' ({attempts})'.format(attempts=max_attempts))
