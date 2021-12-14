import pytest
import requests


@pytest.fixture
def git_content_repos_bundle(headers_data):

    """Returns all the collection content repos names in github (ending with bundle)"""

    repos = []

    next_url = "https://api.github.com/orgs/openstax/repos?per_page=50&type=private"

    while next_url:

        resp = requests.get(next_url, headers=headers_data)

        for item in resp.json():
            for key, val in item.items():
                if str(val).startswith("osbooks-") and str(val).endswith("bundle"):
                    name_list = item["name"]
                    repos.append(name_list)

        next_url = resp.links.get("next", {}).get("url")

    return repos
