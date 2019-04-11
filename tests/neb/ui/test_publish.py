# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import random
from tempfile import TemporaryDirectory
from litezip.main import COLLECTION_NSMAP

from tests import markers
from tests.utils import get_neb_snapshot_name, edit_collXML

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
        assert "--help" in help


@markers.neb
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
@markers.nondestructive
def test_publish_no_col_id(neb_env):
    # GIVEN neb and an environment

    # WHEN we run `neb publish env`
    stdout, stderr, returncode = Neb.run("publish", neb_env)

    # THEN neb exits with an error and the usage message is displayed
    assert returncode > 0
    assert "Usage: neb publish " in stderr
    assert 'Error: Missing argument "CONTENT_DIR"' in stderr


@markers.neb
@markers.nondestructive
def test_publish_no_commit_message(neb_env):
    # GIVEN neb, an environment, and a content dir
    try:
        with TemporaryDirectory() as content_dir:

            # WHEN we run `neb publish env content_dir`
            stdout, stderr, returncode = Neb.run("publish", neb_env, content_dir, timeout=1)
    except subprocess.TimeoutExpired as e:
        # THEN neb prompts for a publication message and waits for user to enter it until it times out
        assert "Publication message:" in e.stdout


@markers.neb
@markers.nondestructive
@markers.slow
@markers.parametrize(
    "col_id,col_version,publication_message,expected_validation_errors",
    [
        (
            "col11562",
            "1.19-invalid",
            "Made the CNXML invalid",
            (
                '/m46885/index.cnxml:102:22 -- error: ID "id9602938" has already been defined',
                '/m46885/index.cnxml:101:22 -- error: first occurrence of ID "id9602938"',
            ),
        )
    ],
)
def test_publish_invalid_cnxml(
    neb_env, col_id, col_version, publication_message, expected_validation_errors, snapshot
):
    # GIVEN neb, an environment, a content dir, a publication message,
    # the expected errors, and the snapshot tool
    snapshot_name = get_neb_snapshot_name(col_id, col_version)

    with TemporaryDirectory() as content_dir:
        snapshot.extract(snapshot_name, content_dir)

        # WHEN we run `neb publish env content_dir publication_message`
        # Neb currently fails with a cryptic error if content_dir is not inside the CWD
        # Remove the following 2 lines once https://trello.com/c/jVkv4hQd is fixed
        import os

        os.chdir(os.path.join(content_dir, ".."))
        stdout, stderr, returncode = Neb.run("publish", neb_env, content_dir, publication_message)

    # THEN neb exits with an error and the CNXML validation failure message is displayed
    assert returncode > 0
    assert "We've got problems... :(" in stderr

    for validation_error in expected_validation_errors:
        assert validation_error in stderr


@markers.neb
@markers.nondestructive
@markers.slow
@markers.parametrize(
    "col_id, col_version, publication_message",
    [("col11562", "latest", "Publication message from cnx-automation")],
)
def test_successful_publish(
    col_id, col_version, publication_message, legacy_username, legacy_password
):
    # GIVEN the latest version of a collection available
    with Neb.get(verbose=True, env="staging", col_id=col_id, col_version="latest") as coll_dir:
        # WHEN we make an edit
        with edit_collXML(coll_dir) as collection:
            elem = collection.xpath("//md:title", namespaces=COLLECTION_NSMAP)[0]
            elem.text = "a different collection title {}".format(random.randint(0, 99999))

        # THEN we are able to successfully publish it
        stdout, stderr, returncode = Neb.run(
            "publish",
            "staging",
            coll_dir,
            "--message",
            publication_message,
            "--username",
            legacy_username,
            "--password",
            legacy_password,
        )
        assert "Great work!!! =D" in stderr
