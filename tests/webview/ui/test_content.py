# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import re
from urllib.parse import urljoin
from requests import get
from time import sleep
from datetime import datetime

from pages.webview.about_this_book import AboutBook
from pages.webview.content_page import ContentPage
from tests import markers

from pages.webview.home import Home
from pages.webview.content import Content
from tests.utils import similar


@markers.webview
@markers.test_case("C193738")
@markers.nondestructive
@markers.parametrize(
    "is_archive,path,expected_response_status_code",
    [
        # FIXME Requires varnish
        # (False, '/content/col23946', 301),
        (True, "/content/col23946", 301),
        # FIXME Requires varnish
        # (False, '/content/col23946/1.1', 301),
        (True, "/content/col23946/1.1", 301),
        (False, "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e", 200),
        (True, "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e", 302),
        (
            False,
            (
                "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e"
                ":7d039be2-93c6-4f32-a469-41689bab7225"
            ),
            200,
        ),
        (
            True,
            (
                "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e"
                ":7d039be2-93c6-4f32-a469-41689bab7225"
            ),
            302,
        ),
        (False, "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e@1.1", 200),
        (True, "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e@1.1", 200),
        (
            False,
            (
                "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e@1.1"
                ":7d039be2-93c6-4f32-a469-41689bab7225"
            ),
            200,
        ),
        (
            False,
            (
                "/contents/4eaa8f03-88a8-485a-a777-dd3602f6c13e@1.1"
                ":7d039be2-93c6-4f32-a469-41689bab7225@5"
            ),
            200,
        ),
        (False, "/contents/TqqPA4io", 200),
        (True, "/contents/TqqPA4io", 302),
        (False, "/contents/TqqPA4io:fQOb4pPG", 200),
        (True, "/contents/TqqPA4io:fQOb4pPG", 302),
        (False, "/contents/TqqPA4io@1.157", 200),
        (True, "/contents/TqqPA4io@1.157", 301),
        (False, "/contents/TqqPA4io@1.157:fQOb4pPG", 200),
        (True, "/contents/TqqPA4io@1.157:fQOb4pPG", 301),
        (False, "/contents/TqqPA4io@1.157:fQOb4pPG@5", 200),
        (True, "/contents/TqqPA4io@1.157:fQOb4pPG@5", 301),
    ],
)
def test_content_status_codes(
    webview_base_url, archive_base_url, is_archive, path, expected_response_status_code
):
    # GIVEN some URL and the expected redirect code
    if is_archive:
        url = urljoin(archive_base_url, path)
    else:
        url = urljoin(webview_base_url, path)

    # WHEN we visit the URL
    # NOTE: Don't bother trying to get status codes using Selenium
    # https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/141
    response = get(url, allow_redirects=False)

    # THEN we get the expected redirect code
    assert response.status_code == expected_response_status_code


@markers.webview
@markers.test_case("C194465")
@markers.nondestructive
@markers.parametrize(
    "id",
    [
        "FqtblkWY@2.1:E3XenWEQ",
        "FqtblkWY@2.1:E3XenWEQ@2",
        "FqtblkWY@2.1:rKBtkIWG@2",
        "TqqPA4io@1.1:fQOb4pPG@2",
    ],
)
def test_canonical_link_is_correct(webview_base_url, selenium, id):
    # GIVEN a book's content page
    content = Content(selenium, webview_base_url, id=id).open()
    section_title = content.section_title

    # WHEN the book's canonical url is visited
    selenium.get(content.canonical_url)
    content.wait_for_page_to_load()

    # THEN we end up in the same page
    # NOTE: we check the section title instead of the url because the canonical link seems to
    #       take us to the latest version of the content, no matter which version we started on
    # NOTE: Newer versions of the book may not have the section number. For this we check in the
    #       section_title string instead of an equality.
    assert content.section_title in section_title


