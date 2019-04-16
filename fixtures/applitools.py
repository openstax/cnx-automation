# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from applitools.eyes import Eyes

@pytest.fixture(scope="session")
def applitools(request):
    """Returns a client that can interface with the applitools API"""

    eyes = Eyes()

    config = request.config
    eyes.api_key = config.getoption("--applitools-key")

    if not eyes.api_key:
        raise Exception("Applitools key is missing")
    else:
        yield eyes



