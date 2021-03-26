import pytest
import json
import urllib
import urllib.error
import urllib.parse
import urllib.request


@pytest.fixture
def git_content_repos(headers_data):

    """Returns the list of all github content repos (starting with osbooks-)
    """

    repos_url = "https://api.github.com/orgs/openstax/repos?per_page=100&type=private"

    repos_req = urllib.request.Request(repos_url, headers=headers_data)
    repos_list = urllib.request.urlopen(repos_req).read()

    repo = []

    for item in json.loads(repos_list):
        for key, val in item.items():
            if str(val).startswith("osbooks-"):
                name_list = item["name"]
                repo.append(name_list)

    return repo
