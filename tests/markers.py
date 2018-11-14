# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pytest import config, mark
from pytest_testrail.plugin import pytestrail

nondestructive = mark.nondestructive
parametrize = mark.parametrize
test_case = pytestrail.case
xfail = mark.xfail

slow = mark.skipif(not config.getoption('runslow'), reason='need --runslow option to run')

webview = mark.webview
legacy = mark.legacy
neb = mark.neb

requires_complete_dataset = mark.requires_complete_dataset
requires_deployment = mark.requires_deployment
requires_publishing = mark.requires_publishing
requires_varnish_routing = mark.requires_varnish_routing
