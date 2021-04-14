import json
import urllib
import urllib.error
import urllib.parse
import urllib.request

from urllib.error import HTTPError

import pytest


"""
Verifies content of collection.xml of every collection in github content repo.
Latest update on April 14th, 2021
"""


def test_github_content_collections(git_content_repos, headers_data):

    license_list = [
        "http://creativecommons.org/licenses/by/4.0",
        "http://creativecommons.org/licenses/by-nc-sa/4.0",
        "http://creativecommons.org/licenses/by-sa/4.0",
    ]

    for repo in git_content_repos:

        print("\nNow verifying: ", repo)

        collections_dir = f"https://api.github.com/repos/openstax/{repo}/contents/collections/"

        try:

            collections_req = urllib.request.Request(collections_dir, headers=headers_data)
            collections_list = urllib.request.urlopen(collections_req).read()

        except HTTPError as h_e:
            # Return code 404, 501, ... for incorrect repo url
            pytest.fail(f"HTTP Error {h_e.code}: incorrect repo url {collections_dir}")

        else:

            for item in json.loads(collections_list):

                if item["type"] != "file":

                    # Ignore anything that may not be a file
                    continue

                rel_path = urllib.parse.quote(item["path"])
                collections_url = (
                    f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}"
                )

                try:

                    collections_req = urllib.request.Request(collections_url, headers=headers_data)
                    collections_resp = urllib.request.urlopen(collections_req)

                except HTTPError as h_e:
                    # Return code 404, 501, ... for incorrect/missing .collection.xml
                    pytest.fail(
                        f"HTTP Error {h_e.code}: incorrect/missing .collection.xml {collections_url}"
                    )

                else:

                    resp_content = str(collections_resp.read())

                    # Verifies collection.xml files for presence of content
                    assert (
                        resp_content.count("<md:") >= 1 and resp_content.count("<col:content") >= 1
                    )
                    # Verifies collection.xml files for presence of a license
                    # (from a list of 3 licenses used by openstax)
                    assert any(substring in resp_content for substring in license_list)
