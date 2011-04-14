"""Generates a configuration file containing the version number."""
import os
from retriever import VERSION, MODULE_LIST

if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "wb")
version_file.write(VERSION + '\n')
modules = MODULE_LIST()
scripts = [','.join([module.__name__ + ('.script' 
                                        if os.path.isfile(module.__file__[:-4] + '.script')
                                        else '.py'), 
                     module.VERSION]) 
           for module in modules
           if module.SCRIPT.public]
for script in scripts:
    version_file.write('\n' + script)
version_file.close()