@markers.webview
@markers.test_case("C176232", "C176233")
@markers.nondestructive
def test_navs_and_elements_are_displayed(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[59]
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
    section_title_div_location = content.section_title_div_location
    section_title_div_size = content.section_title_div_size

    # Section title inside main content section
    assert section_title_div_location["x"] >= main_content_section.location["x"]
    assert section_title_div_location["y"] >= main_content_section.location["y"]
    assert (
        section_title_div_location["x"] + section_title_div_size["width"]
        <= main_content_section.location["x"] + main_content_section.size["width"]
    )
    assert (
        section_title_div_location["y"] + section_title_div_size["height"]
        <= main_content_section.location["y"] + main_content_section.size["height"]
    )

    # Section title on top of main content section
    assert (
        section_title_div_location["y"] - main_content_section.location["y"]
        <= section_title_div_size["height"]
    )


@markers.webview
@markers.test_case("C132542")
@markers.nondestructive
def test_author_contains_openstax(webview_base_url, selenium):
    # GIVEN the home page and a book
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]

    # WHEN the book's cover is clicked
    content = book.click_book_cover()

    # THEN the displayed author is OpenStax
    content_header = content.content_header
    assert content_header.is_book_by_displayed
    assert content_header.are_authors_displayed
    assert "OpenStax" in content_header.authors


