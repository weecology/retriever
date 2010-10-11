"""Generates a configuration file containing the version number."""
import os
from dbtk import VERSION

if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "wb")
version_file.write(VERSION)
version_file.close()
