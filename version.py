"""Generates a configuration file containing the version number."""
import os
from retriever import VERSION, MODULE_LIST
from hashlib import md5
from inspect import getsourcelines

if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "wb")
version_file.write(VERSION)
modules = MODULE_LIST()
scripts = []
for module in modules:
    if module.SCRIPT.public:
        m = md5()
        m.update(''.join(getsourcelines(module)[0]))
        scripts.append(','.join([module.__name__ + ('.script' 
                                                    if os.path.isfile('.'.join(module.__file__.split('.')[:-1]) + '.script')
                                                    else '.py'), 
                                 m.hexdigest()]))

for script in scripts:
    version_file.write('\n' + script)
version_file.close()
