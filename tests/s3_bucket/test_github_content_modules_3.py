import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

"""
Verifies content of index.cnxml of every collection module of every github content repo.
Latest update on April 4th, 2022
"""


def test_github_content_modules_3(git_content_repos_3, headers_data):

    # checks all the github content repos within given index range
    for repo in git_content_repos_3:

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

                    # Verifies index.cnxml files for presence of content
                    assert (
                        resp_content.count("<md:") > 1
                        and resp_content.count("<content") >= 1
                        and resp_content.count("<title") >= 1
                    )
