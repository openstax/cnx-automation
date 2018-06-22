# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

__all__ = ['neb_env']


@pytest.fixture(scope='session')
def neb_env(request):
    """Returns the Neb environment name"""
    config = request.config
    neb_env = config.getoption('neb_env') or config.getini('neb_env')
    if neb_env is not None:
        return neb_env
