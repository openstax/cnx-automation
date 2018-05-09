# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.webview.home import Home


@markers.webview
@markers.nondestructive
def test_splash_banner_loads(base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The home page URL is fully loaded
    page = Home(selenium, base_url).open()

    # THEN The splash text is correct
    assert 'Discover learning materials in an Open Space' in page.splash


@markers.webview
@markers.nondestructive
def test_nav_is_displayed(base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The main website URL is fully loaded
    page = Home(selenium, base_url).open()

    # THEN The navbar is displayed
    assert page.header.is_nav_displayed


@markers.webview
@markers.nondestructive
def test_featured_books_load(base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The main website URL is fully loaded
    page = Home(selenium, base_url).open()

    # THEN the featured books for OpenStax and CNX are greater than 0
    assert len(page.featured_books.openstax_list) > 0
    assert len(page.featured_books.cnx_list) > 0


@markers.webview
@markers.nondestructive
def test_read_more_loads_correct_page(base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The main website URL is fully loaded,
    #      Find the first OpenStax book and click the Read More link
    page = Home(selenium, base_url).open()
    book = page.featured_books.openstax_list[0]
    book_title = book.title
    content_page = book.click_read_more()

    # THEN The book title from the home page matches the content page title
    assert book_title == content_page.title


@markers.webview
@markers.nondestructive
def test_book_cover_loads_correct_page(base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The main website URL is fully loaded,
    #      Find the first OpenStax book and click the book cover link
    page = Home(selenium, base_url).open()
    book = page.featured_books.openstax_list[0]
    book_title = book.title
    content_page = book.click_book_cover()

    # THEN The book title from the home page matches the content page title
    assert book_title == content_page.title


@markers.webview
@markers.nondestructive
def test_title_link_loads_correct_page(base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The main website URL is fully loaded,
    #      Find the first OpenStax book and click the title link
    page = Home(selenium, base_url).open()
    book = page.featured_books.openstax_list[0]
    book_title = book.title
    content_page = book.click_title_link()

    # THEN The book title from the home page matches the content page title
    assert book_title == content_page.title
