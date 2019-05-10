from tests import markers
from pages.webview.home import Home

APP_NAME = '- CNX HOMEPAGE BOOKS VISUAL VERIFICATION -'

# Verifies all the openstax featured books on the cnx homepage
# by visually comparing them to a set of baseline images

@markers.webview
@markers.nondestructive
def test_home_objects(applitools, webview_base_url, selenium):

    try:

        home = Home(selenium, webview_base_url).open()

        # Start the test and set the browser's viewport size to 1400x820
        applitools.open(driver=selenium, app_name=APP_NAME, test_name='Test homepage books', viewport_size={'width': 1400, 'height': 820})

        # list of all openstax featured cnx books (without user content)
        openstax_books = home.featured_books.openstax_list

        for i in range(len(openstax_books)):
            openstax_books[i].click_show_more()

            if i % 4 == 0:
                # Visual checkpoint - cnx homepage screenshot
                applitools.check_window('-> {}'.format(webview_base_url))

        # End the test
        applitools.close()

    finally:

        # If the test was aborted before applitools.close was called, ends the test as aborted
        applitools.abort_if_not_closed()

        assert applitools.api_key
