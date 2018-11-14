# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.webview.home import Home
from pages.webview.search_results import SearchResults


@markers.webview
@markers.test_case("C176268", "C176269")
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
@markers.test_case("C176270")
@markers.nondestructive
def test_subject_categories_load(webview_base_url, selenium):
    # GIVEN the webview base url and Selenium driver

    # When the homepage is fully loaded,
    #      and the browse link in the navbar is clicked
    page = Home(selenium, webview_base_url).open()
    browse_page = page.header.click_search()

    # Then The subject categories are loaded
    assert len(browse_page.search_category_list) > 0


@markers.webview
@markers.test_case("C176271")
@markers.nondestructive
def test_subject_categories_have_page_and_book_counts(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN the browse link in the navbar is clicked
    browse = home.header.click_search()

    # Look for counts in any catagory. When working with a test dataset
    # not all subjects will have content. Therefore, we test that
    # at least one of the subjects has a count. This effectively tests
    # the communication between the browser and the web api as well as the
    # browser's ability to render the results.
    page_counts = set([])
    book_counts = set([])

    # Record the subject category count for pages and books
    for subject in browse.search_category_list:
        page_counts.add(subject.pages_count)
        book_counts.add(subject.books_count)

    # THEN verify one or more subject categories have a count
    assert True in [c > 0 for c in page_counts]
    assert True in [c > 0 for c in book_counts]


@markers.webview
@markers.test_case("C176272")
@markers.nondestructive
def test_click_subject_category(webview_base_url, selenium):
    # GIVEN the browse page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()

    # WHEN a subject category is clicked
    subject = browse.search_category_list[3]
    subject_name = subject.name
    search_results = subject.click()

    # THEN search results are displayed with the correct subject title
    assert type(search_results) is SearchResults
    breadcrumb = search_results.breadcrumbs[0]
    assert breadcrumb.is_subject
    assert breadcrumb.subject == subject_name
    assert not search_results.has_no_results


@markers.webview
@markers.test_case("C176230")
@markers.nondestructive
def test_logo_link_loads_home_page(webview_base_url, selenium):
    # GIVEN the browse page
    home = Home(selenium, webview_base_url).open()
    browse = home.header.click_search()

    # WHEN the OpenStax CNX logo is clicked
    home = browse.header.click_cnx_logo()

    # THEN the home page is loaded
    assert type(home) is Home
