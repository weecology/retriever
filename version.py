"""Generates a configuration file containing the version number."""
import os
from retriever import VERSION, MODULE_LIST

if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "wb")
version_file.write(VERSION + '\n')
categories = ['.'.join(cat.split('.')[:-1]) for cat in os.listdir("categories")
              if cat[-4:] == ".cat"]
modules = MODULE_LIST()
scripts = [','.join([module.__name__ + ('.script' if '.script' in module.__file__ else '.py'), 
                     module.VERSION]) 
           for module in modules
           if module.SCRIPT.public]
version_file.write(','.join(categories))
for script in scripts:
    version_file.write('\n' + script)
version_file.close()
