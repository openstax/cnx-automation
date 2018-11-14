# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from regions.legacy.base import Region


class AddSubcollections(Region):

    _form_locator = (By.ID, "collection-composer-collection-subcollection-form")
    _titles_field_locator = (By.CSS_SELECTOR, 'textarea[name="titles"]')

    def __init__(self, collection, root=None):
        self.collection = collection
        super().__init__(collection.page, root)

    @property
    def form(self):
        return self.find_element(*self._form_locator)

    @property
    def titles_field(self):
        return self.form.find_element(*self._titles_field_locator)

    # We need this check because this region is actually loaded via javascript
    @property
    def loaded(self):
        return self.is_element_displayed(*self._form_locator)

    def fill_in_titles(self, titles):
        self.titles_field.send_keys(titles)
        return self

    # Returns the last subcollection added
    def submit(self):
        self.form.submit()
        # Wait for the modal to close
        self.wait_for_region_to_unload()
        from regions.legacy.collection import Collection

        collection = Collection(self.page, self.collection.content_nodes[-1])
        return collection.wait_for_region_to_load()
