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
@markers.test_case('C176268', 'C176269')
@markers.nondestructive
def test_search_input_and_button_are_displayed(webview_base_url, selenium):
    # GIVEN the webview base url and Selenium driver

    # WHEN the home page URL is fully loaded,
    #      and the browse link in the navbar is clicked
    page = Home(selenium, webview_base_url).open()
    browse_page = page.header.click_search()

    # THEN The search bar and the advanced search button is displayed
    assert browse_page.is_search_input_displayed
    assert browse_page.is_advanced_search_link_displayed


@markers.webview
@markers.nondestructive
def test_search_no_results(webview_base_url, selenium):
    # GIVEN the browse page and a bogus query
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()
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
def test_subject_categories_load(webview_base_url, selenium):
    # GIVEN the webview base url and Selenium driver

    # When the homepage is fully loaded,
    #      and the browse link in the navbar is clicked
    page = Home(selenium, webview_base_url).open()
    browse_page = page.header.click_search()

    # Then The subject categories are loaded
    assert len(browse_page.subject_list) > 0


@markers.webview
@markers.nondestructive
def test_subject_categories_have_page_and_book_counts(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # When the browse link in the navbar is clicked
    browse = home.header.click_search()

    # Then the subject categories have page and book counts
    for subject in browse.subject_list:
        assert subject.pages_count > 0
        assert subject.books_count > 0


@markers.webview
@markers.nondestructive
def test_click_subject_category(webview_base_url, selenium):
    # GIVEN the browse page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()

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


# The query needs to contain a rare word, otherwise we may timeout when searching
# Postgres removes stop words automatically, so don't include those either
@markers.webview
@markers.nondestructive
@markers.parametrize("query", ['Boreal Aardvark'])
def test_search(webview_base_url, selenium, query):
    # GIVEN the browse page and a query
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()

    # WHEN we search for the query
    search_results = browse.search(query)

    # THEN search results are displayed with the query text
    assert type(search_results) is SearchResults

    for (word, breadcrumb) in zip(query.split(), search_results.breadcrumbs):
        assert breadcrumb.is_text
        assert breadcrumb.value == word

    assert not search_results.has_no_results


# The query needs to contain few, rare words, otherwise we may timeout when searching
# Postgres removes stop words automatically, so don't include those either
@markers.webview
@markers.nondestructive
@markers.parametrize("query", ['Boreal Aardvark'])
def test_search_filter(webview_base_url, selenium, query):
    # GIVEN the search results page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()
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


# The query needs to contain few, rare words, otherwise we may timeout when searching
# Postgres removes stop words automatically, so don't include those either
@markers.webview
@markers.nondestructive
@markers.parametrize("query", ['Boreal Aardvark'])
def test_search_unfilter(webview_base_url, selenium, query):
    # GIVEN the search results page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()
    search_results = browse.search(query)

    # WHEN we click on breadcrumb's X link
    search_results = search_results.breadcrumbs[0].click_x_link()

    # THEN search results are displayed with one less filter
    assert type(search_results) is SearchResults

    for (word, breadcrumb) in zip(query.split()[1:], search_results.breadcrumbs):
        assert breadcrumb.is_text
        assert breadcrumb.value == word

    assert not search_results.has_no_results


# The query needs to contain few, rare words, otherwise we may timeout when searching
# Postgres removes stop words automatically, so don't include those either
# At least one of the words must appear in some headline text to test the bolding feature
@markers.webview
@markers.nondestructive
@markers.parametrize("query", ['Aardvark Syllabi'])
def test_search_bold(webview_base_url, selenium, query):
    # GIVEN the browse page and a query
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()

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
    # This could inadvertently become False if other modules with matching metadata are published
    assert any_occurrences, 'No words from the query showed up in the results.'


# The query needs to contain few, rare words, otherwise we may timeout when searching
# Postgres removes stop words automatically, so don't include those either
@markers.webview
@markers.nondestructive
@markers.parametrize("query", ['Boreal Aardvark'])
def test_search_click_result(webview_base_url, selenium, query):
    # GIVEN the search results page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()
    search_results = browse.search(query)

    # WHEN we click on a search result's title
    result = search_results.results[0]
    result_title = result.title
    content = search_results.results[0].click_title_link()

    # THEN we are taken to the matching content page
    assert type(content) is Content
    assert content.title == result_title


# The query needs to contain few, rare words, otherwise we may timeout when searching
# Postgres removes stop words automatically, so don't include those either
@markers.webview
@markers.nondestructive
@markers.parametrize("query", ['Boreal Aardvark'])
def test_search_pagination(webview_base_url, selenium, query):
    # GIVEN the browse page and a query
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()

    # WHEN we search for the query
    search_results = browse.search(query)

    # THEN search results are displayed with pagination
    assert type(search_results) is SearchResults

    pagination = search_results.pagination
    assert len(pagination) >= 4

    prev = pagination[0]
    assert prev.is_disabled
    assert not prev.is_active

    p1 = pagination[1]
    assert not p1.is_disabled
    assert p1.is_active

    p2 = pagination[2]
    assert not p2.is_disabled
    assert not p2.is_active

    next = pagination[-1]
    assert not next.is_disabled
    assert not next.is_active


# The query needs to contain few, rare words, otherwise we may timeout when searching
# Postgres removes stop words automatically, so don't include those either
@markers.webview
@markers.nondestructive
@markers.parametrize("query", ['Boreal Aardvark'])
def test_search_click_pagination(webview_base_url, selenium, query):
    # GIVEN the search results page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()
    search_results = browse.search(query)

    # WHEN we click on the "next" pagination link
    next = search_results.pagination[-1]
    search_results = next.click_link()

    # THEN the pagination is updated
    assert type(search_results) is SearchResults

    pagination = search_results.pagination
    assert len(pagination) >= 4

    prev = pagination[0]
    assert not prev.is_disabled
    assert not prev.is_active

    p1 = pagination[1]
    assert not p1.is_disabled
    assert not p1.is_active

    p2 = pagination[2]
    assert not p2.is_disabled
    assert p2.is_active

    next = pagination[-1]
    # assert next.is_disabled - will change if we have more than 2 pages of results in the future
    assert not next.is_active


@markers.webview
@markers.nondestructive
def test_advanced_search(webview_base_url, selenium):
    # GIVEN the advanced search page, advanced search field values, and the expected breadcrumbs
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()
    advanced_search = browse.click_advanced_search_link()
    search = {
        'Author': 'OpenStax',
        'Title': 'Concepts of Biology',
        'Subject': 'Science and Technology',
        'Keyword': ['Boreal', 'Aardvark'],
        'Type': 'book',
        'Language': 'en',
        'Publication Date': '2018'
    }
    sort_by = 'pubDate'

    # WHEN we select some filters and click submit
    language = advanced_search.get_language(search['Language'])
    search_results = advanced_search.fill_in_author(search['Author']) \
                                    .fill_in_title(search['Title']) \
                                    .select_subject(search['Subject']) \
                                    .fill_in_keywords(' '.join(list(search['Keyword']))) \
                                    .select_type(search['Type']) \
                                    .select_language(search['Language']) \
                                    .select_publication_date(search['Publication Date']) \
                                    .select_sort_by(sort_by) \
                                    .submit()

    # THEN search results are displayed with the chosen filters
    assert type(search_results) is SearchResults

    for breadcrumb in search_results.breadcrumbs:
        limit = breadcrumb.limit
        if limit == 'Language':
            expected_values = language
        else:
            expected_values = search[limit]

        if not type(expected_values) is list:
            expected_values = [expected_values]

        assert breadcrumb.value in expected_values

    assert not search_results.has_no_results


@markers.webview
@markers.nondestructive
def test_logo_link_loads_home_page(webview_base_url, selenium):
    # GIVEN the browse page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()

    # WHEN the OpenStax CNX logo is clicked
    home = browse.header.click_logo()

    # THEN the home page is loaded
    assert type(home) is Home
