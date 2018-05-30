# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pypom


class Region(pypom.Region):
    @property
    def text(self):
        return self.root.text

    @property
    def loaded(self):
        if self._root_locator is None:
            return self.root is not None
        else:
            return self.page.is_element_present(*self._root_locator)
