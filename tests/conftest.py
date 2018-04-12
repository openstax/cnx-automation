import pytest


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(0)
    return selenium
