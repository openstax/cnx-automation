# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from selenium.webdriver.common.action_chains import ActionChains

from tests import markers

from pages.webview.home import Home

_number_of_tested_books = 2


@markers.webview
@markers.nondestructive
def test_splash_banner_loads(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded
    page = Home(selenium, webview_base_url).open()

    # THEN the splash text is correct
    assert 'Discover learning materials in an Open Space' in page.splash


@markers.webview
@markers.nondestructive
def test_nav_is_displayed(webview_base_url, selenium):
    # GIVEN the webview base url and the Selenium driver

    # WHEN the home page is fully loaded
    page = Home(selenium, webview_base_url).open()

    # THEN the navbar is displayed
    assert page.header.is_nav_displayed


@markers.webview
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
        # Needed to prevent failures when trying to click books that are offscreen
        ActionChains(selenium).move_to_element(book.root).perform()
        content_page = book.click_read_more()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        selenium.back()
        home = home.wait_for_page_to_load()


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
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
        # Needed to prevent failures when trying to click books that are offscreen
        ActionChains(selenium).move_to_element(book.root).perform()
        content_page = book.click_book_cover()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        selenium.back()
        home = home.wait_for_page_to_load()


@markers.xfail(reason='https://trello.com/c/mFRaZRqK', raises=AssertionError)
@markers.webview
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
        # Needed to prevent failures when trying to click books that are offscreen
        ActionChains(selenium).move_to_element(book.root).perform()
        content_page = book.click_title_link()

        # THEN The book title from the home page matches the content page title
        assert book_title == content_page.title

        selenium.back()
        home = home.wait_for_page_to_load()


@markers.webview
@markers.nondestructive
def test_logo_link_stays_on_home_page(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN the OpenStax CNX logo is clicked
    home = home.header.click_logo()

    # THEN we are still in the home page
    assert type(home) is Home
