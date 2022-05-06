import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

from bs4 import BeautifulSoup


"""
Verifies content of collection.xml of every collection in github content repo.
Latest update on May 4th, 2022
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

                try:

                    collections_resp = requests.get(collections_url, headers=headers_data)

                except HTTPError as h_e:
                    # Return code 404, 501, ... for incorrect/missing collection.xml
                    pytest.fail(
                        f"HTTP Error {h_e.code}: incorrect/missing .collection.xml {collections_url}"
                    )

                else:

                    resp_content = collections_resp.text

                    soup = BeautifulSoup(resp_content, "xml")

                    md_title = soup.find_all("md:title")
                    md_license = soup.find_all("md:license")
                    content = soup.find_all("col:content")

                    try:

                        assert md_title is not None
                        assert md_license is not None
                        assert content is not None

                        assert any(substring in resp_content for substring in license_list)

                    except AssertionError:
                        print(
                            "---> Assertion error: content, md_title or md_license tags are MISSING CONTENT"
                        )

                    else:
                        pass

                    metadata = soup.find_all("metadata")
                    slug_text = metadata[0].find_next("slug").text

                    try:
                        # Verify slugs in collection.xml files (github repos) against slugs in ABL
                        assert slug_text in abl_books_uuids_slugs.values()

                    except AssertionError:
                        print(f"---> Assertion error (SLUG MISMATCH): {slug_text}")

                    else:
                        pass

                    uuid_text = metadata[0].find_next("uuid").text

                    try:
                        # Verify uuids in collection.xml files (github repos) against uuids in ABL
                        assert uuid_text in abl_books_uuids_slugs.keys()

                    except AssertionError:
                        print(f"---> Assertion error (UUID MISMATCH): {uuid_text}")

                    else:
                        continue
