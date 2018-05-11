# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

nondestructive = pytest.mark.nondestructive
slow = pytest.mark.skipif(not pytest.config.getoption('runslow'),
                          reason='need --runslow option to run')
webview = pytest.mark.webview
legacy = pytest.mark.legacy
neb = pytest.mark.neb
