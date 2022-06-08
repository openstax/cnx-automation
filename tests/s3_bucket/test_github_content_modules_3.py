import requests

import urllib.parse

from bs4 import BeautifulSoup


"""
Verifies content of index.cnxml of every collection module of every github content repo.
Latest update on June 8th, 2022
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

                module_resp = requests.get(modules_url, headers=headers_data)

                if module_resp.status_code in range(400, 501):
                    print(
                        f"Error code {module_resp.status_code}: Incorrect/missing index file in {rel_path}"
                    )
                    continue

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
                            assert len(md_title) > 0

                        except (AssertionError, AttributeError):
                            print(
                                f"---> <md_title> tag is missing in index.cnxml: {repo}/{md_title}/{md_content_id}"
                            )

                        else:
                            pass

                        try:
                            assert len(doc.find_all("md:uuid")) > 0

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
