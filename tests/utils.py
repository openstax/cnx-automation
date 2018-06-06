# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
