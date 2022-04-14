from pages.corgi.home import HomeCorgi
import pytest


@pytest.mark.parametrize(
    "colid, version, style",
    [("osbooks-astronomy/astronomy-2e", "latest", "astronomy")],
)
def test_corgi_git_job_e2e(chrome_page, chrome_browser, corgi_base_url, colid, version, style):

    chrome_page.set_default_timeout(2100000)

    chrome_page.goto(corgi_base_url)
    home_corgi = HomeCorgi(chrome_page)

    home_corgi.click_create_new_job_button()
    home_corgi.click_git_radio_button()

    home_corgi.fill_collection_id(colid)
    home_corgi.fill_version(version)
    home_corgi.fill_book_style(style)

    home_corgi.click_create_button()

    print(f"\n--->>> git job has been created in {corgi_base_url}")


@pytest.mark.parametrize(
    "colid, style",
    [("osbooks-business-ethics/business-ethics", "business-ethics")],
)
def test_corgi_git_preview_job_e2e(chrome_page, chrome_browser, corgi_base_url, colid, style):

    chrome_page.set_default_timeout(2100000)

    chrome_page.goto(corgi_base_url)
    home_corgi = HomeCorgi(chrome_page)

    home_corgi.click_create_new_job_button()
    home_corgi.click_git_preview_radio_button()

    home_corgi.fill_collection_id(colid)
    home_corgi.fill_book_style(style)

    home_corgi.click_create_button()

    print(f"\n--->>> git preview job has been created in {corgi_base_url}")
