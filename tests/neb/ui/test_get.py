# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from cli.neb import Neb


@markers.neb
@markers.nondestructive
def test_get_incomplete_arguments():
    # GIVEN neb

    # WHEN we run `neb get`
    error = Neb.invoke('get', check=False)

    # THEN the usage message is displayed
    assert 'Usage: neb get ' in error
    assert 'Error: Missing argument ' in error


@markers.neb
@markers.nondestructive
def test_get_help():
    # GIVEN neb

    # WHEN we run `neb get --help`
    help = Neb.get(help=True)

    # THEN the usage message is displayed
    assert 'Usage: neb get ' in help
    assert 'Options:' in help
    assert '--help' in help
