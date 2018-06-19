# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pytest

from tests.utils import gen_from_file, skip_if_destructive_and_sensitive

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data', 'webview')

__all__ = ['content_url', 'american_gov_url', 'webview_base_url']


@pytest.fixture
def content_url(base_url):
    """Creates contents URL based on the base_url

    Example: https://qa.cnx.org/contents
    """
    return '{0}/{1}'.format(base_url, 'contents')


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, 'american_gov_uuids.txt')))
def american_gov_url(content_url, request):
    """Creates an American Government URL based on the content_url fixture and a UUID

    Example: https://qa.cnx.org/contents/c6ee95dd-d10b-430c-8a83-20d5a28334a9
    """
    yield '{0}/{1}'.format(content_url, request.param)


@pytest.fixture
def webview_base_url(request):
    """Return a base URL for CNX webview"""
    config = request.config
    base_url = config.getoption('webview_base_url') or config.getini('webview_base_url')
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url
