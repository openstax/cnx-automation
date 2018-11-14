# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pages.webview.base import Page
from regions.webview.base import Region


class SearchResults(Page):
    URL_TEMPLATE = "/search?q={q}"
    _num_results_span_locator = (
        By.CSS_SELECTOR,
        'span[data-l10n-id="search-results-number-results"]',
    )
    _filters_locator = (By.CSS_SELECTOR, "#search div.results ul.filters li")
    _breadcrumbs_locator = (By.CSS_SELECTOR, "#search div.results div.breadcrumbs span.breadcrumb")
    _pagination_locator = (By.CSS_SELECTOR, "#results div.pagination ul li")
    _too_long_results_p_locator = (
        By.CSS_SELECTOR,
        '#results p[data-l10n-id="search-results-list-search-taking-time"]',
    )
    _no_results_p_locator = (
        By.CSS_SELECTOR,
        '#results p[data-l10n-id="search-results-list-no-results"]',
    )
    _results_locator = (By.CSS_SELECTOR, "#results table.table tbody tr")

    @property
    def loaded(self):
        return self.is_element_displayed(*self._num_results_span_locator)

    @property
    def filters(self):
        elements = self.find_elements(*self._filters_locator)
        return [self.Filter(self, element) for element in elements]

    @property
    def breadcrumbs(self):
        elements = self.find_elements(*self._breadcrumbs_locator)
        return [self.Breadcrumb(self, element) for element in elements]

    @property
    def pagination(self):
        elements = self.find_elements(*self._pagination_locator)
        return [self.Pagination(self, element) for element in elements]

    @property
    def results(self):
        elements = self.find_elements(*self._results_locator)
        return [self.Result(self, element) for element in elements]

    @property
    def search_took_too_long(self):
        return self.is_element_displayed(*self._too_long_results_p_locator)

    @property
    def has_no_results(self):
        return self.is_element_displayed(*self._no_results_p_locator)

    @property
    def no_results_p(self):
        return self.find_element(*self._no_results_p_locator)

    @property
    def no_results_text(self):
        return self.no_results_p.text

    def wait_for_page_to_load(self, max_attempts=3):
        for i in range(max_attempts):
            # Sometimes the search takes too long and we get a timeout.
            # When this happens, we reload the page and try again.
            try:
                self = super().wait_for_page_to_load()
            except TimeoutException:
                pass
            else:
                if not self.search_took_too_long:
                    return self

            if i < max_attempts - 1:
                self.driver.refresh()

        from pytest import fail

        fail(
            "Maximum number of attempts exceeded for search"
            " ({attempts})".format(attempts=max_attempts)
        )

    class Filter(Region):
        _link_locator = (By.TAG_NAME, "a")

        @property
        def link(self):
            return self.find_element(*self._link_locator)

        def click(self):
            self.link.click()
            search_results = SearchResults(self.driver, self.page.base_url, self.page.timeout)
            return search_results.wait_for_page_to_load()

    class Breadcrumb(Region):
        _x_link_locator = (By.CSS_SELECTOR, "a.remove")
        _limit_span_locator = (By.CSS_SELECTOR, "span.limit")
        _subject_limit_span_locator = (
            By.CSS_SELECTOR,
            'span.limit[data-l10n-id="search-results-filter-subject"]',
        )
        _text_limit_span_locator = (
            By.CSS_SELECTOR,
            'span.limit[data-l10n-id="search-results-filter-text"]',
        )
        _pub_year_limit_span_locator = (
            By.CSS_SELECTOR,
            'span.limit[data-l10n-id="search-results-filter-pubYear"]',
        )
        _value_span_locator = (By.CSS_SELECTOR, "span.value")

        @property
        def is_subject(self):
            return self.is_element_present(*self._subject_limit_span_locator)

        @property
        def is_text(self):
            return self.is_element_present(*self._text_limit_span_locator)

        @property
        def is_publication_date(self):
            return self.is_element_present(*self._pub_year_limit_span_locator)

        @property
        def x_link(self):
            return self.find_element(*self._x_link_locator)

        @property
        def limit_span(self):
            return self.find_element(*self._limit_span_locator)

        @property
        def limit(self):
            return self.limit_span.text

        @property
        def value_span(self):
            return self.find_element(*self._value_span_locator)

        @property
        def value(self):
            return self.value_span.text

        # For subject breadcrumbs we can use the l10n attributes to be localization-agnostic
        @property
        def subject(self):
            import json

            return json.loads(self.value_span.get_attribute("data-l10n-args"))["subject"]

        def click_x_link(self):
            self.x_link.click()
            search_results = SearchResults(self.driver, self.page.base_url, self.page.timeout)
            return search_results.wait_for_page_to_load()

    class Pagination(Region):
        _link_locator = (By.TAG_NAME, "a")

        @property
        def root_class(self):
            return self.root.get_attribute("class")

        @property
        def is_disabled(self):
            return "disabled" in self.root_class

        @property
        def is_active(self):
            return "active" in self.root_class

        @property
        def link(self):
            return self.find_element(*self._link_locator)

        def click_link(self):
            self.link.click()
            search_results = SearchResults(self.driver, self.page.base_url, self.page.timeout)
            return search_results.wait_for_page_to_load()

    class Result(Region):
        _title_td_locator = (By.CSS_SELECTOR, "td.title")
        _link_locator = (By.TAG_NAME, "a")
        _content_span_locator = (By.TAG_NAME, "span")
        _bold_locator = (By.TAG_NAME, "b")

        @property
        def title_td(self):
            return self.find_element(*self._title_td_locator)

        @property
        def title_link(self):
            return self.title_td.find_element(*self._link_locator)

        @property
        def title(self):
            return self.title_link.text

        # For some reason the content span is inside the td.title
        @property
        def content_span(self):
            return self.title_td.find_element(*self._content_span_locator)

        @property
        def content(self):
            return self.content_span.text

        @property
        def bolds(self):
            return self.content_span.find_elements(*self._bold_locator)

        def count_occurrences(self, word):
            return self.content.lower().count(word.lower())

        def count_bold_occurrences(self, word):
            lowercase_word = word.lower()
            return len([bold for bold in self.bolds if lowercase_word in bold.text.lower()])

        def click_title_link(self):
            self.title_link.click()
            from pages.webview.content import Content

            content = Content(self.driver, self.page.base_url, self.page.timeout)
            return content.wait_for_page_to_load()
