# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

import pytest

from pages.content import Content
from tests.utils import gen_from_file

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data')


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, 'american_gov_uuids.txt')))
def american_gov_url(content_url, request):
    """Creates an American Government URL based on the content_url fixture and a UUID

    Example: https://qa.cnx.org/contents/c6ee95dd-d10b-430c-8a83-20d5a28334a9
    """
    yield '{0}/{1}'.format(content_url, request.param)


@pytest.mark.slow
@pytest.mark.nondestructive
def test_ncy_is_not_displayed(american_gov_url, selenium):
    # GIVEN An American Government URL and Selenium driver

    # WHEN The page is fully loaded using the URL
    page = Content(selenium, american_gov_url).open()

    # THEN :NOT_CONVERTED_YET is not displayed
    assert page.is_ncy_displayed is False
