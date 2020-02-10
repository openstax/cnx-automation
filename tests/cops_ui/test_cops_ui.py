import requests
from tests import markers
from selenium.webdriver.common.keys import Keys

cops_base_url = "https://cops-staging.openstax.org"
new_pdf_xp = (
    '// *[ @ id = "app"] / div[1] / main / div / div / div / div / div[1] / button / span / span'
)
create_xp = '//*[@id="app"]/div[3]/div/div/div[3]/button[2]/span'


@markers.parametrize(
    "colid, style, bserver", [("col11992", "astronomy", "qa"), ("col11496", "anatomy", "staging")]
)
def test_cops_ui(selenium, colid, style, bserver):

    # GIVEN an archive URL for a book
    url = f"{cops_base_url}"

    # WHEN making a request to Archive
    response = requests.get(url)

    selenium.get(url)
    new_pdf = selenium.find_element_by_xpath(new_pdf_xp)
    new_pdf.click()

    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, colid)
    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB)
    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, style)
    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, bserver)

    create_button_xp = selenium.find_element_by_xpath(create_xp)
    create_button_xp.click()
    create_button_xp.click()

    # THEN we should NOT redirect to REX
    assert response.status_code == 200
