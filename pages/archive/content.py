# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from functools import lru_cache

from pages.archive.base import Page

from selenium.webdriver.common.by import By


class Content(Page):

    URL_TEMPLATE = '/contents/{uuid_and_version}.json'

    # The browser automatically wraps the JSON response in some HTML
    _json_locator = (By.TAG_NAME, 'pre')

    _stable_fields = [
        'googleAnalytics',
        'version',
        'submitlog',
        'abstract',
        'printStyle',
        'roles',
        'keywords',
        'title',
        'mediaType',
        'subjects',
        'publishers',
        'stateid',
        'authors',
        'parentVersion',
        'legacy_version',
        'licensors',
        'language',
        'license',
        'doctype',
        'buyLink',
        'submitter',
        'baked',
        'parentAuthors'
    ]

    @property
    def json_pre(self):
        return self.find_element(*self._json_locator)

    @property
    def json_text(self):
        return self.json_pre.text

    @property
    @lru_cache(maxsize=None)
    def dict(self):
        import json
        return json.loads(self.json_text)

    @property
    def id(self):
        return self.dict['id']

    @property
    def title(self):
        return self.dict['title']

    @property
    def content(self):
        return self.dict['content']

    @property
    def stable_content(self):
        import xml.etree.ElementTree as ET

        html = ET.fromstring(self.content)

        head = html.find('{http://www.w3.org/1999/xhtml}head')

        # Remove creation time
        created_time = head.find('./{http://www.w3.org/1999/xhtml}meta[@name="created-time"]')
        head.remove(created_time)

        # Remove revision time
        revised_time = head.find('./{http://www.w3.org/1999/xhtml}meta[@name="revised-time"]')
        head.remove(revised_time)

        return ET.tostring(html, encoding='unicode')

    @property
    def stable_dict(self):
        return {**{field: self.dict[field] for field in self._stable_fields},
                **{'content': self.stable_content}}
