# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pkg_resources import parse_version
import requests
from warnings import warn

import nebu

from tests import markers
from cli.neb import Neb


@markers.neb
@markers.nondestructive
def test_no_command():
    # GIVEN neb

    # WHEN we run `neb`
    usage = Neb.no_command

    # THEN the usage/help message is displayed
    assert "Usage: neb " in usage
    assert "Options:" in usage
    assert "--help" in usage
    assert "--version" in usage
    assert "Commands:" in usage
    assert "get" in usage
    assert "publish" in usage


@markers.neb
@markers.nondestructive
def test_help():
    # GIVEN neb

    # WHEN we run `neb --help`
    usage = Neb.help

    # THEN the usage/help message is displayed
    assert "Usage: neb " in usage
    assert "Options:" in usage
    assert "--help" in usage
    assert "--version" in usage
    assert "Commands:" in usage
    assert "get" in usage
    assert "publish" in usage


@markers.neb
@markers.test_case("C195248")
@markers.nondestructive
def test_version():
    # GIVEN neb and its __version__
    nebu_version = nebu.__version__

    # WHEN we run `neb --version`
    version_string = Neb.version

    # THEN neb lists the same version as the nebu module
    assert version_string == nebu_version

    # Warn if the version of neb is outdated
    version = parse_version(version_string)

    # Based on https://github.com/alexmojaki/outdated/blob/master/outdated/__init__.py
    package_dict = requests.get("https://pypi.python.org/pypi/nebuchadnezzar/json").json()
    latest_version_string = package_dict["info"]["version"]
    latest_version = parse_version(latest_version_string)

    if version < latest_version:
        message = (
            "Tests were run against an outdated version of nebuchadnezzar\n"
            " Loaded version: {loaded_version}\n Latest Version: {latest_version}\n"
            " Consider updating the package version in requirements.txt".format(
                loaded_version=version_string, latest_version=latest_version_string
            )
        )
        warn(message)
