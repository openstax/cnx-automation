import json
import urllib
import urllib.error
import urllib.parse
import urllib.request

from urllib.error import HTTPError

import pytest

"""
Verifies content of index.cnxml of every collection module of every github content repo.
Latest update on April 14th, 2021
"""


def test_github_content_repos(git_content_repos, headers_data):

    for repo in git_content_repos:

        print("\nNow verifying modules of: ", repo)

        modules_dir = f"https://api.github.com/repos/openstax/{repo}/contents/modules/"

        try:

            modules_req = urllib.request.Request(modules_dir, headers=headers_data)
            modules_list = urllib.request.urlopen(modules_req).read()

        except HTTPError as h_e:
            # Return code 404, 501, ... for incorrect modules url
            pytest.fail(f"HTTP Error {h_e.code}: incorrect modules url {modules_dir}")

        else:

            for item in json.loads(modules_list):

                if item["type"] != "dir":

                    # Ignore anything that may not be a directory
                    continue

                rel_path = urllib.parse.quote(item["path"])
                modules_url = (
                    f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}/index.cnxml"
                )

                try:

                    modules_req = urllib.request.Request(modules_url, headers=headers_data)
                    module_resp = urllib.request.urlopen(modules_req)

                except HTTPError as h_e:
                    # Return code 404, 501, ... for incorrect/missing index.cnxml
                    pytest.fail(
                        f"HTTP Error {h_e.code}: incorrect/missing index.cnxml {modules_url}"
                    )

                else:

                    resp_content = module_resp.read()

                    # Verifies index.cnxml files for presence of content
                    assert (
                        resp_content.count(b"<md:") > 1
                        and resp_content.count(b"<content") >= 1
                        and resp_content.count(b"<title") >= 1
                    )
