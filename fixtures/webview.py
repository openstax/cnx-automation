import os

import pytest

from tests.utils import gen_from_file

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data')

__all__ = ['content_url', 'american_gov_url']


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
