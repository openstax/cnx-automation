# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pypom


class Region(pypom.Region):

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def text(self):
        return self.root.text

    @property
    def loaded(self):
        if self._root_locator is None:
            return self.root is not None
        else:
            return self.page.is_element_present(*self._root_locator)

    @property
    def is_displayed(self):
        return self.root.is_displayed()

    def wait_for_region_to_display(self):
        self.page.wait_for_region_to_display(self)
        return self

    def wait_for_element_to_display(self, element):
        return self.page.wait_for_element_to_display(element)

    def focus(self, element=None):
        """Focus (and scrolls to) the given element (or the region's root). Returns the element."""
        if element is None:
            element = self.root
        return self.page.focus(element)

    def offscreen_click(self, element=None):
        """Clicks an offscreen element (or the region's root).

        Clicks the given element, even if it is offscreen, by sending the ENTER key.
        Returns the element.
        """
        if element is None:
            element = self.root
        return self.page.offscreen_click(element)
