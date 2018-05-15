# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

import uuid

import xml.etree.ElementTree as ET

from tests import markers

from pages.legacy.login_form import LoginForm
from pages.legacy.module_edit import ModuleEdit
from pages.legacy.published_module import PublishedModule
from pages.archive.legacy_content import LegacyContent


class TestCreateImportPublishModule(object):

    _module_title = None

    _expected_archive_first_p_content = (b'<html:p xmlns:html="http://www.w3.org/1999/xhtml"'
                                         b' id="test">\n     Hello World!\n  </html:p>\n')

    @markers.legacy
    @markers.slow
    def test_create_module(self, legacy_base_url, legacy_username, legacy_password, selenium):
        # GIVEN a logged in user on their dashboard
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_dashboard = login_page.login(legacy_username, legacy_password)

        # WHEN the user clicks to create a new module, agrees to the license and fills in the Title
        cc_license = my_dashboard.create_module()
        module_metadata = cc_license.agree().submit()
        self.__class__._module_title = 'CNX Automation Test Module {uuid}'.format(uuid=uuid.uuid4())
        module_edit = module_metadata.fill_in_title(self.__class__._module_title).submit()

        # THEN the user is brought to the module editor
        assert type(module_edit) is ModuleEdit
        assert module_edit.title == self.__class__._module_title
        assert module_edit.blank

    @markers.legacy
    @markers.slow
    def test_import_module(self, hello_world_cnxml_filepath, legacy_base_url,
                           legacy_username, legacy_password, selenium):
        # GIVEN a logged in user on their dashboard with a module created from the previous test
        if self.__class__._module_title is None:
            pytest.skip('This test requires a CNX module from a previous test that failed')
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_dashboard = login_page.login(legacy_username, legacy_password)
        assert my_dashboard.last_modified_module_title == self.__class__._module_title

        # WHEN the user accesses the previous module and triggers an import
        module_edit = my_dashboard.edit_last_modified_module()
        module_import = module_edit.select_import_format('plain').click_import()
        module_edit = module_import.fill_in_filename(hello_world_cnxml_filepath).submit()

        # THEN the user is back to the module editor and the module gets the imported content
        assert type(module_edit) is ModuleEdit
        assert module_edit.title == self.__class__._module_title
        assert not module_edit.blank

    @markers.legacy
    @markers.slow
    def test_publish_module(self, archive_base_url, legacy_base_url,
                            legacy_username, legacy_password, selenium):
        # GIVEN a logged in user on their dashboard with a module created from the previous test
        if self.__class__._module_title is None:
            pytest.skip('This test requires a CNX module from a previous test that failed')
        login_page = LoginForm(selenium, legacy_base_url).open()
        my_dashboard = login_page.login(legacy_username, legacy_password)
        assert my_dashboard.last_modified_module_title == self.__class__._module_title

        # WHEN the user accesses the previous module and triggers publication
        module_edit = my_dashboard.edit_last_modified_module()
        module_publish = module_edit.publish()
        module_confirm_publish = module_publish.submit()
        published_module = module_confirm_publish.submit()

        # THEN the user is brought to the published module page and the content is in CNX archive
        assert type(published_module) is PublishedModule
        assert published_module.title == self.__class__._module_title
        archive_content = LegacyContent(selenium, archive_base_url,
                                        module_id=published_module.id).open()
        assert archive_content.title == self.__class__._module_title
        content = ET.fromstring(archive_content.content)
        first_p = content.find('.//{http://www.w3.org/1999/xhtml}p')
        assert ET.tostring(first_p) == self._expected_archive_first_p_content
