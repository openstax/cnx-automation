# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region


class SearchResults(Page):
    URL_TEMPLATE = '/search'
    _filters_locator = (By.CSS_SELECTOR, '#search div.results div.breadcrumbs span.breadcrumb')
    _no_results_p_locator = (By.CSS_SELECTOR,
                             '#results p[data-l10n-id="search-results-list-no-results"]')

    @property
    def loaded(self):
        return self.is_element_displayed(*self._filters_locator)

    @property
    def filters(self):
        elements = self.find_elements(*self._filters_locator)
        return [self.Filter(self, element) for element in elements]

    @property
    def has_no_results(self):
        return self.is_element_displayed(*self._no_results_p_locator)

    @property
    def no_results_p(self):
        return self.find_element(*self._no_results_p_locator)

    @property
    def no_results_text(self):
        return self.no_results_p.text

    class Filter(Region):
        # Only subject and text filters are currently supported/implemented
        _subject_limit_span_locator = (By.CSS_SELECTOR,
                                       'span.limit[data-l10n-id="search-results-filter-subject"]')
        _text_limit_span_locator = (By.CSS_SELECTOR,
                                    'span.limit[data-l10n-id="search-results-filter-text"]')
        _value_span_locator = (By.CSS_SELECTOR, 'span.value')

        @property
        def is_subject(self):
            return self.is_element_present(*self._subject_limit_span_locator)

        @property
        def is_text(self):
            return self.is_element_present(*self._text_limit_span_locator)

        @property
        def value_span(self):
            return self.find_element(*self._value_span_locator)

        @property
        def value(self):
            return self.value_span.text

        # For subject filters we can use the l10n attributes to be localization-agnostic
        @property
        def subject(self):
            import json
            return json.loads(self.value_span.get_attribute('data-l10n-args'))['subject']
