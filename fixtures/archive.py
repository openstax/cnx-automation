# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from tests.utils import skip_if_destructive_and_sensitive

__all__ = ["archive_base_url"]


@pytest.fixture
def archive_base_url(request):
    """Return a base URL for CNX archive"""
    config = request.config
    base_url = config.getoption("archive_base_url") or config.getini("archive_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url
