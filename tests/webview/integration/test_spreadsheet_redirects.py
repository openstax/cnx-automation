import requests
from tests import markers
import webbrowser
from lxml import html


@markers.otto
@markers.test_case("C553080")
@markers.nondestructive
def test_redirecting_to_rex_from_within_webview(
    webview_base_url, rex_base_url, selenium, redirecting_books_titles
):
    """Webview needs to redirect to REX when any of the featured books is a REX book.
    https://github.com/openstax/cnx/issues/401
    """

    for book in redirecting_books_titles:
        data = requests.get(book)
        url = data.url

        print()
        print("REDIRECTED FROM: ", book)
        print("REDIRECTED TO  : ", url)
        print("STATUS CODE    : ", data.status_code)
        print()

        assert rex_base_url in url
        assert 200 == data.status_code
