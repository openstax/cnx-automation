# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import xml.etree.ElementTree as ET

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ModuleEdit(PrivatePage):

    URL_TEMPLATE = '/Members/{username}/{module_id}'

    _blank_module_content_string = (
        '<ns0:content xmlns:ns0="http://cnx.rice.edu/cnxml">\n  '
        '<ns0:para id="delete_me">\n     \n  </ns0:para>\n</ns0:content>\n\n')

    _title_header_locator = (By.CSS_SELECTOR, '#content div div h1')

    _publish_link_locator = (By.CSS_SELECTOR, 'a[href$="module_publish"]')

    _import_form_locator = (By.CSS_SELECTOR, 'form[action="module_import_form"]')
    _import_select_locator = (By.CSS_SELECTOR, 'select[name="format"]')

    _content_textarea_locator = (By.ID, 'textarea')

    @property
    def username(self):
        return re.search('/Members/([^/]+)/([^/]+)', self.driver.current_url).group(1)

    @property
    def id(self):
        return re.search('/Members/([^/]+)/([^/]+)', self.driver.current_url).group(2)

    @property
    def title_header(self):
        return self.find_element(*self._title_header_locator)

    @property
    def title(self):
        import re
        return re.sub('^Module: ', '', self.title_header.text)

    @property
    def publish_link(self):
        return self.find_element(*self._publish_link_locator)

    @property
    def import_form(self):
        return self.find_element(*self._import_form_locator)

    @property
    def import_select(self):
        return self.import_form.find_element(*self._import_select_locator)

    @property
    def content_textarea(self):
        return self.find_element(*self._content_textarea_locator)

    @property
    def content(self):
        return ET.fromstring(self.content_textarea.get_attribute('value')).find(
            '{http://cnx.rice.edu/cnxml}content')

    @property
    def content_string(self):
        return ET.tostring(self.content, encoding='unicode')

    @property
    def blank(self):
        return self.content_string == self._blank_module_content_string

    @property
    def loaded(self):
        return (super().loaded and
                self.is_element_displayed(*self._title_header_locator) and
                self.is_element_displayed(*self._import_form_locator) and
                self.is_element_displayed(*self._publish_link_locator) and
                self.is_element_present(*self._content_textarea_locator))

    def publish(self):
        self.publish_link.click()
        from pages.legacy.module_publish import ModulePublish
        module_publish = ModulePublish(self.driver, self.base_url, self.timeout)
        return module_publish.wait_for_page_to_load()

    def import_select_option(self, format):
        css_selector = 'option[value="{format}"]'.format(format=format)
        return self.import_select.find_element(By.CSS_SELECTOR, css_selector)

    def select_import_format(self, format):
        self.import_select_option(format).click()
        return self

    def click_import(self):
        self.import_form.submit()
        from pages.legacy.module_import import ModuleImport
        module_import = ModuleImport(self.driver, self.base_url, self.timeout)
        return module_import.wait_for_page_to_load()
