import requests
from tests import markers


@markers.test_case("C553092")
@markers.rex
@markers.nondestructive
def test_redirecting_to_rex_from_within_webview(
    webview_base_url, rex_base_url, selenium, redirecting_books_titles
):
    """Webview needs to redirect to REX when any of the featured books is a REX book/page (list from the spreadsheet).
    https://github.com/openstax/cnx/issues/401
    """

    for book in redirecting_books_titles:
        data = requests.get(book)
        url = data.url

        assert rex_base_url in url
        assert 200 == data.status_code
