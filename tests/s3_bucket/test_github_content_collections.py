import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

from bs4 import BeautifulSoup


"""
Verifies content of collection.xml of every collection in github content repo.
Latest update on June 7th, 2022
"""


def test_github_content_collections(git_content_repos, headers_data, abl_books_uuids_slugs):

    license_list = [
        "http://creativecommons.org/licenses/by/4.0",
        "http://creativecommons.org/licenses/by-nc-sa/4.0",
        "http://creativecommons.org/licenses/by-sa/4.0",
        "https://creativecommons.org/licenses/by/4.0/deed.pl",
    ]

    for repo in git_content_repos:

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

                if "collection.xml" not in collections_url:
                    print(f"!!! .collection.xml is missing in {repo}")

                else:

                    try:
                        collections_resp = requests.get(collections_url, headers=headers_data)
                        collections_resp.raise_for_status()

                    except HTTPError as h_e:
                        # Return code 404, 501, ... for incorrect/missing collection.xml
                        pytest.fail(
                            f"HTTP Error {h_e.code}: incorrect/missing .collection.xml {collections_url}"
                        )

                    else:

                        resp_content = collections_resp.text

                        soup = BeautifulSoup(resp_content, "xml")
                        col_collection = soup.find_all("collection")

                        for col in col_collection:

                            try:
                                assert len(col.find("md:title").text.strip()) > 0

                                assert any(substring in resp_content for substring in license_list)

                            except (AssertionError, AttributeError):
                                print(
                                    "---> Assertion error: md:title or md:license tags are MISSING CONTENT"
                                )

                            else:
                                pass

                            try:
                                assert len(col.find("content").text.strip()) > 0

                            except (AssertionError, AttributeError):
                                print("---> Assertion error: col:content tag is MISSING CONTENT")

                            else:
                                pass

                            slug_text = col.find("slug").text

                            try:
                                # Verify slugs in collection.xml files (github repos) against slugs in ABL
                                assert slug_text in abl_books_uuids_slugs.values()

                            except (AssertionError, AttributeError):
                                print(f"---> Assertion error (SLUG MISMATCH): {slug_text}")

                            else:
                                pass

                            uuid_text = col.find("uuid").text

                            try:
                                # Verify uuids in collection.xml files (github repos) against uuids in ABL
                                assert uuid_text in abl_books_uuids_slugs.keys()

                            except (AssertionError, AttributeError):
                                print(f"---> Assertion error (UUID MISMATCH): {uuid_text}")

                            else:
                                continue
