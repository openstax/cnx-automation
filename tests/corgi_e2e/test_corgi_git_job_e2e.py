from pages.corgi.home import Home


def test_corgi_git_job_e2e(chrome_browser, chrome_page):

    chrome_page.set_default_timeout(999999)

    chrome_page.goto("https://corgi-staging.openstax.org")

    new_job = Home(chrome_page)

    new_job.click_create_new_job_button()
    new_job.click_git_radio_button()

    new_job.fill_collection_id("osbooks-statistics/statistics")
    new_job.fill_version("latest")
    new_job.fill_book_style("statistics")

    new_job.click_create_button()

    new_job.start_date_time.wait_for()
    new_job.job_state_completed.wait_for()
    new_job.git_view_link.wait_for()

    job_id = new_job.job_id_locator.text_content()

    with chrome_page.expect_popup() as popup_info:
        new_job.git_view_link.click()

    popup = popup_info.value
    popup.wait_for_load_state()

    assert popup.locator("text=Contents") and popup.locator("text=Preface")
    assert job_id and ".pdf" in popup.url

    chrome_browser.close()
