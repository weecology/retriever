"""Generates a configuration file containing the version number."""
from __future__ import absolute_import

import os

from retriever.lib.defaults import VERSION
from retriever.lib.engine_tools import get_module_version


def write_version_file(scripts):
    """The function creates / updates version.txt with the script version numbers."""
    if os.path.isfile("version.txt"):
        os.remove("version.txt")

    with open("version.txt", "w") as version_file:
        version_file.write(VERSION)
        for script in scripts:
            version_file.write('\n' + script)


def update_version_file():
    """Update version.txt."""
    scripts = get_module_version()
    write_version_file(scripts)
    print("Version.txt updated.")


if __name__ == '__main__':
    update_version_file()
