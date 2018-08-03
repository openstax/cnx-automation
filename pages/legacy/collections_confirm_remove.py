# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.confirm_remove import ConfirmRemove


class CollectionsConfirmRemove(ConfirmRemove):

    def confirm(self):
        self.remove_button.click()
        from pages.legacy.workspace_collection import WorkspaceCollection
        collections = WorkspaceCollection(self.driver, self.base_url, self.timeout)
        return collections.wait_for_page_to_load()
