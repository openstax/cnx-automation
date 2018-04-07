import pytest


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(20)
    return selenium
