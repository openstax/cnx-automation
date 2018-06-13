# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from os.path import join

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
    with Neb.get(help=True) as help:
        # THEN the usage message is displayed
        assert 'Usage: neb get ' in help
        assert 'Options:' in help
        assert '--help' in help


@markers.neb
@markers.nondestructive
@markers.parametrize("col_id,col_version", [('col11562', '1.19')])
def test_get_col(neb_env, col_id, col_version, snapshot):
    # GIVEN neb, an environment name, a collection id, a collection version, and the snapshot tool
    snapshot_name = join('neb', col_id, '{col_version}.tar.gz'.format(col_version=col_version))

    # WHEN we run `neb --verbose get env col_id col_version`
    with Neb.get(verbose=True, env=neb_env, col_id=col_id, col_version=col_version) as zip_dir:
        # THEN the complete zip is downloaded and matches the snapshot
        snapshot.assert_file_or_dir_match(zip_dir, snapshot_name)
