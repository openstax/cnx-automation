# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re
from functools import lru_cache

from pages.archive.base import Page

from selenium.webdriver.common.by import By


class Content(Page):
    """Interfaces with a content page from CNX Archive.

    Archive JSON Examples:

    Collection: https://archive.cnx.org/contents/30189442-6998-4686-ac05-ed152b91b9de@19.2.json
    Module: https://archive.cnx.org/contents/829e47cf-dbf7-4dfb-b3da-a3beb62f99ab@13.json
    """

    URL_TEMPLATE = "/contents/{uuid_and_version}.json"
    # The browser automatically wraps the JSON response in some HTML
    _json_locator = (By.TAG_NAME, "pre")
    # Whitelisted fields in the main archive json
    _stable_fields = [
        "googleAnalytics",
        "version",
        "submitlog",
        "abstract",
        "printStyle",
        "roles",
        "keywords",
        "title",
        "mediaType",
        "subjects",
        "publishers",
        "parentTitle",
        "authors",
        "parentVersion",
        "legacy_version",
        "licensors",
        "language",
        "license",
        "doctype",
        "buyLink",
        "submitter",
        "collated",
        "parentAuthors",
    ]
    # Whitelisted fields inside the "tree" field
    _stable_tree_fields = ["contents", "title"]
    _created_date_regex = re.compile(r'<meta name="created-time".*?\/>')
    _revised_date_regex = re.compile(r'<meta name="revised-time".*?\/>')
    _cnxml_html_version_regex = re.compile('data-cnxml-to-html-ver=".+?"')

    @property
    def json_pre(self):
        """Returns the element that wraps the full archive json."""
        return self.find_element(*self._json_locator)

    @property
    def json_text(self):
        """Returns the full archive json as a string."""
        return self.json_pre.text

    @property
    @lru_cache(maxsize=None)
    def dict(self):
        """Returns the archive json as a dict."""
        import json

        return json.loads(self.json_text)

    @property
    def id(self):
        """Returns the value of the "id" field."""
        return self.dict["id"]

    @property
    def title(self):
        """Returns the value of the "title" field."""
        return self.dict["title"]

    @property
    def has_tree(self):
        """Returns whether or not the "tree" field is present."""
        return "tree" in self.dict

    @property
    def tree(self):
        """Returns the archive tree json as a dict."""
        return self.dict["tree"]

    def stable_tree(self, tree):
        """Returns a stable version of the "tree" field.

        Returns the archive tree json as a dict with fields that change
        from test to test (creation and revision dates) removed.
        """
        if isinstance(tree, dict):
            return {
                field: self.stable_tree(tree[field])
                for field in self._stable_tree_fields
                if field in tree
            }
        elif isinstance(tree, list):
            return [self.stable_tree(element) for element in tree]
        else:
            return tree

    @property
    def has_content(self):
        """Returns whether or not the "content" field is present."""
        return "content" in self.dict

    @property
    def content(self):
        """Returns the archive content xml as a string."""
        return self.dict["content"]

    @property
    def stable_content(self):
        """Returns a stable version of the "content" field.

        Returns the archive content xml as a string with fields that change
        from test to test (creation and revision dates) removed.
        """
        # Remove creation time
        content = re.sub(self._created_date_regex, "", self.content)

        # Remove revision time
        content = re.sub(self._revised_date_regex, "", content)

        # Remove data-cnxml-to-html-ver from the body tag
        content = re.sub(self._cnxml_html_version_regex, "", content)

        return content

    @property
    def stable_dict(self):
        """Returns a stable version of the full archive json as a dict.

        Returns from the archive json only fields that are
        guaranteed not to change from test to test as a dict.

        This includes the whitelisted fields in the _stable_fields array,
        plus stable versions of the tree and content fields, if present.
        """
        result = {field: self.dict[field] for field in self._stable_fields if field in self.dict}

        if self.has_tree:
            result.update(tree=self.stable_tree(self.tree))

        if self.has_content:
            result.update(content=self.stable_content)

        return result
