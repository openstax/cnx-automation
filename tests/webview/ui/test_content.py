# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import re

from selenium.webdriver.common.by import By

from tests import markers

from pages.webview.home import Home
from pages.webview.content import Content


@markers.webview
@markers.test_case('C176231', 'C176232', 'C176233')
@markers.nondestructive
def test_navs_and_elements_are_displayed(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

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

    # Section title is on top of main content section (white area)
    main_content_section = content.main_content_section
    section_title_div = content.section_title_div

    # Section title inside main content section
    assert section_title_div.location['x'] >= main_content_section.location['x']
    assert section_title_div.location['y'] >= main_content_section.location['y']
    assert (section_title_div.location['x'] + section_title_div.size['width'] <=
            main_content_section.location['x'] + main_content_section.size['width'])
    assert (section_title_div.location['y'] + section_title_div.size['height'] <=
            main_content_section.location['y'] + main_content_section.size['height'])

    # Section title on top of main content section
    assert (section_title_div.location['y'] - main_content_section.location['y'] <=
            section_title_div.size['height'])


@markers.webview
@markers.test_case('C132542')
@markers.nondestructive
def test_author_is_openstax(webview_base_url, selenium):
    # GIVEN the home page and a book
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]

    # WHEN the book's cover is clicked
    content = book.click_book_cover()

    # THEN the displayed author is OpenStax
    content_header = content.content_header
    assert content_header.is_book_by_displayed
    assert content_header.is_author_displayed
    assert content_header.author == 'OpenStax'


