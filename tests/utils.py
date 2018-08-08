# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from difflib import SequenceMatcher
from functools import wraps

from selenium.common.exceptions import StaleElementReferenceException


def gen_from_file(filepath):
    """Creates a generator from an input file

    Assumes that each item is on a single line and strips leading and trailing characters
    """
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip()


def patch_module(source_module_name, target_module_name, attr):
    """ Patches a module and attribute based on a source module and attribute of the same name
    """
    source_module = getattr(__import__(source_module_name), attr)
    target_module = __import__(target_module_name)
    setattr(target_module, attr, source_module)


# Retries StaleElementReferenceExceptions up to n-1 times (default n=3)
# Decorator with optional argument based on: https://stackoverflow.com/a/3931903
def retry_stale_element_reference_exception(method_or_max_attempts):
    def wrap(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    return method(*args, **kwargs)
                except StaleElementReferenceException:
                    if i >= max_attempts - 1:
                        raise
        return wrapper

    if callable(method_or_max_attempts):
        max_attempts = 3
        return wrap(method_or_max_attempts)
    else:
        max_attempts = method_or_max_attempts
        return wrap


def similar(a, b):
    """Returns a similarity ratio between two strings"""
    return SequenceMatcher(None, a, b).ratio()


# Like https://github.com/pytest-dev/pytest-selenium/blob/master/pytest_selenium/safety.py
# but does not make a request to the site to get redirect information
def is_url_sensitive(request, base_url, memo={}):
    """Returns whether or not the base_url is considered sensitive"""
    if base_url not in memo:
        import re
        sensitive_url_regex = re.compile(request.config.getoption('sensitive_url'))
        memo[base_url] = bool(sensitive_url_regex.search(base_url))
    return memo[base_url]


def skip_if_destructive_and_sensitive(request, base_url):
    """Skips destructive tests if the base_url is considered sensitive"""
    if 'nondestructive' not in request.node.keywords and is_url_sensitive(request, base_url):
        from pytest import skip
        skip('This test is destructive and the target URL is '
             'considered a sensitive environment. If this test is '
             "not destructive, add the 'nondestructive' marker to "
             'it. Sensitive URL: {base_url}'.format(base_url=base_url))


def shorten_tag(tag):
    """Returns the short version of a git tag when given the long (or short) version."""
    return tag.split('-')[0]
