# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.content import Content


@pytest.mark.slow
@pytest.mark.nondestructive
def test_ncy_is_not_displayed(american_gov_url, selenium):
    # GIVEN An American Government URL and Selenium driver

    # WHEN The page is fully loaded using the URL
    page = Content(selenium, american_gov_url).open()

    # THEN :NOT_CONVERTED_YET is not displayed
    assert page.is_ncy_displayed is False
