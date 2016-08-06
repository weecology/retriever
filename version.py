"""Generates a configuration file containing the version number."""
from __future__ import absolute_import
import os
from retriever import VERSION, MODULE_LIST, MASTER
from hashlib import md5
from inspect import getsourcelines

if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "w")
version_file.write(VERSION)
modules = MODULE_LIST()
scripts = []
for module in modules:
    if module.SCRIPT.public:
        m = md5()
        m.update(''.join(getsourcelines(module)[0]))

        module_name = module.__name__ + ('.json'
                                         if os.path.isfile('.'.join(module.__file__.split('.')[:-1]) + '.json')
                                         else '.py')
        if MASTER:
            scripts.append(module_name)
        else:

            scripts.append(','.join([module_name, m.hexdigest()]))

for script in scripts:
    version_file.write('\n' + script)
version_file.close()
