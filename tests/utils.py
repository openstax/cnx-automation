# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def gen_list_from_file(filepath):
    """Generates a list from a file

    Assumes that each item is on a single line and strips leading and trailing characters
    """
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            yield line
