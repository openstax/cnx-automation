# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import NoSuchElementException

from tests import markers

from pages.legacy.login_form import LoginForm
from pages.legacy.module_edit import ModuleEdit
from pages.legacy.collection_edit import CollectionEdit
from pages.legacy.content_published import ContentPublished
from pages.archive.legacy_content import LegacyContent

from regions.legacy.collection import Collection
from regions.legacy.module import Module


class TestNoSelfCloseCreateImportPublishModuleAndCollection(object):
    _module_temp_id = None
    _module_id = None
    _collection_temp_id = None

    @markers.legacy
    @markers.slow
    def test_noselfclose_create_module(self, legacy_base_url, legacy_username, legacy_password, selenium):
        # GIVEN a logged in user on their dashboard
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_cnx = login_page.login(legacy_username, legacy_password)

        # WHEN the user clicks to create a new module, agrees to the license and fills in the Title
        cc_license = my_cnx.create_module()
        metadata_edit = cc_license.agree().submit()
        module_edit = metadata_edit.fill_in_title("CNX Automation Test Module").submit()

        # THEN the user is brought to the module editor
        assert type(module_edit) is ModuleEdit
        assert module_edit.title == "CNX Automation Test Module"
        assert module_edit.is_blank

        # Other tests will be skipped unless this test succeeds and set this class variable
        self.__class__._module_temp_id = module_edit.id

    @markers.legacy
    @markers.slow
    def test_noselfclose_import_module(
        self,
        not_self_closing_cnxml_filepath,
        legacy_base_url,
        legacy_username,
        legacy_password,
        selenium,
    ):
        # GIVEN a logged in user on their dashboard with a module created in the previous test
        if self.__class__._module_temp_id is None:
            pytest.skip("This test requires a CNX module from a previous test that failed")
        login_page = LoginForm(selenium, legacy_base_url).open()
        login_page.login(legacy_username, legacy_password)

        # WHEN the user accesses the previous module and triggers an import
        module_edit = ModuleEdit(
            selenium,
            legacy_base_url,
            username=legacy_username,
            module_id=self.__class__._module_temp_id,
        ).open()
        module_import = module_edit.select_import_format("plain").click_import()
        module_edit = module_import.fill_in_filename(not_self_closing_cnxml_filepath).submit()

        # THEN the user is back to the module editor and the module gets the imported content
        assert type(module_edit) is ModuleEdit
        assert module_edit.title == "CNX Automation Test Module"
        assert not module_edit.is_blank

    @markers.legacy
    @markers.slow
    def test_noselfclose_publish_module(
        self,
        archive_base_url,
        legacy_base_url,
        legacy_username,
        legacy_password,
        selenium,
        snapshot,
    ):
        # GIVEN a logged in user on their dashboard with a module created in the previous test
        if self.__class__._module_temp_id is None:
            pytest.skip("This test requires a CNX module from a previous test that failed")
        login_page = LoginForm(selenium, legacy_base_url).open()
        login_page.login(legacy_username, legacy_password)

        # WHEN the user accesses the previous module and triggers publication
        module_edit = ModuleEdit(
            selenium,
            legacy_base_url,
            username=legacy_username,
            module_id=self.__class__._module_temp_id,
        ).open()
        content_publish = module_edit.publish()
        confirm_publish = content_publish.submit()
        try:
            content_published = confirm_publish.submit()
        except NoSuchElementException:
            pytest.fail("Publish button not found. Ensure your user has publish permissions")

        # THEN the user is brought to the published module page and the content is in CNX archive
        assert type(content_published) is ContentPublished
        assert content_published.title == "CNX Automation Test Module"
        module_id = content_published.id
        archive_content = LegacyContent(
            selenium, archive_base_url, legacy_id=content_published.id
        ).open()
        assert archive_content.title == "CNX Automation Test Module"
        snapshot.assert_dict_match(archive_content.stable_dict, "legacy/not_self_closing.json")

        # Other tests will be skipped unless this test succeeds and set this class variable
        self.__class__._module_id = module_id

