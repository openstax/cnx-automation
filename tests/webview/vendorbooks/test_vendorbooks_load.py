import requests
from tests import markers
from pages.webview.home import Home


@markers.vendor
@markers.test_case("C593141")
@markers.nondestructive
def test_vendor_books_not_redirecting(vendor_base_url, selenium):

    home = Home(selenium, vendor_base_url).open()
    books = []

    # GIVEN the openstax list
    for op_book in home.featured_books.openstax_list:

        books.append(op_book.title)

    for book_title in books:

        home = Home(selenium, vendor_base_url).open()

        # using selenium fixture to overcome stale element exception occurring with page objects
        title_link = selenium.find_element_by_link_text(book_title)
        title_link.click()

        current_url = home.current_url
        data = requests.get(current_url)

        assert vendor_base_url in current_url
        assert 200 == data.status_code
