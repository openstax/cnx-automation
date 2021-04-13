import pytest
import json
import urllib
import urllib.error
import urllib.parse
import urllib.request

import requests


@pytest.fixture
def git_content_repos(headers_data):

    """Returns the list of all github content repos (starting with osbooks-)
    """

    url = "https://api.github.com/orgs/openstax/repos?per_page=50&type=private"

    resp = requests.get(url, headers=headers_data)

    repos = []

    while resp.links.get("next"):
        next_url = resp.links["next"]["url"]
        resp = requests.get(next_url, headers=headers_data)

        repos_req = urllib.request.Request(resp.url, headers=headers_data)
        repos_list = urllib.request.urlopen(repos_req).read()

        for item in json.loads(repos_list):
            for key, val in item.items():
                if str(val).startswith("osbooks-"):
                    name_list = item["name"]
                    repos.append(name_list)

    return repos
