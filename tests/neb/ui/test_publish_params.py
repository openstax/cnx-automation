# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from os.path import join
import xml.etree.ElementTree as ET
from pkg_resources import parse_version

from tests import markers

from cli.neb import Neb


@markers.neb
@markers.nondestructive
def test_publish_help():
    # GIVEN neb

    # WHEN we run `neb publish --help`
    with Neb.publish(help=True) as help:
        # THEN the usage message is displayed
        assert "Usage: neb publish " in help
        assert "Options:" in help
        assert "--verbose" in help
        assert "--password" in help

@markers.neb
@markers.test_case("C195247")
@markers.nondestructive
def test_publish_no_env():
    # GIVEN neb

    # WHEN we run `neb publish`
    stdout, stderr, returncode = Neb.run("publish")

    # THEN neb exits with an error and the usage message is displayed
    assert returncode > 0
    assert "Usage: neb publish " in stderr
    assert 'Error: Missing argument "ENV"' in stderr


@markers.neb
@markers.test_case("C195247")
@markers.nondestructive
def test_publish_no_content_dir(neb_env):
    # GIVEN neb and an environment

    # WHEN we run `neb publish env`
    stdout, stderr, returncode = Neb.run("publish", neb_env)

    # THEN neb exits with an error and the usage message is displayed
    assert returncode > 0
    assert "Usage: neb publish " in stderr
    assert 'Error: Missing argument "CONTENT_DIR"' in stderr


