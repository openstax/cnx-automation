import requests
from tests import markers
from selenium.webdriver.common.keys import Keys

cops_api_url = "https://cops-staging.openstax.org/api/jobs/"


def test_api_results(selenium):

    # GIVEN an archive URL for a book
    url = f"{cops_api_url}"

    new_api = url[0 - 9]
    print(new_api)


#    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, colid)
#    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB)
#    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, style)
#    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, bserver)

#    create_button_xp = selenium.find_element_by_xpath(create_xp)
#    create_button_xp.click()
#    create_button_xp.click()

# THEN we should NOT redirect to REX
#    assert response.status_code == 200
