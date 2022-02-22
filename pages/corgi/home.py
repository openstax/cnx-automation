class Home:
    def __init__(self, page):
        self.page = page

    @property
    def create_new_job_button_locator(self):
        return self.page.wait_for_selector("text=create a new job")

    def click_create_new_job_button(self):
        self.create_new_job_button_locator.click()

    @property
    def pdf_radio_button_locator(self):
        return self.page.wait_for_selector("div.v-radio.pdf-radio-button")

    def click_pdf_radio_button(self):
        self.pdf_radio_button_locator.click()

    @property
    def git_radio_button_locator(self):
        return self.page.wait_for_selector("div.v-radio.git-pdf-radio-button")

    def click_git_radio_button(self):
        self.git_radio_button_locator.click()

    @property
    def git_preview_radio_button_locator(self):
        return self.page.wait_for_selector("div.v-radio.git-preview-radio-button")

    def click_git_preview_radio_button(self):
        self.git_preview_radio_button_locator.click()

    @property
    def collection_id_locator(self):
        return self.page.wait_for_selector(
            "div:nth-child(2) > div:nth-child(1) > div > div > div.v-input__slot > div > label"
        )

    def fill_collection_id(self, value):
        self.collection_id_locator.fill(value)

    @property
    def version_locator(self):
        return self.page.wait_for_selector(
            "div:nth-child(2) > div:nth-child(2) > div > div > div.v-input__slot > div > label"
        )

    def fill_version(self, value):
        self.version_locator.fill(value)

    @property
    def book_style_locator(self):
        return self.page.wait_for_selector(
            "div:nth-child(2) > div:nth-child(3) > div > div > div.v-input__slot > div.v-select__slot > label"
        )

    def fill_book_style(self, value):
        self.book_style_locator.fill(value)

    @property
    def content_server_locator(self):
        return self.page.locator(
            "div:nth-child(2) > div:nth-child(4) > div > div > div.v-input__slot > div.v-select__slot > label"
        )

    def click_content_server(self):
        self.content_server_locator.click()

    @property
    def content_server_dropdown_locator(self):
        return self.page.locator("div.v-menu__content")

    def click_content_server_dropdown(self, value):
        self.content_server_dropdown_locator.locator(f"text={value}").click()

    @property
    def create_button_locator(self):
        return self.page.locator("button.create-button-start-job")

    def click_create_button(self):
        self.create_button_locator.locator("text=Create").click()
        self.create_button_locator.locator("text=Create").click()

    def click_create_button_pdf(self):
        self.create_button_locator.locator("text=Create").click()

    @property
    def job_state_locator(self):
        return self.page.locator("tr:nth-child(1) > td:nth-child(9)")

    @property
    def job_state_completed(self):
        return self.job_state_locator.locator("text=completed")

    @property
    def git_preview_link_locator(self):
        return self.page.locator(
            "div:nth-child(3) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8) > ul > li:nth-child(2)"
        )

    @property
    def git_preview_link(self):
        return self.git_preview_link_locator.locator("text=View - Rex Web Prod")

    @property
    def git_view_locator(self):
        return self.page.locator(
            "div:nth-child(3) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8)"
        )

    @property
    def git_view_link(self):
        return self.git_view_locator.locator("text=View")

    @property
    def pdf_view_locator(self):
        return self.page.locator(
            "div:nth-child(3) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(8)"
        )

    @property
    def pdf_view_link(self):
        return self.pdf_view_locator.locator("text=View")

    @property
    def start_date_time_locator(self):
        return self.page.locator(
            "div:nth-child(3) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(7)"
        )

    @property
    def start_date_time(self):
        return self.start_date_time_locator.locator("text=a few seconds ago")

    @property
    def job_id_locator(self):
        return self.page.locator(
            "div:nth-child(3) > div > div > table > tbody > tr:nth-child(1) > td:nth-child(7) > time"
        )
