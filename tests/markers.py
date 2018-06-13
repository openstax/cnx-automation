# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pytest import config, mark

nondestructive = mark.nondestructive
parametrize = mark.parametrize
slow = mark.skipif(not config.getoption('runslow'), reason='need --runslow option to run')
webview = mark.webview
legacy = mark.legacy
neb = mark.neb
