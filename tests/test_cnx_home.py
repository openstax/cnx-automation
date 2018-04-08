# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import Home


@pytest.mark.nondestructive
def test_splash_banner_loads(base_url, selenium):
    page = Home(selenium, base_url).open()
    assert page.header.is_nav_displayed
    assert 'Discover learning materials in an Open Space' in page.splash


@pytest.mark.nondestructive
def test_featured_books_load(base_url, selenium):
    page = Home(selenium, base_url).open()
    assert len(page.featured_books.openstax_list) > 0
    assert len(page.featured_books.cnx_list) > 0


@pytest.mark.nondestructive
def test_read_more_loads_correct_page(base_url, selenium):
    page = Home(selenium, base_url).open()
    book = page.featured_books.openstax_list[0]
    name = book.name
    content_page = book.click_read_more()
    assert name == content_page.title


@pytest.mark.nondestructive
def test_book_cover_loads_correct_page(base_url, selenium):
    page = Home(selenium, base_url).open()
    book = page.featured_books.openstax_list[0]
    name = book.name
    content_page = book.click_book_cover()
    assert name == content_page.title


@pytest.mark.nondestructive
def test_title_link_loads_correct_page(base_url, selenium):
    page = Home(selenium, base_url).open()
    book = page.featured_books.openstax_list[0]
    name = book.name
    content_page = book.click_title_link()
    assert name == content_page.title
