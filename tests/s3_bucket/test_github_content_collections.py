import requests

import urllib.parse
from urllib.error import HTTPError

import pytest


"""
Verifies content of collection.xml of every collection in github content repo.
Latest update on December 13th, 2021
"""


def test_github_content_collections(git_content_repos, git_content_repos_bundle, headers_data):

    license_list = [
        "http://creativecommons.org/licenses/by/4.0",
        "http://creativecommons.org/licenses/by-nc-sa/4.0",
        "http://creativecommons.org/licenses/by-sa/4.0",
    ]

    for repo in git_content_repos + git_content_repos_bundle:

        print("\nNow verifying: ", repo)

        collections_dir = f"https://api.github.com/repos/openstax/{repo}/contents/collections/"

        collections_list = requests.get(collections_dir, headers=headers_data)

        if collections_list.status_code != 200:

            # Return code 404, 501, ... for incorrect collections url
            print(f">>>>> FAILED {collections_list.status_code}: no collections folder in {repo}")

        else:

            for item in collections_list.json():

                if item["type"] != "file":

                    # Ignore anything that may not be a file
                    continue

                rel_path = urllib.parse.quote(item["path"])
                collections_url = (
                    f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}"
                )

                try:

                    collections_resp = requests.get(collections_url, headers=headers_data)

                except HTTPError as h_e:
                    # Return code 404, 501, ... for incorrect/missing collection.xml
                    pytest.fail(
                        f"HTTP Error {h_e.code}: incorrect/missing .collection.xml {collections_url}"
                    )

                else:

                    resp_content = collections_resp.text

                    # Verifies collection.xml files for presence of content
                    assert resp_content.count("<md:") >= 1
                    assert (
                        resp_content.count("<col:content") >= 1
                        or resp_content.count("<content") >= 1
                    )
                    assert resp_content.count("<col:collection") == 1
                    # Verifies collection.xml files for presence of a license
                    # (from a list of 3 licenses used by openstax)
                    assert any(substring in resp_content for substring in license_list)
