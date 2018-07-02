# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from tests import markers

from pages.webview.home import Home

_number_of_tested_books = 2


@markers.webview
@markers.test_case('C167405')
@markers.nondestructive
@markers.parametrize('width,height', [(1024, 768), (640, 480)])
def test_top_right_links_and_nav(width, height, webview_base_url, legacy_base_url, selenium):
    # GIVEN the window width and height, the webview URL, the legacy URL, and the Selenium driver
    selenium.set_window_size(width, height)

    # WHEN the webview home page is fully loaded
    home = Home(selenium, webview_base_url).open()
    header = home.header

    # THEN the top right links, logos and nav are displayed and point to the correct URLs
    assert header.is_support_link_displayed
    assert header.support_url == 'http://openstax.force.com/support?l=en_US&c=Products%3ACNX'

    assert header.is_legacy_site_link_displayed
    expected_legacy_url = '{legacy_url}/content?legacy=true'.format(legacy_url=legacy_base_url)
    assert header.legacy_site_url == expected_legacy_url, (
               'The legacy URL in the CNX home page did not match the legacy_base_url. '
               'Check that both webview_base_url and legacy_base_url point to the same environment.'
           )

    assert header.is_cnx_logo_displayed
    assert header.cnx_logo_url.rstrip('/') == webview_base_url

    assert header.is_nav_displayed

    if header.is_nav_button_displayed:
        assert not header.is_browse_link_displayed
        assert not header.is_about_us_link_displayed
        assert not header.is_donate_link_displayed
        assert not header.is_rice_logo_displayed
        header.nav_button.click()

    assert header.is_browse_link_displayed
    assert header.browse_url == '{webview_url}/browse'.format(webview_url=webview_base_url)

    assert header.is_about_us_link_displayed
    assert header.about_us_url == '{webview_url}/about'.format(webview_url=webview_base_url)

    assert header.is_donate_link_displayed
    assert header.donate_url == '{webview_url}/donate'.format(webview_url=webview_base_url)

    assert header.is_rice_logo_displayed
    assert header.rice_logo_url.rstrip('/') == 'http://www.rice.edu'


@markers.webview
@markers.nondestructive
def test_splash_banner_loads(webview_base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The home page URL is fully loaded
    page = Home(selenium, webview_base_url).open()

    # THEN The splash text is correct
    assert 'Discover learning materials in an Open Space' in page.splash


@markers.webview
@markers.test_case('C176224', 'C176225')
@markers.nondestructive
def test_featured_books_load(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded
    page = Home(selenium, webview_base_url).open()

    # THEN there are featured books for both OpenStax and CNX
    assert len(page.featured_books.openstax_list) > 0
    assert len(page.featured_books.cnx_list) > 0


@markers.xfail(reason='https://trello.com/c/DL7xEWon', raises=AssertionError)
@markers.webview
@markers.test_case('C176226')
@markers.nondestructive
def test_featured_books_have_title_and_intro(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded
    home = Home(selenium, webview_base_url).open()

    # THEN all featured books have titles and intros
    books = home.featured_books.openstax_list + home.featured_books.cnx_list

    for book in books:
        assert book.title
        assert book.intro
        assert book.intro != '...'


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
@markers.test_case('C176227')
@markers.nondestructive
def test_read_more_loads_correct_page(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded,
    #      find the first OpenStax book and click the Read More link
    home = Home(selenium, webview_base_url).open()
    for i in range(_number_of_tested_books):
        # Can't use `for book in sample(home.featured_books.openstax_list, _number_of_tested_books)`
        # because it causes StaleElementReferenceExceptions
        book = random.choice(home.featured_books.openstax_list)
        book_title = book.title
        content_page = book.click_read_more()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        if i < _number_of_tested_books - 1:
            selenium.back()
            home = home.wait_for_page_to_load()


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
@markers.test_case('C176228')
@markers.nondestructive
def test_book_cover_loads_correct_page(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded,
    #      find the first OpenStax book and click the book cover link
    home = Home(selenium, webview_base_url).open()
    for i in range(_number_of_tested_books):
        # Can't use `for book in sample(home.featured_books.openstax_list, _number_of_tested_books)`
        # because it causes StaleElementReferenceExceptions
        book = random.choice(home.featured_books.openstax_list)
        book_title = book.title
        content_page = book.click_book_cover()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        if i < _number_of_tested_books - 1:
            selenium.back()
            home = home.wait_for_page_to_load()


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
@markers.test_case('C176229')
@markers.nondestructive
def test_title_link_loads_correct_page(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded,
    #      find the first OpenStax book and click the title link
    home = Home(selenium, webview_base_url).open()
    for i in range(_number_of_tested_books):
        # Can't use `for book in sample(home.featured_books.openstax_list, _number_of_tested_books)`
        # because it causes StaleElementReferenceExceptions
        book = random.choice(home.featured_books.openstax_list)
        book_title = book.title
        content_page = book.click_title_link()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        if i < _number_of_tested_books - 1:
            selenium.back()
            home = home.wait_for_page_to_load()


@markers.webview
@markers.test_case('C176230')
@markers.nondestructive
def test_logo_link_stays_on_home_page(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN the OpenStax CNX logo is clicked
    home = home.header.click_cnx_logo()

    # THEN we are still in the home page
    assert type(home) is Home
