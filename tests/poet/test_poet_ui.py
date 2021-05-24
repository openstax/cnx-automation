import requests

from urllib.error import HTTPError
from selenium.common.exceptions import NoSuchElementException

import pytest

from pages.poet.home import Home

import os

"""
Verifies POET ui
Latest update on May 21st, 2021
"""


def test_poet_ui(selenium, headers_data):
    github_user = os.environ.get("GITHUB_USER")
    github_password = os.environ.get("GITHUB_PASSWORD")

    git_repo_url = os.environ.get("GIT_REPO_URL")

    try:
        requests.get(git_repo_url, headers=headers_data)

    except HTTPError as h_e:
        # Return code 404, 501, ... for incorrect repo url
        pytest.fail(f"HTTP Error {h_e.code}: incorrect repo url {git_repo_url}")

    else:
        # launches gitpod for openstax/poet test repo and logs in
        home = Home(selenium, git_repo_url).open()

        home.click_github_login_button()

        selenium.switch_to.window(selenium.window_handles[1])

        home.fill_user_field(github_user)
        home.fill_passwd_field(github_password)

        home.click_login_button()

        selenium.switch_to.window(selenium.window_handles[0])

        try:
            # tries for the presence of existing workspace dialog
            # and clicks on it to launch the workspace
            home.is_existing_workspace_present()

            home.click_existing_workspace_selector()
            home.click_openstax_icon()
            home.click_toc_editor_button()
            home.click_add_subcollection_button()

            assert home.new_subcollection_box
            assert home.toc_trees_dropdown

        except AssertionError as aerr:
            pytest.fail(f"ASSERTION ERROR {aerr}")

        except NoSuchElementException:
            # creates and launches a new workspace
            home.click_openstax_icon()
            home.click_toc_editor_button()
            home.click_add_subcollection_button()

            assert home.new_subcollection_box
            assert home.toc_trees_dropdown
