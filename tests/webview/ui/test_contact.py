# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.webview.home import Home

from tests import markers


@markers.webview
@markers.nondestructive
def test_contact_has_location_map(base_url, selenium):
    # GIVEN the About Us page
    home = Home(selenium, base_url).open()
    about_us = home.header.click_about_us()

    # WHEN the contact link in the navbar is clicked
    contact = about_us.click_contact()

    # THEN a map of the location of OpenStax is displayed
    assert contact.contact_content.is_map_displayed
