# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from cli.neb import Neb


@markers.neb
@markers.nondestructive
def test_help():
    # GIVEN neb

    # WHEN we run `neb --help`
    help = Neb.help

    # THEN the usage message is displayed
    assert 'Usage: neb ' in help
    assert 'Options:' in help
    assert '--help' in help
    assert '--version' in help
    assert 'Commands:' in help
    assert 'get' in help
    assert 'publish' in help


@markers.neb
@markers.nondestructive
def test_version():
    # GIVEN neb and a minimum version
    minimum_version = '3.1.0'

    # WHEN we run `neb --version`
    version = Neb.version

    # THEN neb lists a version that is greater than or equal to the minimum version
    assert version >= minimum_version
