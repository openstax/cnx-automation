# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.webview.base import Page


class Donate(Page):
    OPENSTAX_GIVE_URL = 'https://openstax.org/give'

    @property
    def is_openstax_org_give_page(self):
        return self.driver.current_url == self.OPENSTAX_GIVE_URL
