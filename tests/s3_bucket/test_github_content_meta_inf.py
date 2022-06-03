import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

from bs4 import BeautifulSoup

"""
Verifies that META-INF folder in every github content repo exists and is not empty.
Latest update on June 3rd, 2022
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
                        book_tags = soup.find_all("book")

                        for btag in book_tags:

                            try:
                                btag["slug"]

                            except (KeyError, AttributeError):
                                print(f"\n--- slug tag is MISSING in META-INF/books.xml: {repo}")

                            else:

                                if len(btag["slug"]) > 0:
                                    pass
                                else:
                                    print(f"\n--- slug tag is EMPTY in META-INF/books.xml: {repo}")

                            try:
                                btag["style"]

                            except (KeyError, AttributeError):
                                print(f"\n--- style tag is MISSING in META-INF/books.xml: {repo}")

                            else:

                                if len(btag["style"]) > 0:
                                    pass
                                else:
                                    print(f"\n--- style tag is EMPTY in META-INF/books.xml: {repo}")

                            try:
                                btag["href"]

                            except (KeyError, AttributeError):
                                print(f"\n--- href tag is MISSING in META-INF/books.xml: {repo}")

                            else:

                                if len(btag["href"]) > 0:
                                    pass
                                else:
                                    print(f"\n--- href tag is EMPTY in META-INF/books.xml: {repo}")
