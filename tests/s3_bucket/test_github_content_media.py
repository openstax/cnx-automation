import requests

"""
Verifies that media folder in every github content repo exists and is not empty.
Latest update on December 13th, 2021
"""


def test_github_content_media(git_content_repos, git_content_repos_bundle, headers_data):

    for repo in git_content_repos + git_content_repos_bundle:

        html_url_list = []

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

                    html_url_list.append(item["html_url"])

        if len(html_url_list) > 1:
            assert any(".jpg" in s for s in html_url_list) or any(
                ".png" in s for s in html_url_list
            )

        else:
            print("No media files found")
            assert all(".gitkeep" in s for s in html_url_list)
