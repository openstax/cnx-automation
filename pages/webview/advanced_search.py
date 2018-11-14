# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page


class AdvancedSearch(Page):
    URL_TEMPLATE = "/search"
    _form_locator = (By.CSS_SELECTOR, "#search div.search div.advanced form")
    _author_field_locator = (By.CSS_SELECTOR, 'input[type="text"][name="author"]')
    _title_field_locator = (By.CSS_SELECTOR, 'input[type="text"][name="title"]')
    _subject_select_locator = (By.CSS_SELECTOR, 'select[name="subject"]')
    _keywords_field_locator = (By.CSS_SELECTOR, 'input[type="text"][name="keywords"]')
    _type_select_locator = (By.CSS_SELECTOR, 'select[name="type"]')
    _language_select_locator = (By.CSS_SELECTOR, 'select[name="language"]')
    _language_option_locator = (By.CSS_SELECTOR, 'select[name="language"] option:not([value=""])')
    _publication_date_select_locator = (By.CSS_SELECTOR, 'select[name="pubYear"]')
    _sort_by_select_locator = (By.CSS_SELECTOR, 'select[name="sort"]')

    @property
    def form(self):
        return self.find_element(*self._form_locator)

    @property
    def author_field(self):
        return self.form.find_element(*self._author_field_locator)

    @property
    def title_field(self):
        return self.form.find_element(*self._title_field_locator)

    @property
    def subject_select(self):
        return self.form.find_element(*self._subject_select_locator)

    @property
    def keywords_field(self):
        return self.form.find_element(*self._keywords_field_locator)

    @property
    def type_select(self):
        return self.form.find_element(*self._type_select_locator)

    @property
    def language_select(self):
        return self.form.find_element(*self._language_select_locator)

    @property
    def publication_date_select(self):
        return self.form.find_element(*self._publication_date_select_locator)

    @property
    def sort_by_select(self):
        return self.form.find_element(*self._sort_by_select_locator)

    # The language list loads after everything else
    @property
    def loaded(self):
        return self.is_element_displayed(*self._language_option_locator)

    def fill_in_author(self, value):
        self.author_field.send_keys(value)
        return self

    def fill_in_title(self, value):
        self.title_field.send_keys(value)
        return self

    def subject_select_option(self, value):
        css_selector = 'option[value="{value}"]'.format(value=value)
        return self.subject_select.find_element(By.CSS_SELECTOR, css_selector)

    def select_subject(self, value):
        self.subject_select_option(value).click()
        return self

    def fill_in_keywords(self, value):
        self.keywords_field.send_keys(value)
        return self

    def type_select_option(self, value):
        css_selector = 'option[value="{value}"]'.format(value=value)
        return self.type_select.find_element(By.CSS_SELECTOR, css_selector)

    def select_type(self, value):
        self.type_select_option(value).click()
        return self

    def language_select_option(self, value):
        css_selector = 'option[value="{value}"]'.format(value=value)
        return self.language_select.find_element(By.CSS_SELECTOR, css_selector)

    def get_language(self, value):
        return self.language_select_option(value).text

    def select_language(self, value):
        self.language_select_option(value).click()
        return self

    def publication_date_select_option(self, value):
        xpath_selector = './/option[text()="{value}"]'.format(value=str(value))
        return self.publication_date_select.find_element(By.XPATH, xpath_selector)

    def select_publication_date(self, value):
        self.publication_date_select_option(value).click()
        return self

    def sort_by_select_option(self, value):
        css_selector = 'option[value="{value}"]'.format(value=value)
        return self.sort_by_select.find_element(By.CSS_SELECTOR, css_selector)

    def select_sort_by(self, value):
        self.sort_by_select_option(value).click()
        return self

    def submit(self):
        self.form.submit()
        from pages.webview.search_results import SearchResults

        search_results = SearchResults(self.driver, self.base_url, self.timeout)
        return search_results.wait_for_page_to_load()
