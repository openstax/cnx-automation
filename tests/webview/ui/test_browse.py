# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from random import choice
from string import digits, ascii_letters

from tests import markers

from pages.webview.home import Home
from pages.webview.search_results import SearchResults
from pages.webview.content import Content


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


@markers.webview
@markers.nondestructive
def test_click_subject_category(base_url, selenium):
    # GIVEN the browse page
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()

    # WHEN a subject category is clicked
    subject = browse.subject_list[0]
    subject_name = subject.name
    search_results = subject.click()

    # THEN search results are displayed with the correct subject title
    assert type(search_results) is SearchResults
    breadcrumb = search_results.breadcrumbs[0]
    assert breadcrumb.is_subject
    assert breadcrumb.subject == subject_name
    assert not search_results.has_no_results


@markers.webview
@markers.nondestructive
def test_search(base_url, selenium):
    # GIVEN the browse page and a query
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()
    # Needs to contain a rare word, otherwise we may timeout when searching
    # Postgres removes stop words automatically, so don't include those either
    query = 'Amazing Aardvark Concepts'

    # WHEN we search for the query
    search_results = browse.search(query)

    # THEN search results are displayed with the query text
    assert type(search_results) is SearchResults

    for (word, breadcrumb) in zip(query.split(), search_results.breadcrumbs):
        assert breadcrumb.is_text
        assert breadcrumb.value == word

    assert not search_results.has_no_results


@markers.webview
@markers.nondestructive
def test_search_filter(base_url, selenium):
    # GIVEN the search results page
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()
    # Needs to contain a rare word, otherwise we may timeout when searching
    # Postgres removes stop words automatically, so don't include those either
    query = 'Amazing Aardvark Concepts'
    search_results = browse.search(query)

    # WHEN we click on a filter
    search_results = search_results.filters[0].click()

    # THEN search results are displayed with the added filter
    assert type(search_results) is SearchResults

    breadcrumbs = search_results.breadcrumbs
    breadcrumb = breadcrumbs[len(query.split())]

    assert breadcrumb.is_publication_date
    # Just in case more Aardvarks are published in 2019+
    assert int(breadcrumb.value) >= 2018

    assert not search_results.has_no_results


@markers.webview
@markers.nondestructive
def test_search_unfilter(base_url, selenium):
    # GIVEN the search results page
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()
    # Needs to contain a rare word, otherwise we may timeout when searching
    # Postgres removes stop words automatically, so don't include those either
    # The rare word should probably not be the first word, since that one will be X'd in the test
    query = 'Amazing Aardvark Concepts'
    search_results = browse.search(query)

    # WHEN we click on breadcrumb's X link
    search_results = search_results.breadcrumbs[0].click_x_link()

    # THEN search results are displayed with one less filter
    assert type(search_results) is SearchResults

    for (word, breadcrumb) in zip(query.split()[1:], search_results.breadcrumbs):
        assert breadcrumb.is_text
        assert breadcrumb.value == word

    assert not search_results.has_no_results


@markers.webview
@markers.nondestructive
def test_search_bold(base_url, selenium):
    # GIVEN the browse page and a query
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()
    # Needs to contain a rare word, otherwise we may timeout when searching
    # Postgres removes stop words automatically, so don't include those either
    query = 'Amazing Aardvark Concepts'

    # WHEN we search for the query
    search_results = browse.search(query)

    # THEN search results are displayed with query words bolded
    assert type(search_results) is SearchResults
    assert not search_results.has_no_results

    results = search_results.results
    any_occurrences = False

    # Test that all occurrences are bolded
    for word in query.split():
        for result in results:
            occurrences = result.count_occurrences(word)

            if occurrences > 0:
                any_occurrences = True

            assert occurrences == result.count_bold_occurrences(word)

    # At least one word must show up in the results
    # This could become False if someone publishes blank modules with matching metadata
    assert any_occurrences, 'No words from the query showed up in the results.'


@markers.webview
@markers.nondestructive
def test_search_click_result(base_url, selenium):
    # GIVEN the search results page
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()
    # Needs to contain a rare word, otherwise we may timeout when searching
    # Postgres removes stop words automatically, so don't include those either
    query = 'Amazing Aardvark Concepts'
    search_results = browse.search(query)

    # WHEN we click on a search result's title
    result = search_results.results[0]
    result_title = result.title
    content = search_results.results[0].click_title_link()

    # THEN we are taken to the matching content page
    assert type(content) is Content
    assert content.title == result_title


@markers.webview
@markers.nondestructive
def test_logo_link_loads_home_page(base_url, selenium):
    # GIVEN the browse page
    home = Home(selenium, base_url).open()
    browse = home.header.click_browse()

    # WHEN the OpenStax CNX logo is clicked
    home = browse.header.click_logo()

    # THEN the home page is loaded
    assert type(home) is Home
