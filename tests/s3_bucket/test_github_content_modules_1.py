import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

from bs4 import BeautifulSoup


"""
Verifies content of index.cnxml of every collection module of every github content repo.
Latest update on May 9th, 2022
"""


def test_github_content_modules_1(git_content_repos_1, headers_data):

    # checks all the github content repos within given index range
    for repo in git_content_repos_1:

        print("\nNow verifying: ", repo)

        modules_dir = f"https://api.github.com/repos/openstax/{repo}/contents/modules/"

        modules_list = requests.get(modules_dir, headers=headers_data)

        if modules_list.status_code != 200:

            # Return code 404, 501, ... for incorrect modules url
            print(f">>>>> FAILED {modules_list.status_code}: no modules folder in {repo}")

        else:

            for item in modules_list.json():

                if item["type"] != "dir":

                    # Ignore anything that may not be a directory
                    continue

                rel_path = urllib.parse.quote(item["path"])
                modules_url = (
                    f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}/index.cnxml"
                )

                try:

                    module_resp = requests.get(modules_url, headers=headers_data)

                except HTTPError as h_e:
                    # Return code 404, 501, ... for incorrect/missing index.cnxml
                    pytest.fail(
                        f"HTTP Error {h_e.code}: incorrect/missing index.cnxml {modules_url}"
                    )

                else:

                    resp_content = module_resp.text

                    soup = BeautifulSoup(resp_content, "xml")
                    document = soup.find_all("document")
                    content = soup.find_all("content")

                    for doc in document:

                        md_title = doc.find_all("md:title")
                        md_content_id = doc.find_all("md:content-id")

                        # Verifies index.cnxml for presence of md:title and md:uuid metadata
                        try:
                            assert md_title is not None

                        except (AssertionError, AttributeError):
                            print(
                                f"---> <md_title> tag is missing in index.cnxml: {repo}/{md_title}/{md_content_id}"
                            )

                        else:
                            pass

                        try:
                            assert doc.find_all("md:uuid") is not None

                        except (AssertionError, AttributeError):
                            print(
                                f"---> <md_uuid> tag is missing in index.cnxml: {repo}/{md_title}/{md_content_id}"
                            )

                        else:
                            pass

                        try:
                            # Verifies that <content> tag in index.cnxml is not empty
                            for abc in content:
                                assert len(abc.get_text()) > 1

                        except (AssertionError, AttributeError):
                            print(
                                f"---> <content> is empty in index.cnxml: {repo}/{md_title}/{md_content_id}"
                            )

                        else:
                            continue
