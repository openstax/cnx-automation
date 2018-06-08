# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from functools import wraps

from selenium.common.exceptions import StaleElementReferenceException


# Retries StaleElementReferenceExceptions up to n-1 times (default n=3)
# Decorator with optional argument based on: https://stackoverflow.com/a/3931903
def retry_stale_element_reference_exception(method_or_max_tries):
    def wrap(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            for i in range(max_tries):
                try:
                    return method(*args, **kwargs)
                except StaleElementReferenceException:
                    if i >= max_tries - 1:
                        raise
        return wrapper

    if callable(method_or_max_tries):
        max_tries = 3
        return wrap(method_or_max_tries)
    else:
        max_tries = method_or_max_tries
        return wrap
