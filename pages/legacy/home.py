# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PublicPage


class Home(PublicPage):

    @property
    def loaded(self):
        return super().loaded and self.my_account.loaded
