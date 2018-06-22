# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from github3 import login, GitHub


@pytest.fixture(scope='session')
def github(pytestconfig):
    """Returns a client that can interface with the GitHub API"""
    token = pytestconfig.getoption('--github-token')
    if token:
        return login(token=token)
    else:
        return GitHub()
