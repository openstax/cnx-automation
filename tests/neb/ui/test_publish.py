# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

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
@markers.parametrize('content_dir', ['.'])
def test_publish_no_commit_message(neb_env, content_dir):
    # GIVEN neb, an environment, and a content dir

    # WHEN we run `neb publish env col_id`
    stdout, stderr, returncode = Neb.run('publish', neb_env, content_dir)

    # THEN neb exits with an error and the usage message is displayed
    assert returncode > 0
    assert 'Usage: neb publish ' in stderr
    assert 'Error: Missing argument "publication_message"' in stderr
