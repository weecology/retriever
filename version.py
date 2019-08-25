"""Generates a configuration file containing the version number."""
from __future__ import absolute_import

import os

from retriever.lib.defaults import VERSION
from retriever.lib.scripts import get_retriever_script_versions


def write_version_file(scripts):
    if os.path.isfile("version.txt"):
        os.remove("version.txt")

    with open("version.txt", "w") as version_file:
        version_file.write(VERSION)
        for script in scripts:
            version_file.write('\n' + script)


def update_version_file():
    """Update version.txt."""
    scripts = get_retriever_script_versions()
    write_version_file(scripts)
    print("Version.txt updated.")


if __name__ == '__main__':
    update_version_file()
