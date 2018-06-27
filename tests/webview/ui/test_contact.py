# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.webview.home import Home

from tests import markers


@markers.webview
@markers.test_case('C176254', 'C176255')
@markers.nondestructive
def test_contact_has_correct_email_link(webview_base_url, selenium):
    # GIVEN the About Us page
    home = Home(selenium, webview_base_url).open()
    about_us = home.header.click_about_us()

    # WHEN the contact link in the navbar is clicked
    contact = about_us.click_contact()

    # THEN the contact email is displayed
    contact_content = contact.contact_content
    assert contact_content.is_email_displayed
    assert contact_content.email_url == 'mailto:support@openstax.org'


@markers.webview
@markers.test_case('C176253')
@markers.nondestructive
def test_contact_has_location_map(webview_base_url, selenium):
    # GIVEN the About Us page
    home = Home(selenium, webview_base_url).open()
    about_us = home.header.click_about_us()

    # WHEN the contact link in the navbar is clicked
    contact = about_us.click_contact()

    # THEN a map of the location of OpenStax is displayed
    assert contact.contact_content.is_map_displayed


@markers.webview
@markers.test_case('C176256')
@markers.nondestructive
def test_contact_has_correct_headers(webview_base_url, selenium):
    # GIVEN the About Us page
    home = Home(selenium, webview_base_url).open()
    about_us = home.header.click_about_us()

    # WHEN the contact link in the navbar is clicked
    contact = about_us.click_contact()

    # THEN the Questions?, Technical Support and General Questions headers are displayed
    assert contact.contact_content.questions_header.text == 'Questions?'
    assert contact.contact_content.technical_support_header.text == 'Technical Support'
    assert contact.contact_content.general_questions_header.text == 'General Questions'