@markers.webview
@markers.test_case('C176242')
@markers.nondestructive
def test_toc_is_displayed(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # WHEN the contents button is clicked
    toc = content.header_nav.click_contents_button()

    # THEN the table of contents is displayed
    assert toc.is_displayed
    assert toc.number_of_chapters > 0
    assert toc.number_of_pages > 0


@markers.webview
@markers.test_case('C176243', 'C176244')
@markers.nondestructive
def test_toc_navigation(webview_base_url, selenium):
    # GIVEN a book's table of contents
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()
    toc = content.header_nav.click_contents_button()

    # WHEN a chapter is expanded and we navigate to one of its pages
    chapter = toc.chapters[1]
    chapter = chapter.click()
    page = chapter.pages[1]
    chapter_section = page.chapter_section
    title = page.title
    content = page.click()

    # THEN we end up at the correct page
    assert type(content) is Content
    assert content.chapter_section == chapter_section
    assert content.section_title == title


@markers.webview
@markers.test_case('C176257')
@markers.nondestructive
def test_share_on_top_right_corner(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # THEN social share links are displayed in the top right corner
    share = content.share
    assert share.is_displayed
    assert share.is_facebook_share_link_displayed
    assert share.is_twitter_share_link_displayed
    assert share.is_google_share_link_displayed
    assert share.is_linkedin_share_link_displayed
    root = content.share.root
    # Top half
    assert root.location['y'] + root.size['height'] < selenium.get_window_size()['height']/2
    # Right half
    assert root.location['x'] > selenium.get_window_size()['width']/2


@markers.webview
@markers.test_case('C176258', 'C176259', 'C176260', 'C176261')
@markers.nondestructive
def test_share_links_displayed(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # THEN social share links have the expected urls
    current_url = selenium.current_url
    normalized_title = content.title.replace(' ', '%20')
    share = content.share

    expected_facebook_url = 'https://facebook.com/sharer/sharer.php?u={url}'.format(url=current_url)
    assert share.facebook_share_url == expected_facebook_url

    expected_twitter_url = 'https://twitter.com/share?url={url}&text={title}&via=cnxorg'.format(
        url=current_url, title=normalized_title)
    assert share.twitter_share_url == expected_twitter_url

    expected_google_url = 'https://plus.google.com/share?url={url}'.format(url=current_url)
    assert share.google_share_url == expected_google_url

    expected_linkedin_url = (
        'https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}&'
        'summary=An%20OpenStax%20CNX%20book&source=OpenStax%20CNX'
    ).format(url=current_url, title=normalized_title)
    assert share.linkedin_share_url == expected_linkedin_url


@markers.webview
@markers.test_case('C176234')
@markers.nondestructive
def test_get_this_book(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # WHEN we click the "Get This Book!" button
    button_displayed = content.is_get_this_book_button_displayed
    if button_displayed:
        get_this_book = content.click_get_this_book_button()
        pdf_displayed = get_this_book.is_pdf_link_displayed
        epub_displayed = get_this_book.is_epub_link_displayed
        offline_zip_displayed = get_this_book.is_offline_zip_link_displayed

    # THEN links to download the pdf, epub and offline zip versions are displayed
    # Look at the footer to see which downloads should have been available
    downloads = content.footer.click_downloads_tab()

    if not button_displayed:
        assert not downloads.is_any_available
        pytest.skip('No files available to download: "Get This Book!" button not present.')

    assert pdf_displayed == downloads.is_pdf_available
    assert epub_displayed == downloads.is_epub_available
    assert offline_zip_displayed == downloads.is_offline_zip_available


@markers.webview
@markers.test_case('C167408')
@markers.nondestructive
def test_section_title_for_no_markup(webview_base_url, selenium):
    # GIVEN the home page and a book
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]

    # WHEN the book's cover is clicked
    content = book.click_book_cover()

    # THEN the section title does not contain HTML markup
    section_title = content.section_title
    assert '<' not in section_title
    assert '>' not in section_title


@markers.webview
@markers.test_case('C176236')
@markers.nondestructive
def test_content_and_figures_display_after_scrolling(webview_base_url, selenium):
    # GIVEN a book's content page with figures
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content_page = book.click_book_cover()
    content_region = content_page.content_region
    assert not content_region.is_blank
    assert content_region.has_figures

    # WHEN we scroll to a figure
    content_region.scroll_to(content_region.figures[0])

    # THEN some figure is displayed
    assert content_region.is_figure_displayed


@markers.webview
@markers.test_case('C176235', 'C176237')
@markers.nondestructive
def test_nav_and_menus_display_after_scrolling(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # WHEN we scroll to the bottom
    footer = content.footer.scroll_to()

    # THEN the content nav is displayed on top without the site navbar or any social links
    # The header nav is offscreen but still considered displayed
    assert content.header.is_nav_displayed
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
@markers.test_case('C162171')
@markers.nondestructive
def test_attribution(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()

    # WHEN we click the attribution tab
    attribution = content.footer.click_attribution_tab()

    # THEN the attribution is displayed and has the correct support email
    assert attribution.is_displayed
    expected_sentence = 'For questions regarding this license, please contact support@openstax.org.'
    assert expected_sentence in attribution.text


@markers.webview
@markers.test_case('C176241')
@markers.nondestructive
def test_back_to_top(webview_base_url, selenium):
    # GIVEN a book's scrolled content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()
    footer = content.footer

    # WHEN we scroll to the bottom then click the back to top link
    footer_nav = footer.nav.scroll_to()
    content = footer_nav.click_back_to_top_link()

    # THEN the content page is no longer scrolled
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
    share = content.share
    assert share.is_displayed

    assert share.is_facebook_share_link_displayed
    assert share.is_twitter_share_link_displayed
    assert share.is_google_share_link_displayed
    assert share.is_linkedin_share_link_displayed

    # The footer is offscreen, but still considered displayed
    assert footer.is_displayed
    assert footer.is_downloads_tab_displayed
    assert footer.is_history_tab_displayed
    assert footer.is_attribution_tab_displayed
    assert footer.is_more_information_tab_displayed

    # The header is no longer pinned
    assert 'pinned' not in content_header.root.get_attribute('class')


@markers.webview
@markers.test_case('C176238', 'C176239', 'C176240', 'C176245')
@markers.nondestructive
def test_navigation(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[0]
    content = book.click_book_cover()
    header_nav = content.header_nav
    toc = header_nav.click_contents_button()
    num_pages = toc.number_of_pages

    assert type(content) == Content
    assert content.chapter_section == '1'
    # Preface is skipped by default
    assert header_nav.progress_bar_fraction_is(2 / num_pages)

    # WHEN we navigate next twice and then back twice using the header and footer controls
    content = content.header_nav.click_next_link()
    assert type(content) == Content
    assert content.chapter_section == '1.1'
    assert header_nav.progress_bar_fraction_is(3 / num_pages)

    content = content.footer_nav.click_next_link()
    assert type(content) == Content
    assert content.chapter_section == '1.2'
    assert header_nav.progress_bar_fraction_is(4 / num_pages)

    content = content.footer_nav.click_back_link()
    assert type(content) == Content
    assert content.chapter_section == '1.1'
    assert header_nav.progress_bar_fraction_is(3 / num_pages)

    content = content.header_nav.click_back_link()

    # THEN we arrive back at the initial page
    assert type(content) == Content
    assert content.chapter_section == '1'
    assert header_nav.progress_bar_fraction_is(2 / num_pages)


@markers.webview
@markers.test_case('C195073')
@markers.slow
@markers.nondestructive
def test_ncy_is_not_displayed(american_gov_url, selenium):
    # GIVEN An American Government URL and Selenium driver

    # WHEN The page is fully loaded using the URL
    page = Content(selenium, american_gov_url).open()

    # THEN :NOT_CONVERTED_YET is not displayed
    assert page.is_ncy_displayed is False


@markers.webview
@markers.test_case('C132547', 'C132548', 'C162195')
@markers.nondestructive
@markers.parametrize(
    'page_uuid,is_baked_book_index',
    [('d50f6e32-0fda-46ef-a362-9bd36ca7c97d:72a3ef21-e30b-5ba4-9ea6-eac9699a2f09', True),
     ('b3c1e1d2-839c-42b0-a314-e119a8aafbdd', False)]
)
def test_id_links_and_back_button(page_uuid, is_baked_book_index, webview_base_url, selenium):
    # GIVEN an index page in a baked book or a page with anchor links in an unbaked book
    content_page = Content(selenium, webview_base_url, id=page_uuid).open()
    content_url = selenium.current_url
    assert '#' not in content_url

    # WHEN we click on a term (baked index) or an anchor link
    content_region = content_page.content_region
    if is_baked_book_index:
        content_page = content_region.click_index_term()
    else:
        content_page = content_region.click_anchor_link()
        assert selenium.current_url.startswith(content_url)

    # THEN we end up at the linked page and the element with the same id as the link is displayed
    new_url = selenium.current_url
    assert '#' in new_url
    assert not new_url.endswith('#')
    id = re.search('#(.+)$', new_url)[1]
    assert content_page.is_element_displayed(By.ID, id)

    # WHEN we click the browser's back button
    selenium.back()

    # THEN we end up at the previous page
    assert selenium.current_url == content_url
