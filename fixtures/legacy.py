# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pytest

from tests.utils import skip_if_destructive_and_sensitive

LEGACY_DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data', 'legacy')

__all__ = ['legacy_base_url', 'legacy_username', 'legacy_password',
           'm46922_1_13_cnxml_filepath', 'sample_mathml3_cnxml_filepath']


@pytest.fixture
def legacy_base_url(request):
    """Return a base URL for CNX legacy"""
    config = request.config
    base_url = config.getoption('legacy_base_url') or config.getini('legacy_base_url')
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
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
def m46922_1_13_cnxml_filepath(request):
    """Returns the path to the source CNXML file for module m46922@1.13 (for upload)"""
    return os.path.join(LEGACY_DATA_DIR, 'm46922_1.13.cnxml')


@pytest.fixture(scope='session')
def sample_mathml3_cnxml_filepath(request):
    """Returns the path to the source CNXML file for sample mathml3 (for upload)"""
    return os.path.join(LEGACY_DATA_DIR, 'sample_mathml3.cnxml')
