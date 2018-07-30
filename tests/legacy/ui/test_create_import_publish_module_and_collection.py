# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from tests import markers

from pages.legacy.login_form import LoginForm
from pages.legacy.module_edit import ModuleEdit
from pages.legacy.collection_edit import CollectionEdit
from pages.legacy.content_published import ContentPublished
from pages.archive.legacy_content import LegacyContent

from regions.legacy.collection import Collection
from regions.legacy.module import Module


class TestCreateImportPublishModuleAndCollection(object):
    _module_temp_id = None
    _module_id = None
    _collection_temp_id = None

    @markers.legacy
    @markers.slow
    def test_create_module(self, legacy_base_url, legacy_username, legacy_password, selenium):
        # GIVEN a logged in user on their dashboard
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_cnx = login_page.login(legacy_username, legacy_password)

        # WHEN the user clicks to create a new module, agrees to the license and fills in the Title
        cc_license = my_cnx.create_module()
        metadata_edit = cc_license.agree().submit()
        module_edit = metadata_edit.fill_in_title('CNX Automation Test Module').submit()

        # THEN the user is brought to the module editor
        assert type(module_edit) is ModuleEdit
        assert module_edit.title == 'CNX Automation Test Module'
        assert module_edit.is_blank

        # Other tests will be skipped unless this test succeeds and set this class variable
        self.__class__._module_temp_id = module_edit.id

    @markers.legacy
    @markers.slow
    def test_import_module(self, m46922_1_13_cnxml_filepath, legacy_base_url,
                           legacy_username, legacy_password, selenium):
        # GIVEN a logged in user on their dashboard with a module created in the previous test
        if self.__class__._module_temp_id is None:
            pytest.skip('This test requires a CNX module from a previous test that failed')
        login_page = LoginForm(selenium, legacy_base_url).open()
        login_page.login(legacy_username, legacy_password)

        # WHEN the user accesses the previous module and triggers an import
        module_edit = ModuleEdit(selenium, legacy_base_url, username=legacy_username,
                                 module_id=self.__class__._module_temp_id).open()
        module_import = module_edit.select_import_format('plain').click_import()
        module_edit = module_import.fill_in_filename(m46922_1_13_cnxml_filepath).submit()

        # THEN the user is back to the module editor and the module gets the imported content
        assert type(module_edit) is ModuleEdit
        assert module_edit.title == 'CNX Automation Test Module'
        assert not module_edit.is_blank

    @markers.legacy
    @markers.slow
    def test_publish_module(self, archive_base_url, legacy_base_url,
                            legacy_username, legacy_password, selenium, snapshot):
        # GIVEN a logged in user on their dashboard with a module created in the previous test
        if self.__class__._module_temp_id is None:
            pytest.skip('This test requires a CNX module from a previous test that failed')
        login_page = LoginForm(selenium, legacy_base_url).open()
        login_page.login(legacy_username, legacy_password)

        # WHEN the user accesses the previous module and triggers publication
        module_edit = ModuleEdit(selenium, legacy_base_url, username=legacy_username,
                                 module_id=self.__class__._module_temp_id).open()
        content_publish = module_edit.publish()
        confirm_publish = content_publish.submit()
        content_published = confirm_publish.submit()

        # THEN the user is brought to the published module page and the content is in CNX archive
        assert type(content_published) is ContentPublished
        assert content_published.title == 'CNX Automation Test Module'
        module_id = content_published.id
        archive_content = LegacyContent(selenium, archive_base_url,
                                        legacy_id=content_published.id).open()
        assert archive_content.title == 'CNX Automation Test Module'
        snapshot.assert_dict_match(archive_content.stable_dict, 'legacy/m46922_1.13.json')

        # Other tests will be skipped unless this test succeeds and set this class variable
        self.__class__._module_id = module_id

    @markers.legacy
    @markers.slow
    def test_create_collection(self, legacy_base_url, legacy_username, legacy_password, selenium):
        # GIVEN a logged in user on their dashboard with a module created in the previous test
        if self.__class__._module_temp_id is None:
            pytest.skip('This test requires a CNX module from a previous test that failed')
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_cnx = login_page.login(legacy_username, legacy_password)

        # WHEN the user clicks to create a new collection,
        # agrees to the license and fills in the Title
        cc_license = my_cnx.create_collection()
        metadata_edit = cc_license.agree().submit()
        collection_edit = metadata_edit.fill_in_title('CNX Automation Test Collection').submit()

        # THEN the user is brought to the collection editor
        assert type(collection_edit) is CollectionEdit
        assert collection_edit.title == 'CNX Automation Test Collection'
        assert collection_edit.root_collection.is_empty

        # Other tests will be skipped unless this test succeeds and set this class variable
        self.__class__._collection_temp_id = collection_edit.id

    @markers.legacy
    @markers.slow
    def test_add_content_to_collection(self, legacy_base_url, legacy_username,
                                       legacy_password, selenium):
        # GIVEN a logged in user on their dashboard with a module created in the previous test
        if self.__class__._collection_temp_id is None or self.__class__._module_id is None:
            pytest.skip('This test requires a CNX collection and '
                        'a CNX module from previous tests that failed')
        login_page = LoginForm(selenium, legacy_base_url).open()
        login_page.login(legacy_username, legacy_password)

        # WHEN the user accesses the previous collection and adds some content
        collection_edit = CollectionEdit(selenium, legacy_base_url, username=legacy_username,
                                         collection_id=self.__class__._collection_temp_id).open()
        root_collection = collection_edit.root_collection
        add_subcollections = root_collection.add_subcollections()
        collection = add_subcollections.fill_in_titles('CNX Automation Test Subcollection').submit()
        add_modules = collection.add_modules()
        add_modules = add_modules.fill_in_search_words(self.__class__._module_id).submit_search()
        module = add_modules.add_workarea().submit()

        # THEN the user is back to the collection editor and the collection gets the new content
        assert type(collection) is Collection
        assert type(module) is Module
        assert not root_collection.is_empty
        assert collection.title == 'CNX Automation Test Subcollection'
        assert not collection.is_empty
        assert module.title == 'CNX Automation Test Module'

    @markers.legacy
    @markers.test_case('C195231')
    @markers.slow
    def test_publish_collection(self, archive_base_url, legacy_base_url,
                                legacy_username, legacy_password, selenium, snapshot):
        # GIVEN a logged in user on their dashboard with a collection created in the previous test
        if self.__class__._collection_temp_id is None or self.__class__._module_id is None:
            pytest.skip('This test requires a CNX collection and '
                        'a CNX module from previous tests that failed')
        login_page = LoginForm(selenium, legacy_base_url).open()
        login_page.login(legacy_username, legacy_password)

        # WHEN the user accesses the previous collection and triggers publication
        collection_edit = CollectionEdit(selenium, legacy_base_url, username=legacy_username,
                                         collection_id=self.__class__._collection_temp_id).open()
        content_publish = collection_edit.publish()
        confirm_publish = content_publish.fill_in_message('Created collection').submit()
        content_published = confirm_publish.submit()

        # THEN the user is brought to the published collection page
        # and the content is in CNX archive
        assert type(content_published) is ContentPublished
        assert content_published.title == 'CNX Automation Test Collection'
        archive_content = LegacyContent(selenium, archive_base_url,
                                        legacy_id=content_published.id).open()
        assert archive_content.title == 'CNX Automation Test Collection'
        snapshot.assert_dict_match(archive_content.stable_dict, 'legacy/col_with_m46922_1.13.json')

    @markers.legacy
    @markers.test_case('C195231')
    @markers.slow
    def test_mathmal3_valid_in_legacy(self, legacy_base_url, legacy_username,
                                      legacy_password, sample_mathml3_cnxml_filepath, selenium):
        # GIVEN a logged in user on their dashboard, and the sample mathml3
        with open(sample_mathml3_cnxml_filepath) as file:
            sample = file.read()
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_cnx = login_page.login(legacy_username, legacy_password)

        # WHEN the user clicks to create a new module,
        # agrees to the license and fills in the Title
        cc_license = my_cnx.create_module()
        metadata_edit = cc_license.agree().submit()
        module_edit = metadata_edit.fill_in_title('CNX Automation Test MathMl3').submit()

        # AND click full source editing to edit
        module_edit.edit_method.full_source_editing()
        module_edit.edit_content_text(sample)

        # THEN save and msg shows 'Saved'
        module_edit.save()
        assert module_edit.portal_msg == 'Saved.'

    @markers.legacy
    @markers.test_case('C175153')
    @markers.slow
    def test_empty_collection_publish_not_allowed(self, legacy_base_url, legacy_username,
                                                  legacy_password, selenium):
        # GIVEN a logged in user on their dashboard
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_cnx = login_page.login(legacy_username, legacy_password)

        # WHEN the user clicks to create a new collection,
        # agrees to the license and fills in the Title
        cc_license = my_cnx.create_collection()
        metadata_edit = cc_license.agree().submit()
        collection_edit = metadata_edit.fill_in_title('CNX Automation Test Collection').submit()

        # THEN click publish and publish is blocked (block msg, no submit button)
        content_published = collection_edit.publish()
        assert content_published.block_msg
