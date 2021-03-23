import json
import urllib
import urllib.error
import urllib.parse
import urllib.request

"""
Verifies content of collection.xml of every collection in github content repo.
Latest update on March. 23nd, 2021
"""


def test_github_content_collections(git_content_repos, headers_data):

    for repo in git_content_repos:

        collections_dir = f"https://api.github.com/repos/openstax/{repo}/contents/collections/"

        collections_req = urllib.request.Request(collections_dir, headers=headers_data)
        collections_list = urllib.request.urlopen(collections_req).read()

        for item in json.loads(collections_list):

            if item["type"] != "file":

                # Ignore anything that may not be a file
                continue

            rel_path = item["path"]
            collections_url = f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}"

            collections_req = urllib.request.Request(collections_url, headers=headers_data)
            collections_resp = urllib.request.urlopen(collections_req)

            if collections_resp.status != 200:
                assert (
                    collections_resp.status != 200
                ), f"FAILED to find collection.xml in {rel_path}"

            else:
                resp_content = collections_resp.read()

                # Verifies collection.xml files for presence of content
                assert resp_content.count(b"<md:") >= 1 and resp_content.count(b"<col:content") >= 1
