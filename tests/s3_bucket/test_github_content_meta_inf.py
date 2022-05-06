import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

from bs4 import BeautifulSoup

import re

"""
Verifies that META-INF folder in every github content repo exists and is not empty.
Latest update on May 5th, 2022
"""


def test_github_content_meta_inf(git_content_repos, headers_data):

    for repo in git_content_repos:

        print("\nNow verifying: ", repo)

        meta_inf_dir = f"https://api.github.com/repos/openstax/{repo}/contents/META-INF/"

        meta_inf_list = requests.get(meta_inf_dir, headers=headers_data)

        if meta_inf_list.status_code != 200:

            # Return code 404, 501, ... for incorrect meta-inf url
            print(f">>>>> FAILED {meta_inf_list.status_code}: no meta-inf folder in {repo}")

        else:

            for item in meta_inf_list.json():

                if item["type"] != "file":

                    # Ignore anything that may not be a file
                    continue

                else:

                    rel_path = urllib.parse.quote(item["path"])
                    meta_inf_url = (
                        f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}"
                    )

                    try:

                        meta_inf_resp = requests.get(meta_inf_url, headers=headers_data)

                    except HTTPError as h_e:
                        # Return code 404, 501, ... for incorrect/missing books.xml
                        pytest.fail(
                            f"HTTP Error {h_e.code}: incorrect/missing books.xml {meta_inf_url}"
                        )

                    else:

                        resp_content = meta_inf_resp.text

                        soup = BeautifulSoup(resp_content, "xml")
                        meta_inf = soup.find_all("book")

                        for cid in meta_inf:

                            try:
                                # Verifies that href= in META-INF/books.xml contains strings
                                href_result = re.search('href="(.*).xml', str(cid)).group(1)
                                assert href_result is not None

                            except AssertionError and AttributeError:
                                print(f"href missing in META-INF/books.xml: {repo}")

                            else:
                                pass

                            try:
                                # Verifies that slug= in META-INF/books.xml contains strings
                                slug_result = re.search('slug="(.*)" ', str(cid)).group(1)
                                assert slug_result is not None

                            except AssertionError and AttributeError:
                                print(f"slug missing in META-INF/books.xml: {repo}")

                            else:
                                pass

                            try:
                                # Verifies that style= in META-INF/books.xml contains strings
                                style_result = re.search('style="(.*)"', str(cid)).group(1)
                                assert style_result is not None

                            except AssertionError and AttributeError:
                                print(f"style missing in META-INF/books.xml: {repo}")

                            else:
                                continue
