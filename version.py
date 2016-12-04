"""Generates a configuration file containing the version number."""
from __future__ import absolute_import
import os
from retriever import VERSION, MODULE_LIST


if os.path.isfile("version.txt"):
    os.remove("version.txt")
version_file = open("version.txt", "w")
version_file.write(VERSION)
modules = MODULE_LIST()
scripts = []
for module in modules:
    if module.SCRIPT.public:
        if os.path.isfile('.'.join(module.__file__.split('.')[:-1]) + '.json') and module.SCRIPT.version:
            module_name = module.__name__ + '.json'
            scripts.append(','.join([module_name, str(module.SCRIPT.version)]))
        elif os.path.isfile('.'.join(module.__file__.split('.')[:-1]) + '.py') and \
                not os.path.isfile('.'.join(module.__file__.split('.')[:-1]) + '.json'):
            module_name = module.__name__ + '.py'
            scripts.append(','.join([module_name, str(module.SCRIPT.version)]))

scripts = sorted(scripts, key = str.casefold)

for script in scripts:
    version_file.write('\n' + script)
version_file.close()
