import pytest
import requests


@pytest.fixture
def git_content_repos_1(headers_data):

    """Returns all the collection content repos names in github within given index range"""

    repos = []

    # list of excluded test git repos
    dels = [
        "osbooks-testing",
        "osbooks-otto-book",
        "osbooks-poet-documentation",
        "osbooks-ce-styles-test",
        "osbooks-playground",
    ]

    next_url = "https://api.github.com/orgs/openstax/repos?per_page=50"

    while next_url:

        resp = requests.get(next_url, headers=headers_data)

        for item in resp.json():
            for key, val in item.items():
                if str(val).startswith("osbooks-"):
                    name_list = item["name"]
                    repos.append(name_list)

        next_url = resp.links.get("next", {}).get("url")

    repos_dels = [ele for ele in repos if ele not in dels]

    return repos_dels[0:9]
