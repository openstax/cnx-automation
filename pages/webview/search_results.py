# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page


class SearchResults(Page):
    URL_TEMPLATE = '/search'
    _query_locator = (By.CSS_SELECTOR, '#search div.results div.breadcrumbs span.breadcrumb')
    _no_results_p_locator = (By.CSS_SELECTOR,
                             '#results p[data-l10n-id="search-results-list-no-results"]')

    @property
    def loaded(self):
        return self.is_element_displayed(*self._query_locator)

    @property
    def has_no_results(self):
        return self.is_element_displayed(*self._no_results_p_locator)

    @property
    def no_results_p(self):
        return self.find_element(*self._no_results_p_locator)

    @property
    def no_results_text(self):
        return self.no_results_p.text
