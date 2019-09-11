# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from applitools.selenium import Eyes


@pytest.fixture
def applitools_api_key(request):
    config = request.config
    api_key = config.getoption("--applitools-key")

    if not api_key:

        pytest.warns("No Applitools API Key provided. Visual Tests will fail.")

    return api_key


@pytest.fixture
def applitools(request, applitools_api_key):
    """Returns a client that can interface with the applitools API"""

    eyes = Eyes()
    eyes.api_key = applitools_api_key

    yield eyes
