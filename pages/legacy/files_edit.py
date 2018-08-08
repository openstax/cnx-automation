# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.legacy.base import PrivatePage
from regions.legacy.base import Region


class FilesEdit(PrivatePage):
    _add_new_file_locator = (By.ID, 'add_new_file')

    @property
    def add_new_file(self):
        return self.FileUpload(self, self.find_element(*self._add_new_file_locator))

    class FileUpload(Region):
        _choose_file_locator = (By.ID, 'file')
        _upload_locator = (By.CSS_SELECTOR, '[name="form.button.Save"]')

        def choose_file(self, filepath):
            return self.find_element(*self._choose_file_locator).send_keys(filepath)

        def click_upload(self):
            return self.find_element(*self._upload_locator).click()
