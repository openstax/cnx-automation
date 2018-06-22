# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from github3 import GitHub


@pytest.fixture(scope='session')
def github():
    """Returns a client that can interface with the GitHub API"""
    return GitHub()
