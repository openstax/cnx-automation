from tests import markers
from pages.webview.home import Home


@markers.webview
@markers.test_case("C553080")
@markers.nondestructive
def test_book_cover_loads_correct_page(
    webview_base_url, selenium, rex_base_url, rex_released_books
):

    # GIVEN the webview base url, the Selenium driver, and rex released books list
    for allbooks in rex_released_books:

        home = Home(selenium, webview_base_url).open()

        for book in home.featured_books.openstax_list:

            # WHEN book id is a rex released book
            if book.cnx_id in allbooks:

                book_title = book.title

                link_elem = home.selenium.find_element_by_link_text(book_title)
                link_elem.click()

                current_url = home.selenium.current_url

                # THEN compare the title from the home page and the content page
                assert rex_base_url in current_url
                break

        else:
            assert False, f"{allbooks} not a rex book"
