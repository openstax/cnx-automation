# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.webview.home import Home

from tests import markers


@markers.webview
@markers.nondestructive
def test_about_us_links_are_positioned_properly(base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, base_url).open()

    # WHEN the About Us link in the navbar is clicked
    about_us_page = home.header.click_about_us()

    # THEN the about us and contact links are same size
    # and vertically stacked on the left of the page
    about_us = about_us_page.about_us_link
    contact = about_us_page.contact_link
    # Same size
    assert about_us.size == contact.size
    # Stacked:
    # Same x
    assert about_us.location['x'] == contact.location['x']
    # Similar y
    assert (about_us.location['y'] + about_us.size['height'] <
            contact.location['y'] <
            about_us.location['y'] + 2 * about_us.size['height'])
    # On the left
    assert about_us.location['x'] + about_us.size['width'] < selenium.get_window_size()['width']/2
