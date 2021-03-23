import pytest


@pytest.fixture
def git_content_repos():
    """Returns the list of all github content repos
    """
    repo = ["osbooks-university-physics", "osbooks-college-algebra-bundle"]

    return repo
