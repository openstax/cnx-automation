# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from regions.legacy.add_modules import AddModules


class AddModulesWithSearchResults(AddModules):
    _form_locator = (By.ID, 'collection_composer')
    _add_workarea_checkbox_locator = (By.CSS_SELECTOR,
                                      'input[type="checkbox"][name="selectButton"]')

    @property
    def form(self):
        return self.find_element(*self._form_locator)

    @property
    def add_workarea_checkbox(self):
        return self.form.find_element(*self._add_workarea_checkbox_locator)

    # This is a separate `loaded` method for when performing the search (more fields show up)
    # Necessary because without waiting for the new elements we were getting StaleElementErrors
    @property
    def loaded(self):
        return ((self.is_element_displayed(*self._add_workarea_checkbox_locator) or
                 'No results matched your query' in self.text) and
                super().loaded)

    def add_workarea(self):
        self.add_workarea_checkbox.click()
        return self

    # Returns the last module added
    def submit(self):
        self.form.submit()
        # Wait for the modal to close
        self.wait_for_region_to_unload()
        from regions.legacy.module import Module
        module = Module(self.page, self.collection.content_nodes[-1])
        return module.wait_for_region_to_load()
