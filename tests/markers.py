# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pytest import mark
from pytest_testrail.plugin import pytestrail

# Markers need to be registered in conftest.py and added as a return value
# in the get_custom_markers() function.
# FIXME: Replace all instances of @markers.{custom_marker} with @pytest.mark.{custom_marker}

nondestructive = mark.nondestructive
parametrize = mark.parametrize
test_case = pytestrail.case
xfail = mark.xfail

slow = mark.slow
smoke = mark.smoke

webview = mark.webview
legacy = mark.legacy
neb = mark.neb
rex = mark.rex

requires_complete_dataset = mark.requires_complete_dataset
requires_deployment = mark.requires_deployment
requires_publishing = mark.requires_publishing
requires_varnish_routing = mark.requires_varnish_routing
