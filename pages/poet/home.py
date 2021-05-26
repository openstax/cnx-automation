# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page

from time import sleep


class Home(Page):

    _github_login_locator = (By.CSS_SELECTOR, "button:nth-child(1)")

    _user_field_locator = (By.CSS_SELECTOR, "#login_field")
    _passwd_field_locator = (By.CSS_SELECTOR, "#password")

    _login_locator = (By.CSS_SELECTOR, "input.btn.btn-primary.btn-block")

    _openstax_icon_locator = (By.CSS_SELECTOR, "li:nth-child(8)")
    _toc_editor_button_locator = (By.CSS_SELECTOR, "div.welcome-view-content > div:nth-child(1)")

    _add_subcollection_button_locator = (By.CSS_SELECTOR, "div:nth-child(2) button")
    _toc_trees_dropdown_locator = (
        By.CSS_SELECTOR,
        "div.pane-body > div.tree-explorer-viewlet-tree-view",
    )

    _new_subcollection_box_locator = (By.CSS_SELECTOR, "div.rst__rowContents > div.rst__rowLabel")

    _existing_workspace_selector_locator = (By.CSS_SELECTOR, "p:nth-child(2)")

    @property
    def is_github_login_displayed(self):
        return self.is_element_displayed(*self._github_login_locator)

    def click_github_login_button(self):
        self.wait.until(lambda _: self.is_github_login_displayed)
        self.find_element(*self._github_login_locator).click()

    @property
    def is_passwd_field_displayed(self):
        return self.find_element(*self._passwd_field_locator)

    def fill_passwd_field(self, value):
        self.wait.until(lambda _: self.is_passwd_field_displayed)
        self.is_passwd_field_displayed.send_keys(value)

    @property
    def is_user_field_displayed(self):
        return self.find_element(*self._user_field_locator)

    def fill_user_field(self, value):
        self.wait.until(lambda _: self.is_user_field_displayed)
        self.is_user_field_displayed.send_keys(value)

    @property
    def is_login_button_displayed(self):
        return self.is_element_displayed(*self._login_locator)

    def click_login_button(self):
        self.wait.until(lambda _: self.is_login_button_displayed)
        self.find_element(*self._login_locator).click()

    @property
    def is_openstax_icon_displayed(self):
        return self.is_element_displayed(*self._openstax_icon_locator)

    def click_openstax_icon(self):
        self.wait.until(lambda _: self.is_openstax_icon_displayed)
        self.find_element(*self._openstax_icon_locator).click()

    @property
    def is_toc_editor_button_displayed(self):
        return self.is_element_displayed(*self._toc_editor_button_locator)

    def click_toc_editor_button(self):
        self.wait.until(lambda _: self.is_toc_editor_button_displayed)
        self.find_element(*self._toc_editor_button_locator).click()

    @property
    def is_add_subcollection_button_displayed(self):
        return self.is_element_displayed(*self._add_subcollection_button_locator)

    def click_add_subcollection_button(self):
        self.wait.until(lambda _: self.is_add_subcollection_button_displayed)
        self.find_element(*self._add_subcollection_button_locator).click()

    @property
    def is_toc_trees_dropdown_displayed(self):
        return self.is_element_displayed(*self._toc_trees_dropdown_locator)

    def toc_trees_dropdown(self):
        self.wait.until(lambda _: self.is_toc_trees_dropdown_displayed)
        return self.is_element_displayed(*self._toc_trees_dropdown_locator)

    @property
    def is_new_subcollection_box_displayed(self):
        return self.is_element_displayed(*self._new_subcollection_box_locator)

    def new_subcollection_box(self):
        self.wait.until(lambda _: self.is_new_subcollection_box_displayed)
        return self.is_element_displayed(*self._new_subcollection_box_locator)

    @property
    def existing_workspace_selector(self):
        return self.find_element(*self._existing_workspace_selector_locator)

    def is_existing_workspace_present(self):
        return self.is_element_displayed(*self._existing_workspace_selector_locator)

    def click_existing_workspace_selector(self):
        sleep(3)
        self.find_element(*self._existing_workspace_selector_locator).click()
