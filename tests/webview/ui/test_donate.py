# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.webview.home import Home
from pages.webview.donate_form import DonateForm


@markers.webview
@markers.nondestructive
def test_donate_form_loads(base_url, selenium):
    # GIVEN the home page
    home = Home(selenium, base_url).open()

    # WHEN the donate link is clicked and then the donate now button is clicked
    donate = home.header.click_donate()
    donate_form = donate.submit()

    # THEN the donate form is displayed
    assert type(donate_form) is DonateForm
    assert donate_form.amount == 10
