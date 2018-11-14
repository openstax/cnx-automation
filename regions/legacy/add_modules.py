# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from regions.legacy.base import Region


class AddModules(Region):
    _search_form_locator = (By.ID, "collection-composer-collection-module-form-search")
    _words_field_locator = (By.CSS_SELECTOR, 'input[type="text"][name="words"]')
    _spinner_locator = (By.ID, "kss-spinner")

    def __init__(self, collection, root=None):
        self.collection = collection
        super().__init__(collection.page, root)

    @property
    def search_form(self):
        return self.find_element(*self._search_form_locator)

    @property
    def words_field(self):
        return self.search_form.find_element(*self._words_field_locator)

    # We need this check because this region is actually loaded via javascript
    @property
    def loaded(self):
        return self.is_element_displayed(
            *self._search_form_locator
        ) and not self.is_element_displayed(*self._spinner_locator)

    # Overridden so it doesn't return true as soon as the spinner appears
    @property
    def unloaded(self):
        return not self.is_element_displayed(
            *self._search_form_locator
        ) and not self.is_element_displayed(*self._spinner_locator)

    def fill_in_search_words(self, words):
        self.words_field.send_keys(words)
        return self

    def submit_search(self):
        self.search_form.submit()
        from regions.legacy.add_modules_with_search_results import AddModulesWithSearchResults

        search_results = AddModulesWithSearchResults(self.collection, self.root)
        return search_results.wait_for_region_to_load()
