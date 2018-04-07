# Tests for cnx-automation
This repository contains tests for [cnx-automation](https://qa.cnx.org).

## How to run the tests locally

### Clone the repository

If you have cloned this project already then you can skip this, otherwise you'll
need to clone this repo using Git. If you do not know how to clone a GitHub
repository, check out this [help page][git-clone] from GitHub.

### Install dependencies

#### Create a virtualenv

    $ python3 -m venv .env

#### Activate the virtualenv

    $ source .env/bin/activate

#### Install dependencies using requirements.txt

    $ pip install -r requirements.txt

### Run the tests

Tests are run using the command line using the `tox` command. By default this
will run all of the environments configured, including checking your tests against
recommended style conventions using [flake8][flake8].

To run against a different base URL, pass in a value for `--base-url`:

```bash
$ tox -- --base-url=https://qa.cnx.org
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
`py.test --help`. The full documentation for the plugin can be found
[here][pytest-selenium].

### PageObject Pattern

This testing framework heavily relies on the pypom library. The [PyPOM][pypom]
library is the Python implementation of the [PageObject][pageobject] design pattern.

The [PageObject][pageobject] pattern creates a nice API abstraction around
an HTML page allowing the test creator to focus on the intent of a test
rather than decyphering HTML code.

The inspiration for this framework is based on the [Mozilla Addons Server Project][mozilla]
and plenty of examples can be gleamed from their fantastic usage of the
pattern.


[git-clone]: https://help.github.com/articles/cloning-a-repository/
[python]: https://www.python.org/downloads/
[flake8]: http://flake8.readthedocs.io/
[pytest-selenium]: http://pytest-selenium.readthedocs.org/
[pypom]: https://pypom.readthedocs.io/en/latest/user_guide.html#regions
[pageobject]: https://martinfowler.com/bliki/PageObject.html
[mozilla]: https://github.com/mozilla/addons-server
