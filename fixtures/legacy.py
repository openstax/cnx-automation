# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pytest

LEGACY_DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data')

__all__ = ['legacy_base_url', 'legacy_username', 'legacy_password', 'blank_module_cnxml_filepath']


@pytest.fixture(scope='session')
def legacy_base_url(request):
    """Return a base URL for CNX legacy"""
    config = request.config
    base_url = (config.getoption('legacy_base_url') or
                config.getini('legacy_base_url'))
    if base_url is not None:
        return base_url


@pytest.fixture(scope='session')
def legacy_username(request):
    """Return a username for CNX legacy"""
    config = request.config
    username = config.getoption('legacy_username')
    if username is not None:
        return username


@pytest.fixture(scope='session')
def legacy_password(request):
    """Return a password for CNX legacy"""
    config = request.config
    password = config.getoption('legacy_password')
    if password is not None:
        return password


@pytest.fixture(scope='session')
def blank_module_cnxml_filepath(request):
    """Returns the path to the source CNXML file for a blank module (for upload)"""
    return os.path.join(LEGACY_DATA_DIR, 'blank_module.cnxml')
