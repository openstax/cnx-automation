# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import Home


@pytest.mark.nondestructive
def test_search_items_are_displayed(base_url, selenium):
    # GIVEN The base_url and Selenium driver

    # WHEN The home page URL is fully loaded,
    #      and the browse link in the navbar is clicked
    page = Home(selenium, base_url).open()
    browse_page = page.header.click_browse()

    # THEN The search bar and the advanced search button is displayed
    assert browse_page.is_search_input_displayed
    assert browse_page.is_advanced_search_button_displayed


@pytest.mark.nondestructive
def test_subject_categories_load(base_url, selenium):
    # GIVEN the base_url and Selenium driver

    # When The homepage URL is fully loaded,
    #      and the browse link in the navbar is clicked
    page = Home(selenium, base_url).open()
    browse_page = page.header.click_browse()

    # Then The subject categories are loaded
    assert len(browse_page.subject_list) > 0
