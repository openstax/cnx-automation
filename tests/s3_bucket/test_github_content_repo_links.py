import requests

import urllib.parse

from bs4 import BeautifulSoup


"""
Checks link tags for http urls in each index.cnxml file in a given range
Latest update on February 8th, 2023
"""


def test_github_content_repo_links(git_content_repos, headers_data):
    # checks all the github content repos within given index range
    sindex = int(input("Enter start index of a content repo: "))
    eindex = int(input("Enter end index a content repo: "))

    for repo in git_content_repos[sindex:eindex]:
        print("\nNow verifying: ", repo)

        contents_dir = f"https://api.github.com/repos/openstax/{repo}/contents"
        modules_dir = f"{contents_dir}/modules/"

        user_agent_list = "Mozilla/5.0 (X11; Ubuntu; Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

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
                links = soup.find_all("link")

                for link in links:
                    try:
                        urls = link["url"]

                    except KeyError:
                        continue

                    else:
                        if "http" in urls:
                            try:
                                session = requests.Session()
                                session.max_redirects = 60
                                session.headers["User-Agent"] = user_agent_list

                                assert session.get(urls, timeout=30).status_code in [
                                    200,
                                    301,
                                    302,
                                    400,
                                    403,
                                    406,
                                ]

                            except (
                                AssertionError,
                                requests.exceptions.ConnectionError,
                                requests.exceptions.ReadTimeout,
                            ) as err:
                                print(f"{rel_path} - {urls} - {err}")
                                continue
