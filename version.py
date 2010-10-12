"""Generates a configuration file containing the version number."""
import os
from dbtk import VERSION

if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "wb")
version_file.write(VERSION + '\n')
categories = ['.'.join(cat.split('.')[:-1]) for cat in os.listdir("categories")
              if cat[-4:] == ".cat"]
scripts = ['.'.join(script.split('.')[:-1]) for script in os.listdir("scripts")
           if script[-3:] == ".py"]
version_file.write(','.join(categories))
for script in scripts:
    version_file.write('\n' + script)
version_file.close()
