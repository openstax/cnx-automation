# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.content import Content


@pytest.mark.nondestructive
def test_ncy_not_displayed(base_url, selenium):
    page = Content(selenium, 'https://qa.cnx.org/contents/26b372ce-28e5-4338-95e6-49639cd2a88d').open()
    assert not page.is_ncy_displayed
