# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page


class Base(Page):

    def __init__(self, driver, base_url, timeout=15):
        super().__init__(driver, base_url, timeout)
