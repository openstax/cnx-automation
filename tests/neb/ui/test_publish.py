# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tempfile import TemporaryDirectory

from tests import markers
from tests.utils import get_neb_snapshot_name

from cli.neb import Neb


@markers.neb
@markers.nondestructive
def test_publish_help():
    # GIVEN neb

    # WHEN we run `neb publish --help`
    with Neb.publish(help=True) as help:
        # THEN the usage message is displayed
        assert 'Usage: neb publish ' in help
        assert 'Options:' in help
        assert '--help' in help


@markers.neb
@markers.nondestructive
def test_publish_no_env():
    # GIVEN neb

    # WHEN we run `neb publish`
    stdout, stderr, returncode = Neb.run('publish')

    # THEN neb exits with an error and the usage message is displayed
    assert returncode > 0
    assert 'Usage: neb publish ' in stderr
    assert 'Error: Missing argument "env"' in stderr


@markers.neb
@markers.nondestructive
def test_publish_no_col_id(neb_env):
    # GIVEN neb and an environment

    # WHEN we run `neb publish env`
    stdout, stderr, returncode = Neb.run('publish', neb_env)

    # THEN neb exits with an error and the usage message is displayed
    assert returncode > 0
    assert 'Usage: neb publish ' in stderr
    assert 'Error: Missing argument "content_dir"' in stderr


@markers.neb
@markers.nondestructive
def test_publish_no_commit_message(neb_env):
    # GIVEN neb, an environment, and a content dir
    with TemporaryDirectory() as content_dir:

        # WHEN we run `neb publish env content_dir`
        stdout, stderr, returncode = Neb.run('publish', neb_env, content_dir)

    # THEN neb exits with an error and the usage message is displayed
    assert returncode > 0
    assert 'Usage: neb publish ' in stderr
    assert 'Error: Missing argument "publication_message"' in stderr


@markers.neb
@markers.nondestructive
@markers.slow
@markers.parametrize(
    'col_id,col_version,publication_message,expected_validation_errors',
    [('col11562', '1.19-invalid', 'Made the CNXML invalid',
      ('/m46885/index.cnxml:102:22 -- error: ID "id9602938" has already been defined',
       '/m46885/index.cnxml:101:22 -- error: first occurrence of ID "id9602938"'))])
def test_publish_invalid_cnxml(neb_env, col_id, col_version, publication_message,
                               expected_validation_errors, snapshot):
    # GIVEN neb, an environment, a content dir, a publication message,
    # the expected errors, and the snapshot tool
    snapshot_name = get_neb_snapshot_name(col_id, col_version)

    with TemporaryDirectory() as content_dir:
        snapshot.extract(snapshot_name, content_dir)

        # WHEN we run `neb publish env content_dir publication_message`
        # Neb currently fails with a cryptic error if content_dir is not inside the CWD
        # Remove the following 2 lines once https://trello.com/c/jVkv4hQd is fixed
        import os
        os.chdir(os.path.join(content_dir, '..'))
        stdout, stderr, returncode = Neb.run('publish', neb_env, content_dir, publication_message)

    # THEN neb exits with an error and the CNXML validation failure message is displayed
    assert returncode > 0
    assert "We've got problems... :(" in stderr

    for validation_error in expected_validation_errors:
        assert validation_error in stderr
