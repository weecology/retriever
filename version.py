"""Generates a configuration file containing the version number."""
from __future__ import absolute_import
import os
from retriever.lib.defaults import VERSION
from retriever.lib.scripts import MODULE_LIST


def get_module_version():
    """This function gets the version number of the scripts and returns them in array form."""
    modules = MODULE_LIST()
    scripts = []
    for module in modules:
        if module.public:
            if os.path.isfile('.'.join(module._file.split('.')[:-1]) + '.json') and module.version:
                module_name = module._name + '.json'
                scripts.append(','.join([module_name, str(module.version)]))
            elif os.path.isfile('.'.join(module._file.split('.')[:-1]) + '.py') and \
                    not os.path.isfile('.'.join(module._file.split('.')[:-1]) + '.json'):
                module_name = module._name + '.py'
                scripts.append(','.join([module_name, str(module.version)]))

    scripts = sorted(scripts, key = str.lower)
    return scripts

scripts = get_module_version()

if os.path.isfile("version.txt"):
    os.remove("version.txt")

with open("version.txt", "w") as version_file:
    version_file.write(VERSION)
    for script in scripts:
        version_file.write('\n' + script)
