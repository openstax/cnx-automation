from tests import markers
from pages.webview.content import Content
from pages.webview.home import Home
import requests


@markers.vendor
@markers.test_case("C593142")
@markers.nondestructive
def test_vendor_pages_load(vendor_base_url, selenium, openstax_all_books_uuids):

    home = Home(selenium, vendor_base_url).open()

    vendor_content = Content(selenium, vendor_base_url, id=openstax_all_books_uuids).open()

    content = vendor_content.open()
    content.header_nav.click_contents_button()
    toc = content.table_of_contents

    # testing American Government 2e book as it requires different indexing
    if openstax_all_books_uuids == "9d8df601-4f12-4ac1-8224-b450bf739e5f":

        # WHEN a chapter is expanded and we navigate to one of its pages
        chapter = toc.chapters[2]
        chapter = chapter.click()
        page = chapter.pages[0]
        title = page.title
        content = page.click()

        # THEN we end up at the correct page
        current_url = home.current_url
        data = requests.get(current_url)

        assert vendor_base_url in current_url, "vendor_base_url is NOT in current_url"
        assert 200 == data.status_code, "status code is NOT 200"
        assert content.section_title == title, "section titles does NOT match"

    elif (
        openstax_all_books_uuids == "4eaa8f03-88a8-485a-a777-dd3602f6c13e"
        or openstax_all_books_uuids == "16ab5b96-4598-45f9-993c-b8d78d82b0c6"
        or openstax_all_books_uuids == "bb62933e-f20a-4ffc-90aa-97b36c296c3e"
    ):
        # testing 3 Polish books as I cannot find appropriate indexes
        selenium.find_element_by_link_text("Rozwiązania zadań").click()

        current_url = home.current_url
        data = requests.get(current_url)

        assert vendor_base_url in current_url, "vendor_base_url is NOT in current_url"
        assert 200 == data.status_code, "status code is NOT 200"

    else:
        # checking rest of the books that title and chapter/pages redirects

        # WHEN a chapter is expanded and we navigate to one of its pages
        chapter = toc.chapters[1]
        chapter = chapter.click()
        page = chapter.pages[1]
        title = page.title
        content = page.click()

        # THEN we end up at the correct page
        current_url = home.current_url
        data = requests.get(current_url)

        assert vendor_base_url in current_url, "vendor_base_url is NOT in current_url"
        assert 200 == data.status_code, "status code is NOT 200"
        assert content.section_title == title, "section titles does NOT match"
