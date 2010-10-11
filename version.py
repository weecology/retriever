"""Generates a configuration file containing the version number."""
import os
from dbtk import VERSION, CATEGORIES

if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "wb")
version_file.write(VERSION + '\n')
version_file.write(','.join(CATEGORIES))
version_file.close()
