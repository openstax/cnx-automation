from playwright.sync_api import sync_playwright
import pytest


@pytest.fixture
def corgi_base_url():
    """Return local corgi url"""
    corgi_base_url = "https://corgi-staging.ce.openstax.org/"
    return corgi_base_url


@pytest.fixture
def chrome_browser():

    playwright_sync = sync_playwright().start()
    chromebrowser = playwright_sync.chromium.launch(headless=True, slow_mo=400)

    yield chromebrowser

    chromebrowser.close()
    playwright_sync.stop()


@pytest.fixture
def chrome_page(chrome_browser, corgi_user, corgi_password):
    context = chrome_browser.new_context(
        http_credentials={"username": corgi_user, "password": corgi_password}
    )
    page = context.new_page()

    return page


@pytest.fixture
def corgi_user(request):
    """Return value of the corgi username"""
    config = request.config
    corgi_user = config.getoption("corgi_user") or config.getini("corgi_user")
    if corgi_user is not None:
        return corgi_user


@pytest.fixture
def corgi_password(request):
    """Return value of the corgi password"""
    config = request.config
    corgi_password = config.getoption("corgi_password") or config.getini("corgi_password")
    if corgi_password is not None:
        return corgi_password
