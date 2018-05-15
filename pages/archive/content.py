# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.archive.base import Page

from selenium.webdriver.common.by import By


class Content(Page):

    URL_TEMPLATE = '/contents/{uuid_and_version}.json'

    # The browser automatically wraps the JSON response in some HTML
    _json_locator = (By.TAG_NAME, 'pre')

    @property
    def json_pre(self):
        return self.find_element(*self._json_locator)

    @property
    def json_text(self):
        return self.json_pre.text

    @property
    def json(self):
        import json
        return json.loads(self.json_text)

    @property
    def id(self):
        return self.json['id']

    @property
    def title(self):
        return self.json['title']

    @property
    def content(self):
        return self.json['content']

    @property
    def loaded(self):
        return super().loaded and self.is_element_displayed(*self._json_locator)
