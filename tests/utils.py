# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def gen_list_from_file(location):
    """Generates a list from a file

    Assumes that each item is on a single line and strips newline characters
    """
    with open(location, 'r') as f:
        uuids = [uuid.strip() for uuid in f.readlines()]
    return uuids
