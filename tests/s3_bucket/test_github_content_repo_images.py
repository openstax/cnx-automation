import requests

import urllib.parse

from bs4 import BeautifulSoup

import re


"""
Verifies whether images in the content of each index.cnxml file are present in the media folder
Latest update on January 29, 2023
"""


def test_github_content_repo_images(git_content_repos, headers_data):
    # checks all the github content repos within given index range
    sindex = int(input("Enter start index of a content repo: "))
    eindex = int(input("Enter end index a content repo: "))

    for repo in git_content_repos[sindex:eindex]:
        print("\nNow verifying: ", repo)

        contents_dir = f"https://api.github.com/repos/openstax/{repo}/contents"
        modules_dir = f"{contents_dir}/modules/"

        modules_list = requests.get(modules_dir, headers=headers_data)

        for item in modules_list.json():
            rel_path = urllib.parse.quote(item["path"])

            if item["type"] != "dir":
                print(f"Exclude file(s): {rel_path}")
                continue

            index_url = f"{contents_dir}/{rel_path}/index.cnxml"

            module_resp = requests.get(index_url, headers=headers_data)

            if module_resp.status_code in range(400, 501):
                print(
                    f"Error code {module_resp.status_code}: Incorrect/missing index file in {repo} / {rel_path}"
                )
                continue

            else:
                resp_content = module_resp.text

                soup = BeautifulSoup(resp_content, "xml")
                document = soup.find_all("document")
                content = soup.find_all("content")

                for doc in document:
                    md_title = doc.find_all("md:title")

                    try:
                        for img in content:
                            medias = img.find_all_next("image")

                            for image in medias:
                                try:
                                    src = re.findall(r'src="../../(.+?)"/>', str(image))[0]

                                except IndexError as ider:
                                    print(f"{ider}: {rel_path} -- {image}")
                                    continue

                                else:
                                    src_mod = re.sub(r"\".*", "", str(src))

                                    image_url = f"{contents_dir}/" + str(src_mod)

                                    module_resp = requests.get(image_url, headers=headers_data)

                                    if module_resp.status_code != 200:
                                        # Return code 404, 501, ... for incorrect image url
                                        print(
                                            f">>>>> FAILED {module_resp.status_code}: media/image issues in {image}"
                                        )

                                    else:
                                        continue

                    except (AssertionError, AttributeError):
                        print(f"---> media/image is missing in index.cnxml: {repo} / {md_title}")

                    else:
                        continue
