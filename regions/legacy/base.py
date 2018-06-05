# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pypom

from selenium.common.exceptions import StaleElementReferenceException


class Region(pypom.Region):

    @property
    def unloaded(self):
        """Can be overridden in subclasses."""
        return not self.loaded

    def wait_for_region_to_unload(self):
        """Wait for the region to unload."""

        # If we get a StaleElementReferenceException while waiting for the region to unload,
        # we consider that it already unloaded
        try:
            self.wait.until(lambda _: self.unloaded)
        except StaleElementReferenceException:
            pass

        return self
