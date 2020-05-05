# cnx-automation

[![CircleCI](https://circleci.com/gh/openstax/cnx-automation/tree/master.svg?style=svg)](https://circleci.com/gh/openstax/cnx-automation/tree/master)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

# Getting started

## Clone the repository

If you have cloned this project already then you can skip this, otherwise you'll
need to clone this repo using Git. If you do not know how to clone a GitHub
repository, check out this [help page][git-clone] from GitHub.

## How to run the tests using Docker

### Install Docker and Docker Compose

Follow the instructions to install [Docker](https://docs.docker.com/install/).

Follow the instructions to install [Docker Compose](https://docs.docker.com/compose/install/).

### Docker first run

If you have a fresh cloned repository ignore this step.

If you have run this repo without docker before please run to delete e.g. prebuilt `.pyc` files:

    $ make clean

### Run Docker Compose

    $ docker-compose up -d selenium-chrome

### Execute the tests

It's necessary for reducing the amount of time that it takes for test collection
to be specific about the set of tests you'd like to execute.

You do this by adding the test folder you want pytest to scan for tests. Typically,
the folders follow the following format `/tests/<application>/<type of test>. 
The following test folders exist for running tests with pytest:

* ./tests/webview/integration
* ./tests/webview/ui
* ./tests/webview/vendorbooks
* ./tests/archive/integration
* ./tests/legacy/ui
* ./tests/cops
* ./tests/neb/ui

An example on how to target the UI test for webview is below:

    $ docker-compose exec selenium-chrome pytest tests/webview/ui


> Note: The [Run the tests using pytest](#run-the-tests-using-pytest) section covers how to pass arguments to pytest in order to target specific tests

### View the browser

List the docker containers and find the one for selenium-chrome

    $ docker container ls

A table will be displayed with column names. Find the one labeled PORTS

    PORTS
    4444/tcp, 0.0.0.0:32778->5900/tcp

Use a VNC application to connect to `0.0.0.0:32778`. The port number `32778` may be different.
The password for the VNC session is `secret`.

Execute the tests as described above.

    $ docker-compose exec selenium-chrome pytest

Switch over to the VNC window to see your tests running!

## How to prepare the project locally

### Install dependencies

#### Install Selenium Chrome WebDriver

    $ brew cask install chromedriver    # macOS

#### Create a virtualenv

    $ make venv

#### Activate the virtualenv

    $ source .venv/bin/activate

#### Install git pre-commit hooks

This utilizes [pre-commit](https://pre-commit.com/) to format code using [black](https://github.com/ambv/black)
and lint your code using flake8. This is IDE agnostic and runs only on checked in code before a commit.

    $ make precommit

### Using dotenv for Environmental Variables

Dotenv is used by the framework to load environmental variables from a `.env` file if it exists in the root of the project directory.

This is useful for loading environment variables that use usernames. To use a .env file copy the example and fill out the values.

    $ cp .env.example .env

### Doing updates to dependencies

[pip-tools](https://pypi.org/project/pip-tools/) are utilized for updating dependencies in the framework. Pip-tools provides a number of utilities to pip that are useful for cnx-automation. Cnx-automation installs dependencies from a number of our projects that may have conflicting versions. Pip-tools will warn when there is a conflict and can help with finding compatible versions between all the dependencies and sub-dependencies.

First, install [pip-tools](https://pypi.org/project/pip-tools/):

    $ pip install pip-tools

To do updates to dependencies you'll first need to update the main dependency in [./requirements.in](./requirements.in) file.

When the dependency has been updated you can then generate the requirements.txt that will be used to install the dependencies.

    $ pip-compile --output-file=requirements.txt

### Set username and password for legacy tests

If you intend to run the legacy tests, you will need to set the LEGACY_USERNAME
and LEGACY_PASSWORD environment variables. You can either export them from your
shell profile or simply add them to a `.env` file in the root dir of this repo.

### Run the tests using pytest

When only using the `pytest` command the default environment will set to QA.

To run against a different environment pass in a value for `--webview_base_url`, `--legacy_base_url`, `--archive_base_url`:

**Staging**
```bash
$ pytest --webview_base_url https://staging.cnx.org --legacy_base_url https://legacy-staging.cnx.org --archive_base_url https://archive-staging.cnx.org tests/webview/ui
```

**Production**
```bash
$ pytest --webview_base_url https://cnx.org --legacy_base_url https://legacy.cnx.org --archive_base_url https://archive.cnx.org tests/webview/ui
```

To run a specific test or test module pass in a value for `-k`:

```bash
$ pytest -k test_about tests/webview/ui
```

To run a specific project, pass in `webview`, `legacy`, or `neb` for `-m`:

```bash
$ pytest -m webview tests/webview
```

To run a more complicated example that runs a specific project and a specific test module in headless mode:

```bash
$ pytest -m webview -k test_home --headless tests/webview/ui
```

To run tests in parallel you can combine the above and use `-n` option to specify the number of workers.

```bash
$ pytest -n 4 -m webview tests/webview/ui
```

#### Run Smoke Tests

To run smoke tests you can add the `smoke` marker to the particular project that is being tested:

```bash
$ pytest -m "webview and smoke"
```
### Run Integration Tests

To run integration tests you'll want to add teh `integration` marker and target the correct folder you want to scan for test:

```bash
$ pytest -m "webview and integration" tests/webview
```

### Additional Pytest Options

The pytest plugin that we use for running tests has a number of advanced
command line options available. To see the options available, run
`pytest --help`. The full documentation for the plugin can be found
[here][pytest-selenium].

### Uploading results to TestRail

The TestRail integration is currently intended to be used during a local test run of the cnx-automation suite when the uploading of results to TestRail is desired.

Make a copy of of the testrail.example.cfg:

    $ cp testrail.example.cfg testrail.cfg

Replace the example values with the appropriate values:

    [API]
    url = https://instance.testrail.net/
    email = testrail_user@domain.com
    password = api_key

To run the tests only for webview and a specific set of tests:

```bash
$ pytest -m webview -k test_home --testrail --testrail-name release01 tests/
```

Consult the pytest-testrail project `README.md`  for more options

https://github.com/allankp/pytest-testrail

### Marking a test that has a test case in TestRail

Use the `markers.text_case` decorator with case number to upload the results to TestRail. More than one test case can be used by separating with a comma.

```python
@markers.test_case('C10000', 'C10001')
def test_foo_uploads_bar:
```

## Framework Design

### Pytest Selenium Training

You can find more in depth documentation in our [Pytest Selenium Training][selenium-training].

### Brief Architectural Description

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
def test_nav_is_displayed(webview_base_url, selenium):
    # GIVEN the main website URL and the Selenium driver

    # WHEN The main website URL is fully loaded
    page = Home(selenium, webview_base_url).open()

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
[selenium-training]: https://qualitas-server.herokuapp.com/wiki/Introduction_to_Pytest_and_Selenium

## HOW TO CREATE TEST DATA FOR REDIRECTS

i. go to ce-scripts repo and create virtual environment: 

```pyenv virtualenv 3.7.x virtualenv_name```

activate it: 

```pyenv activate virtualenv_name```

install requirements:

```pip install -r requirements.txt```

ii. cd python

run 

```gen_book_uris.py <archive_host> <cnx_uuid>```

e.g. $ ./gen_book_uris.py archive-staging.cnx.org e42bd376-624b-4c0f-972f-e0c57998e765

iii. this will create url variations as per rex_redirects.py and stores it in output/<cnx_uuid.txt> file 

    e.g. output/e42bd376-624b-4c0f-972f-e0c57998e765.txt

iv. rex_redirects.py file can be found here: [rex_redirects][rex_redirects]

vi. copy the created cnx_uuid.txt file into cnx-automation folder: 
fixtures/data/webview/

vii. in fixtures/webview.py add fixture to read and iterate through by tests:

    tests/webview/integration/test_redirects_301.py

    tests/webview/integration/test_rex_redirects.py

[rex_redirects]: https://github.com/openstax/cnx-rex-redirects/blob/master/rex_redirects.py
 
