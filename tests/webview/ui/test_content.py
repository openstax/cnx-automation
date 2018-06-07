# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.action_chains import ActionChains

from tests import markers

from pages.webview.home import Home
from pages.webview.content import Content


@markers.webview
@markers.nondestructive
def test_navs_and_elements_are_displayed(base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # THEN the site navbar and content nav are displayed
    assert content.header.is_nav_displayed
    content_header = content.content_header
    assert content_header.is_displayed
    assert content_header.is_title_displayed
    assert content_header.is_book_by_displayed
    assert content_header.is_share_displayed
    header_nav = content_header.nav
    assert header_nav.is_contents_button_displayed
    assert header_nav.is_searchbar_displayed
    assert header_nav.is_back_link_displayed
    assert header_nav.is_progress_bar_displayed
    assert header_nav.is_next_link_displayed
    assert content.is_section_title_displayed


@markers.webview
@markers.nondestructive
def test_share_on_top_right_corner(base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # THEN social share links are displayed in the top right corner
    root = content.share.root
    # Top half
    assert root.location['y'] + root.size['height'] < selenium.get_window_size()['height']/2
    # Right half
    assert root.location['x'] > selenium.get_window_size()['width']/2


@markers.webview
@markers.nondestructive
def test_share_links_displayed(base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # THEN social share links are displayed with the expected urls
    share = content.share
    assert share.is_displayed
    assert share.is_facebook_share_link_displayed
    assert share.is_twitter_share_link_displayed
    assert share.is_google_share_link_displayed
    assert share.is_linkedin_share_link_displayed


@markers.webview
@markers.nondestructive
def test_content(base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[0]
    content_page = book.click_book_cover()

    # THEN the book content is present and contains figure(s)
    content = content_page.content
    assert not content.is_blank
    assert content.has_figures


@markers.webview
@markers.nondestructive
def test_scroll(base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # WHEN we scroll to the bottom
    footer = content.footer
    ActionChains(selenium).move_to_element(footer.root).perform()

    # THEN the content nav is displayed on top without the site navbar or any social links
    # assert not content.header.is_nav_displayed # Returns True even though site nav is offscreen
    content_header = content.content_header
    assert content_header.is_displayed
    assert content_header.is_title_displayed
    assert content_header.is_book_by_displayed
    assert not content_header.is_share_displayed
    header_nav = content_header.nav
    assert header_nav.is_contents_button_displayed
    assert header_nav.is_searchbar_displayed
    assert header_nav.is_back_link_displayed
    assert header_nav.is_progress_bar_displayed
    assert header_nav.is_next_link_displayed
    assert content.is_section_title_displayed
    share = content.share
    assert not share.is_displayed
    assert not share.is_facebook_share_link_displayed
    assert not share.is_twitter_share_link_displayed
    assert not share.is_google_share_link_displayed
    assert not share.is_linkedin_share_link_displayed

    # The footer is displayed at the bottom
    assert footer.is_displayed
    assert footer.is_downloads_tab_displayed
    assert footer.is_history_tab_displayed
    assert footer.is_attribution_tab_displayed
    assert footer.is_more_information_tab_displayed

    # Hard to check that the content_header is on top after scrolling, but we can check
    # that it at least has the pinned class and is above the footer
    assert 'pinned' in content_header.root.get_attribute('class')
    assert content_header.root.location['y'] < footer.root.location['y']


@markers.webview
@markers.nondestructive
def test_nav(base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()
    assert type(content) == Content
    assert content.chapter_section == '1'

    # WHEN we navigate next twice and then back twice using the header and footer controls
    content = content.header_nav.click_next_link()
    assert type(content) == Content
    assert content.chapter_section == '1.1'

    content = content.footer_nav.click_next_link()
    assert type(content) == Content
    assert content.chapter_section == '1.2'

    content = content.footer_nav.click_back_link()
    assert type(content) == Content
    assert content.chapter_section == '1.1'

    content = content.header_nav.click_back_link()

    # THEN we arrive back at the initial page
    assert type(content) == Content
    assert content.chapter_section == '1'


@markers.webview
@markers.slow
@markers.nondestructive
def test_ncy_is_not_displayed(american_gov_url, selenium):
    # GIVEN An American Government URL and Selenium driver

    # WHEN The page is fully loaded using the URL
    page = Content(selenium, american_gov_url).open()

    # THEN :NOT_CONVERTED_YET is not displayed
    assert page.is_ncy_displayed is False
