import pytest


@pytest.fixture
def headers_data(github_tok):
    """Returns the headers with token
    """
    headers = {"Authorization": "token " + github_tok, "Accept": "application/vnd.github.v3.raw"}

    return headers
