# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers
from pages.webview.content import Content
from pages.webview.home import Home
import requests
import pytest


@markers.vendor
@markers.test_case("C593142")
@markers.nondestructive
def test_vendor_pages_load(vendor_base_url, selenium, openstax_allbooks_uuids):

    home = Home(selenium, vendor_base_url).open()

    content1 = Content(selenium, vendor_base_url, id=openstax_allbooks_uuids).open()

    print("\nBOOK TITLE  : ", content1.title)

    if (
        openstax_allbooks_uuids == "4eaa8f03-88a8-485a-a777-dd3602f6c13e"
        or openstax_allbooks_uuids == "16ab5b96-4598-45f9-993c-b8d78d82b0c6"
        or openstax_allbooks_uuids == "bb62933e-f20a-4ffc-90aa-97b36c296c3e"
        or openstax_allbooks_uuids == "9d8df601-4f12-4ac1-8224-b450bf739e5f"
    ):
        pytest.skip()
    else:
        content = content1.open()
        content.header_nav.click_contents_button()
        toc = content.table_of_contents

        # WHEN a chapter is expanded and we navigate to one of its pages
        chapter = toc.chapters[1]
        chapter = chapter.click()
        page = chapter.pages[1]
        title = page.title
        print("PAGE TITLE  : ", title)
        content = page.click()

        # THEN we end up at the correct page
        current_url = home.current_url

        print("CURRENT URL : ", current_url)

        data = requests.get(current_url)

        assert vendor_base_url in current_url, "vendor_base_url is NOT in current_url"
        assert 200 == data.status_code, "status code is NOT 200"
        assert content.section_title == title, "section titles does NOT match"
