# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.webview.home import Home


@markers.webview
@markers.test_case('C176262')
@markers.nondestructive
def test_donate_redirects_to_openstax_org(webview_base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN the Give link is clicked and redirects to openstax.org
    donate = home.header.click_donate()
    assert donate.is_openstax_org_give_page