@markers.webview
@markers.test_case("C176242")
@markers.nondestructive
def test_toc_is_displayed(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()

    # WHEN the contents button is clicked
    content.header_nav.click_contents_button()
    toc = content.table_of_contents

    # THEN the table of contents is displayed
    assert toc.is_displayed
    assert toc.number_of_chapters > 0
    assert toc.number_of_pages > 0


@markers.webview
@markers.smoke
@markers.test_case("C176243", "C176244")
@markers.nondestructive
def test_toc_navigation(webview_base_url, selenium):
    # GIVEN a book's table of contents
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()
    content.header_nav.click_contents_button()
    toc = content.table_of_contents

    # WHEN a chapter is expanded and we navigate to one of its pages
    chapter = toc.chapters[0]
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
@markers.smoke
@markers.test_case("C176257")
@markers.nondestructive
def test_share_on_top_right_corner(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()

    # THEN social share links are displayed in the top right corner
    share = content.share
    assert share.is_displayed
    assert share.is_facebook_share_link_displayed
    assert share.is_twitter_share_link_displayed
    root = content.share.root
    # Top half
    assert root.location["y"] + root.size["height"] < selenium.get_window_size()["height"] / 2
    # Right half
    assert root.location["x"] > selenium.get_window_size()["width"] / 2


@markers.webview
@markers.smoke
@markers.test_case("C132549", "C175148")
@markers.nondestructive
@markers.parametrize(
    "uuid,query,has_results,result_index,has_os_figures,has_os_tables",
    [
        (
            "36004586-651c-4ded-af87-203aca22d946",
            "mitosis genetics gorilla",
            False,
            None,
            None,
            None,
        ),
        ("bb62933e-f20a-4ffc-90aa-97b36c296c3e", "Fizyka", True, 1, True, False),
        ("bb62933e-f20a-4ffc-90aa-97b36c296c3e", "Tabela", True, 3, True, True),
    ],
)
def test_in_book_search(
    webview_base_url,
    selenium,
    uuid,
    query,
    has_results,
    result_index,
    has_os_figures,
    has_os_tables,
):
    # GIVEN a book's content page and a query
    content = Content(selenium, webview_base_url, id=uuid).open()

    # WHEN we search the book for the given query
    search_results = content.header_nav.search(query)

    # THEN search results are present (or not) and bolded and link to the matching content
    results = search_results.results
    result_count = search_results.result_count
    assert len(results) == result_count

    if not has_results:
        assert result_count == 0
        return

    assert result_count > 0

    words = query.split()
    for result in results:
        for word in words:
            assert result.count_occurrences(word) == result.count_bold_occurrences(word)

    result = results[result_index]
    title = result.title
    content = result.click_link()
    assert content.section_title == title

    content_region = content.content_region

    assert content_region.has_os_figures == has_os_figures
    for figure in content_region.os_figures:
        assert figure.caption.is_labeled
        assert figure.caption.is_numbered

    assert content_region.has_os_tables == has_os_tables
    for table in content_region.os_tables:
        assert table.caption.is_labeled
        assert table.caption.is_numbered


@markers.webview
@markers.smoke
@markers.test_case("C176258", "C176259", "C176261")
@markers.nondestructive
def test_share_links_displayed(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN a book is clicked
    book = home.featured_books.openstax_list[32]
    content = book.click_book_cover()

    # THEN social share links have the expected urls
    current_url = selenium.current_url
    share = content.share

    expected_facebook_url = f"https://facebook.com/sharer/sharer.php?u={current_url}"
    assert share.facebook_share_url == expected_facebook_url

    expected_twitter_url = f"https://twitter.com/share?url={current_url}"
    assert expected_twitter_url in share.twitter_share_url

    expected_linkedin_url = f"https://www.linkedin.com/shareArticle?mini=true&url={current_url}"
    assert expected_linkedin_url in share.linkedin_share_url


@markers.webview
@markers.test_case("C193880")
@markers.nondestructive
@markers.parametrize("id", ["u2KTPvIK@3.30:qVb4K8xR@3"])
def test_newer_version_leads_to_correct_page(webview_base_url, selenium, id):
    # GIVEN the content page
    content = Content(selenium, webview_base_url, id=id).open()
    version = content.book_version
    section_title = content.section_title

    # WHEN the newer version link is clicked
    content = content.click_newer_version_link()

    # THEN we end up in a newer version of the same page
    assert content.section_title == section_title
    assert content.book_version > version


@markers.webview
@markers.smoke
@markers.test_case("C176234")
@markers.nondestructive
def test_get_this_book(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[32]
    content = book.click_book_cover()

    # WHEN we click the "Get This Book!" button
    button_displayed = content.is_get_this_book_button_displayed
    if button_displayed:
        get_this_book = content.click_get_this_book_button()
        pdf_displayed = get_this_book.is_pdf_link_displayed
        offline_zip_displayed = get_this_book.is_offline_zip_link_displayed

    # THEN links to download the pdf, epub and offline zip versions are displayed
    # Look at the footer to see which downloads should have been available
    downloads = content.content_footer.click_downloads_tab()

    if not button_displayed:
        assert not downloads.is_any_available
        pytest.skip('No files available to download: "Get This Book!" button not present.')
    else:
        assert pdf_displayed or offline_zip_displayed

    # Check the footer
    if pdf_displayed:
        assert downloads.is_pdf_available

    if offline_zip_displayed:
        assert downloads.is_offline_zip_available


@markers.webview
@markers.smoke
@markers.test_case("C195074")
@markers.nondestructive
@markers.parametrize("id", ["u2KTPvIK@3.1:Zv6FJYpb@3"])
def test_page_with_unicode_characters_in_title_loads(webview_base_url, selenium, id):
    # GIVEN the webview base url, the Selenium driver and the id of a page whose title has unicode
    content = Content(selenium, webview_base_url, id=id)

    # WHEN we load the content page
    content = content.open()

    # Ensure it has a figure element
    assert content.content_region.has_figures

    # THEN the page does not reload afterwards
    # Wait 10 seconds to see if the page reloads
    sleep(10)
    # If we don't get a StaleElementReferenceException then the page didn't reload
    assert content.content_region.os_figures


@markers.xfail
@markers.webview
@markers.smoke
@markers.test_case("C176236")
@markers.nondestructive
def test_content_and_figures_display_after_scrolling(webview_base_url, selenium):

    # This is expected to fail as we ran out non-redirecting collections
    # with figures on the main page

    # GIVEN a book's content page with figures
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[60]
    content_page = book.click_book_cover()
    content_region = content_page.content_region
    assert not content_region.is_blank
    assert content_region.has_figures

    # WHEN we scroll to a figure
    figure = content_region.figures[0]
    content_region.scroll_to(figure)

    # THEN some figure is displayed
    assert figure.is_displayed()


@markers.webview
@markers.smoke
@markers.test_case("C176235", "C176237")
@markers.nondestructive
def test_nav_and_menus_display_after_scrolling(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()
    content_header = content.content_header
    original_content_header_y = content_header.root.location["y"]

    # WHEN we scroll to the bottom
    content.footer.scroll_to()
    content_footer = content.content_footer

    # THEN - the header nav is offscreen but still considered displayed
    #      - the content nav is displayed on top without the site navbar or any social links
    assert content.header.is_nav_displayed

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

    # The footer is displayed at the bottom
    assert content_footer.is_displayed
    assert content_footer.is_downloads_tab_displayed
    assert content_footer.is_history_tab_displayed
    assert content_footer.is_attribution_tab_displayed
    assert content_footer.is_more_information_tab_displayed

    # Hard to check that the content_header is on top after scrolling, but we can check
    # that it at least has the pinned class and is above the footer
    assert content_header.is_pinned
    assert not content_header.is_opened
    assert not content_header.is_closed
    assert content_header.root.location["y"] > original_content_header_y
    assert content_header.root.location["y"] < content_footer.root.location["y"]


@markers.webview
@markers.smoke
@markers.test_case("C195232")
@markers.nondestructive
@markers.parametrize("width,height", [(480, 640)])
def test_mobile_nav_and_menus_hide_after_scrolling(webview_base_url, selenium, width, height):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()
    content_header = content.content_header
    original_content_header_y = content_header.root.location["y"]

    # WHEN we scroll to the bottom
    content.footer.scroll_to()

    # THEN - the header nav is offscreen but still considered displayed
    #      - the content nav is offscreen without the site navbar or any social links
    assert content.header.is_nav_displayed

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

    assert not content_header.is_pinned
    assert content_header.root.location["y"] == original_content_header_y

    # WHEN we scroll up
    content.scroll_up()

    # THEN - the header nav is offscreen but still considered displayed
    #      - the content nav is now pinned and onscreen without the site navbar or any social links
    assert content.header.is_nav_displayed

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

    assert content_header.is_pinned
    assert content_header.is_opened
    assert not content_header.is_closed
    previous_content_header_y = content_header.root.location["y"]
    assert previous_content_header_y > original_content_header_y

    # WHEN we scroll down again
    content.scroll_down()

    # THEN - the header nav is offscreen but still considered displayed
    #      - the content nav is now closed and offscreen without the site navbar or any social links
    assert content.header.is_nav_displayed

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

    assert content_header.is_pinned
    assert not content_header.is_opened
    assert content_header.is_closed
    assert content_header.root.location["y"] > previous_content_header_y


@markers.webview
@markers.smoke
@markers.test_case("C162171")
@markers.nondestructive
def test_attribution(webview_base_url, selenium):
    # GIVEN a book's content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()

    # WHEN we click the attribution tab
    attribution = content.content_footer.click_attribution_tab()

    # THEN the attribution is displayed and has the correct support email
    assert attribution.is_displayed
    expected_sentence = "For questions regarding this license, please contact support@openstax.org."
    assert expected_sentence in attribution.text


@markers.webview
@markers.smoke
@markers.test_case("C176241")
@markers.nondestructive
def test_back_to_top(webview_base_url, selenium):
    # GIVEN a book's scrolled content page
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()
    footer = content.content_footer
    content_header = content.content_header
    original_content_header_y = content_header.root.location["y"]

    # WHEN we scroll to the bottom then click the back to top link
    content = footer.nav.click_back_to_top_link()

    # THEN the content page is no longer scrolled
    assert content.header.is_nav_displayed

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

    # The footer is offscreen, but still considered displayed
    assert footer.is_displayed
    assert footer.is_downloads_tab_displayed
    assert footer.is_history_tab_displayed
    assert footer.is_attribution_tab_displayed
    assert footer.is_more_information_tab_displayed

    # The header is no longer pinned
    assert not content_header.is_pinned
    assert content_header.root.location["y"] == original_content_header_y


@markers.webview
@markers.smoke
@markers.test_case("C176238", "C176239", "C176240", "C176245")
@markers.nondestructive
def test_navigation(webview_base_url, selenium):
    # GIVEN a book's content page and a sim_ratio
    sim_ratio = 0.4
    home = Home(selenium, webview_base_url).open()
    book = home.featured_books.openstax_list[59]
    content = book.click_book_cover()
    header_nav = content.header_nav
    header_nav.click_contents_button()
    toc = content.table_of_contents
    num_pages = toc.number_of_pages

    assert type(content) == Content
    # Introduction should be the first section loaded
    assert (
        content.section_title == "Introduction"
        or similar(content.section_title, "📎 Inquiry Organizer") > sim_ratio
    )
    # Preface is skipped by default
    assert header_nav.progress_bar_fraction_is(2 / num_pages)

    # WHEN we navigate next twice and then back twice using the header and footer controls
    content = content.header_nav.click_next_link()
    assert type(content) == Content
    assert content.chapter_section == "1.2"
    assert header_nav.progress_bar_fraction_is(3 / num_pages)

    content = content.footer_nav.click_next_link()
    assert type(content) == Content
    assert content.chapter_section == "1.3"
    assert header_nav.progress_bar_fraction_is(4 / num_pages)

    content = content.footer_nav.click_back_link()
    assert type(content) == Content
    assert content.chapter_section == "1.2"
    assert header_nav.progress_bar_fraction_is(3 / num_pages)

    content = content.header_nav.click_back_link()

    # THEN we arrive back at the initial page

    assert header_nav.progress_bar_fraction_is(2 / num_pages)


@markers.webview
@markers.test_case("C195073")
@markers.slow
@markers.nondestructive
def test_ncy_is_not_displayed(webview_base_url, american_gov_uuid, selenium):
    # GIVEN the webview base url, an American Government content page UUID, and the Selenium driver

    # WHEN the page is fully loaded using the URL
    page = Content(selenium, webview_base_url, id=american_gov_uuid).open()

    # THEN :NOT_CONVERTED_YET is not displayed
    assert page.is_ncy_displayed is False


@markers.webview
@markers.test_case("C132547", "C132548")
@markers.nondestructive
@markers.parametrize(
    "page_uuid,is_baked_book_index",
    [
        ("bb62933e-f20a-4ffc-90aa-97b36c296c3e:85036aed-fa1a-5d51-a9c2-c07ee673488d", True),
        ("6a0568d8-23d7-439b-9a01-16e4e73886b3", False),
    ],
)
def test_id_links_and_back_button(page_uuid, is_baked_book_index, webview_base_url, selenium):
    # GIVEN an index page in a baked book or a page with anchor links in an unbaked book
    content_page = Content(selenium, webview_base_url, id=page_uuid).open()
    content_url = content_page.current_url
    assert "#" not in content_url

    # WHEN we click on a term (baked index) or an anchor link
    content_region = content_page.content_region
    if is_baked_book_index:
        content_page = content_region.click_index_term()
    else:
        content_page = content_region.click_anchor_link(internal_only=True)
        assert content_page.current_url.startswith(content_url)

    # THEN we end up at the linked page and the element with the same id as the link is displayed
    new_url = content_page.current_url
    assert "#" in new_url
    id = re.search("#(.+)$", new_url)[1]
    assert id
    assert content_page.is_element_id_displayed(id)

    # WHEN we click the browser's back button
    content_page.back()

    # THEN we end up at the previous page
    assert content_page.current_url == content_url


@markers.webview
@markers.test_case("C181754")
@markers.nondestructive
@markers.parametrize(
    "ch_review_id", ["u2KTPvIK@3.32:6IrsWVCW", pytest.param("u2KTPvIK@3.32:aVXUrOzZ")]
)
def test_chapter_review_version_matches_book_version(webview_base_url, selenium, ch_review_id):
    # GIVEN the webview base url, a chapter review id, and the Selenium driver

    # WHEN we visit the chapter review page
    content = Content(selenium, webview_base_url, id=ch_review_id).open()

    # THEN the chapter review version matches the book version
    assert content.page_version == content.book_version


@markers.webview
@markers.smoke
@markers.test_case("C195064")
@markers.nondestructive
@markers.parametrize("ch_review_id", ["e5fbbjPE"])
def test_books_containing_go_to_book_link(webview_base_url, selenium, ch_review_id):
    # GIVEN the webview base url, a chapter review id, and the Selenium driver
    content = ContentPage(selenium, webview_base_url, id=ch_review_id).open()
    books = content.books_containing.book_list

    # WHEN we click the link to the first book
    title = books[0].title

    book = books[0].click_go_to_book_link

    # THEN we are on the About this Book page and it is displayed
    assert type(book) == AboutBook
    assert book.about_this_book_section.is_displayed
    assert book.title == title


@markers.webview
@markers.test_case("C195063")
@markers.nondestructive
@markers.parametrize("ch_review_id", ["SjdU64Og@3"])
def test_books_containing_have_revised_date(webview_base_url, selenium, ch_review_id):
    # GIVEN the webview base url, a chapter review id, and the Selenium driver

    # WHEN the content_page is fully loaded and we have a list of books containing the page
    content = ContentPage(selenium, webview_base_url, id=ch_review_id).open()
    books = content.books_containing.book_list

    # THEN all the Books should contain revision date
    for book in books:
        assert book.revision_date.is_displayed


@markers.webview
@markers.requires_complete_dataset
@markers.test_case("C195061")
@markers.nondestructive
@markers.parametrize("page_id", ["BWYBGK7C@2"])
def test_books_containing_title_not_limited(webview_base_url, selenium, page_id):
    # GIVEN the webview base url, page_id, and the Selenium driver

    # WHEN we visit that page of the chapter and we have a list of books containing the page
    content = ContentPage(selenium, webview_base_url, id=page_id).open()

    books = content.books_containing.book_list

    # THEN the title of the books are not truncated by ellipses
    for book in books:
        assert "..." not in book.title


@markers.webview
@markers.requires_complete_dataset
@markers.test_case("C195057", "C195058", "C195059", "C195072")
@markers.nondestructive
@markers.parametrize("page_id", ["mjO9LQWq@1", "bJs8AcSE@1", "4fGVMb7P@1"])
def test_books_containing_message_is_correct(webview_base_url, selenium, page_id):
    # GIVEN the webview base url, page_id, and the Selenium driver

    # WHEN we visit the content page
    # AND  we have a books containing count
    # AND  we have the overview message
    content = ContentPage(selenium, webview_base_url, id=page_id).open()

    book_count = len(content.books_containing.book_list)
    overview = content.books_containing.overview

    # THEN ensure the proper books containing overview message is displayed
    if book_count > 1:
        assert overview == f"This page is in {book_count} books:"
    elif book_count > 0:
        assert overview == "This page is in this book:"
    else:
        assert overview == "This page is not in any books."


@markers.webview
@markers.test_case("C195062")
@markers.nondestructive
@markers.parametrize("page_id", ["SjdU64Og@3"])
def test_books_containing_have_authors(webview_base_url, selenium, page_id):
    # GIVEN the webview base url, page_id, and the Selenium driver

    # WHEN we visit that page of the chapter and we have a list of books containing page
    content = ContentPage(selenium, webview_base_url, id=page_id).open()

    books = content.books_containing.book_list

    # THEN the authors of the book should be displayed
    for book in books:
        assert book.author.is_displayed()


@markers.webview
@markers.requires_complete_dataset
@markers.test_case("C195065")
@markers.nondestructive
@markers.parametrize("page_id", ["HOATLqlR@5"])
def test_books_containing_list_in_sorted_order(webview_base_url, selenium, page_id):
    # GIVEN the webview base url, page_id, and the Selenium driver

    # WHEN we visit that page of the chapter and we have a list of books containing page
    content = Content(selenium, webview_base_url, id=page_id).open()

    # AND store the main author
    main_author = content.content_header.authors

    # AND Save list of authors and dates
    content = ContentPage(selenium, webview_base_url, id=page_id).open()
    dates = content.books_containing.date_list
    author = content.books_containing.author_list

    # THEN main author should be the author of the first book listed
    assert author[0][0] == main_author

    # AND if there are more books with main author, they should be listed first
    i = 1
    while i < len(author) - 1 and author[i][0] == main_author:
        i += 1

    # AND for the rest of the books, the revision dates are sorted in decreasing order
    date_list = []
    for date in dates[i:]:
        date_list.append(datetime.strptime(date[0], "%b %d, %Y"))
    assert date_list == sorted(date_list, reverse=True)


@markers.webview
@markers.smoke
@markers.requires_complete_dataset
@markers.test_case("C195055")
@markers.nondestructive
@markers.parametrize("page_id", ["4fGVMb7P@1"])
def test_books_containing_button_toggles_and_labelled_books(webview_base_url, selenium, page_id):
    # GIVEN the webview base url, page_id, and the Selenium driver

    # WHEN we visit a single content page (not a book)
    content = ContentPage(selenium, webview_base_url, id=page_id).open()
    books_containing = content.books_containing

    # THEN the button that opens and closes the "ToC" is labelled "Books" instead of "Contents"
    # AND the button opens and closes the "This page is in # books" side nav
    contents_button = content.header_nav.contents_button
    assert contents_button.text == "Books"

    # The side nav area should be open by default
    assert books_containing.is_displayed

    content.header_nav.click_contents_button()
    assert not books_containing.is_displayed

    content.header_nav.click_contents_button()
    content.books_containing.wait_for_region_to_display()
    assert books_containing.is_displayed


@markers.webview
@markers.requires_complete_dataset
@markers.test_case("C195054")
@markers.nondestructive
@markers.parametrize("page_id", ["4fGVMb7P@1"])
def test_books_containing_list_is_on_left_of_page(webview_base_url, selenium, page_id):
    # GIVEN the webview base url, page_id, and the Selenium driver

    # WHEN we load the page of the chapter and we have the width of the window
    content = ContentPage(selenium, webview_base_url, id=page_id).open()
    window_width = content.get_window_size("width")

    # THEN check if the books list exists and on the left
    assert content.books_containing.book_list
    assert content.location["x"] < window_width / 2


@markers.webview
@markers.smoke
@markers.requires_complete_dataset
@markers.test_case("C195056")
@markers.nondestructive
@markers.parametrize("page_id", ["QlYg2VHd"])
@markers.parametrize("width,height", [(1024, 768), (630, 480)])
def test_button_open_with_certain_window_size(webview_base_url, selenium, page_id, width, height):
    # GIVEN the webview base url, page_id, and the Selenium driver

    # WHEN we visit that page of the chapter and we have a list of books containing the page
    content = ContentPage(selenium, webview_base_url, id=page_id).open()

    # THEN if window width >= 640, button should be open
    if width >= 640:
        assert content.books_containing.overview_is_displayed
    # AND if window width < 640, button should be closed
    else:
        assert not content.books_containing.overview_is_displayed


@markers.webview
@markers.test_case("C195060")
@markers.nondestructive
@markers.parametrize("id", ["4fGVMb7P@1"])
@markers.parametrize("highlight_color", ["#78b04a"])
def test_book_title_link_and_highlight_on_view(webview_base_url, id, selenium, highlight_color):
    # GIVEN the webview base url, a chapter page id, the color and the Selenium driver

    # WHEN we visit that page of the chapter
    content = ContentPage(selenium, webview_base_url, id=id).open()
    content_page_title = content.title

    # AND click the title
    content.books_containing.book_list[0].click_title_link()

    # AND get and click the Contents button
    content.header_nav.click_contents_button()

    # AND find the on viewing title and get the color
    active_color = content.table_of_contents.active_page_color

    # THEN make sure the section matches the original page title and the highlight color is correct
    assert content_page_title == content.section_title_without_chapter_section
    assert active_color == highlight_color
