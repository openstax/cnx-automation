import requests

"""
Verifies that media folder in every github content repo exists and is not empty.
Latest update on September 16th, 2021
"""


def test_github_content_media(git_content_repos, headers_data):

    html_url_count = []

    for repo in git_content_repos:

        print("\nNow verifying: ", repo)

        media_dir = f"https://api.github.com/repos/openstax/{repo}/contents/media/"

        media_list = requests.get(media_dir, headers=headers_data)

        if media_list.status_code != 200:

            # Return code 404, 501, ... for incorrect media url
            print(f">>>>> FAILED {media_list.status_code}: no media folder in {repo}")

        else:

            for item in media_list.json():

                if item["type"] != "file":

                    # Ignore anything that may not be a file
                    continue

                else:

                    html_url_count.append(item["html_url"])

        assert sum(".jpg" in s for s in html_url_count) > 0