import pytest


@pytest.fixture
def github_authorization(github_tok):
    """Returns the authorization token for github
    """
    headers = {"Authorization": "token " + github_tok, "Accept": "application/vnd.github.v3.raw"}

    return headers
