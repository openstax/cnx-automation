# cnx-automation

[![Build Status](https://travis-ci.org/openstax/cnx-automation.svg?branch=master)](https://travis-ci.org/openstax/cnx-automation)

## Getting started

### Clone the repository

If you have cloned this project already then you can skip this, otherwise you'll
need to clone this repo using Git. If you do not know how to clone a GitHub
repository, check out this [help page][git-clone] from GitHub.

## How to run the tests using Docker

### Install Docker and Docker Compose

Follow the instructions to install [Docker](https://docs.docker.com/install/).

Follow the instructions to install [Docker Compose](https://docs.docker.com/compose/install/).

### Run Docker Compose

    $ docker-compose up -d

### Execute the tests

    $ docker-compose exec --user root selenium-chrome tox

> Note: The [Run the tests](#run-the-tests) section covers how to pass arguments to tox in order to target specific tests

## How to run the tests locally

### Install dependencies

#### Create a virtualenv

    $ make venv

#### Activate the virtualenv

    $ source .env/bin/activate

### Set username and password for legacy tests

If you intend to run the legacy tests, you will need to set the LEGACY_USERNAME
and LEGACY_PASSWORD environment variables. You can either export them from your
shell profile or simply add them to a `.env` file in the root dir of this repo.

### Run the tests

Tests are run using the command line using the `tox` command. By default this
will run all of the environments configured, including checking your tests against
recommended style conventions using [flake8][flake8].

To run against a different base URL, pass in a value for `--base-url`:

```bash
$ tox -- --base-url=https://qa.cnx.org
```

To run Chrome in headless mode, pass in `--headless` or set the HEADLESS environment variable:

```bash
$ tox -- --headless
```

To run against a different browser, pass in a value for `--driver`:

```bash
$ tox -- --driver=Chrome
```

To run a specific test, pass in a value for `-k`:

```bash
$ tox -- -k=test_my_feature
```

### Additional Options

The pytest plugin that we use for running tests has a number of advanced
command line options available. To see the options available, run
`pytest --help`. The full documentation for the plugin can be found
[here][pytest-selenium].

## Framework Design

This testing framework heavily relies on the [PyPOM][pypom]. The [PyPOM][pypom]
library is the Python implementation of the [PageObject][pageobject] design pattern.

The [PageObject][pageobject] pattern creates a nice API abstraction around
an HTML page allowing the test creator to focus on the intent of a test
rather than decyphering HTML code. This design pattern makes the test framework
much more maintainable as any code changes to the page can occur in the
[PageObject][pageobject] rather than within the test code.

According to Siman Stewart,

> If you have WebDriver APIs in your test methods, You're Doing It Wrong.

The usage of [pytest][pytest], [pytest-selenium][pytest-selenium] plugin,
and the [PageObject][pageobject] pattern allows for a succinct test structure
like so:

```python
from tests import markers

from pages.home import Home

@markers.webview
@markers.nondestructive
def test_nav_is_displayed(base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The main website URL is fully loaded
    page = Home(selenium, base_url).open()

    # THEN The navbar is displayed
    assert page.header.is_nav_displayed
```

The inspiration for this framework is based on the [Mozilla Addons Server Project][mozilla]
and plenty of examples can be gleamed from their fantastic usage of the
pattern.

[cnx-org]: https://cnx.org
[git-clone]: https://help.github.com/articles/cloning-a-repository/
[python]: https://www.python.org/downloads/
[flake8]: http://flake8.readthedocs.io/
[pytest-selenium]: http://pytest-selenium.readthedocs.org/
[pypom]: https://pypom.readthedocs.io/en/latest/user_guide.html#regions
[pageobject]: https://martinfowler.com/bliki/PageObject.html
[pytest]: https://docs.pytest.org/en/latest/
[mozilla]: https://github.com/mozilla/addons-server
