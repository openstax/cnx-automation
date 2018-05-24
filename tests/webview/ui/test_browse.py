# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from random import choice
from string import digits, ascii_letters

from tests import markers

from pages.webview.home import Home
from pages.webview.search_results import SearchResults


@markers.webview
@markers.nondestructive
def test_search_input_and_button_are_displayed(base_url, selenium):
    # GIVEN The base_url and Selenium driver

    # WHEN The home page URL is fully loaded,
    #      and the browse link in the navbar is clicked
    page = Home(selenium, base_url).open()
    browse_page = page.header.click_browse()

    # THEN The search bar and the advanced search button is displayed
    assert browse_page.is_search_input_displayed
    assert browse_page.is_advanced_search_button_displayed


@markers.webview
@markers.nondestructive
def test_search_no_results(base_url, selenium):
    # GIVEN the browse page and a bogus query
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()
    query = ''.join(choice(digits + ascii_letters) for i in range(32))

    # WHEN we search for the bogus query
    search_results = browse.search(query)

    # THEN the localized "no results found" message is displayed
    assert type(search_results) is SearchResults
    assert search_results.has_no_results
    # Valid only when the website is in English
    assert search_results.no_results_text == 'No results found. Please try expanding your search.'


@markers.webview
@markers.nondestructive
def test_subject_categories_load(base_url, selenium):
    # GIVEN the base_url and Selenium driver

    # When The homepage URL is fully loaded,
    #      and the browse link in the navbar is clicked
    page = Home(selenium, base_url).open()
    browse_page = page.header.click_browse()

    # Then The subject categories are loaded
    assert len(browse_page.subject_list) > 0


@markers.webview
@markers.nondestructive
def test_subject_categories_have_page_and_book_counts(base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, base_url).open()

    # When the browse link in the navbar is clicked
    browse = home.header.click_browse()

    # Then the subject categories have page and book counts
    for subject in browse.subject_list:
        assert subject.pages_count > 0
        assert subject.books_count > 0


def test_logo_link_loads_home_page(base_url, selenium):
    # GIVEN the browse page
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()

    # WHEN the OpenStax CNX logo is clicked
    home = browse.header.click_logo()

    # THEN the home page is loaded
    assert type(home) is Home
