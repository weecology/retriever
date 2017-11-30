from __future__ import print_function

from future import standard_library

from retriever.lib.tools import open_fr

standard_library.install_aliases()
import imp
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from os.path import join, isfile, getmtime, exists, abspath

from pkg_resources import parse_version

from retriever.lib.defaults import SCRIPT_SEARCH_PATHS, VERSION, SCRIPT_WRITE_PATH
from retriever.lib.compile import compile_json

global_temp_scripts = {}

def check_retriever_minimum_version(module):
    mod_ver = module.retriever_minimum_version
    m = module.name
    if not parse_version(VERSION) >= parse_version("{}".format(mod_ver)):
        print("{} is supported by Retriever version ""{}".format(m, mod_ver))
        print("Current version is {}".format(VERSION))
        return False
    return True


def MODULE_LIST(force_compile=False):
    """Load scripts from scripts directory and return list of modules."""
    if not force_compile and global_temp_scripts:
        return global_temp_scripts._getScripts()

    modules = []
    loaded_scripts = []
    if not os.path.isdir(SCRIPT_WRITE_PATH):
        os.makedirs(SCRIPT_WRITE_PATH)

    for search_path in [search_path for search_path in SCRIPT_SEARCH_PATHS if exists(search_path)]:
        to_compile = [
            file for file in os.listdir(search_path) if file[-5:] == ".json" and
            file[0] != "_"]

        datapackages_file = join(abspath(search_path), "datapackages.yml")
        if exists(datapackages_file):
            try:
                file_obj = open(datapackages_file)
            except IOError:
                print('{} file cant be read'.format(datapackages_file))
            else:
                with file_obj:
                    for line in file_obj:
                        if line.strip():
                            script_url = line.split(": ")
                            json_file_name = str(script_url[0]).replace("-","_") + ".json"
                            json_file_path = join(SCRIPT_WRITE_PATH, json_file_name)
                            urllib.request.urlretrieve(script_url[1], json_file_path)

        for script in to_compile:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_scripts:
                compiled_script = compile_json(join(search_path, script_name))
                if compiled_script:
                    if hasattr(compiled_script, "retriever_minimum_version") \
                            and not check_retriever_minimum_version(
                                compiled_script):
                        continue
                    setattr(compiled_script, "_file", os.path.join(search_path, script))
                    setattr(compiled_script, "_name", script_name)
                    modules.append(compiled_script)
                    loaded_scripts.append(script_name)

        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_" and
                 ('#retriever' in
                  ' '.join(open_fr(join(search_path, file)).readlines()[:2]).lower()
                  or '# retriever' in
                  ' '.join(open_fr(join(search_path, file)).readlines()[:2]).lower())
                 ]

        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_scripts:
                loaded_scripts.append(script_name)
                file, pathname, desc = imp.find_module(script_name, [search_path])
                try:
                    new_module = imp.load_module(script_name, file, pathname, desc)
                    if hasattr(new_module, "retriever_minimum_version"):
                        # a script with retriever_minimum_version should be loaded
                        # only if its compliant with the version of the retriever
                        if not check_retriever_minimum_version(new_module):
                            continue
                    # if the script wasn't found in an early search path
                    # make sure it works and then add it
                    new_module.SCRIPT.download
                    setattr(new_module.SCRIPT, "_file", os.path.join(search_path, script))
                    setattr(new_module.SCRIPT, "_name", script_name)
                    modules.append(new_module.SCRIPT)
                except Exception as e:
                    sys.stderr.write("Failed to load script: {} ({})\n"
                                     "Exception: {} \n"
                                     .format(script_name, search_path, str(e)))
    return modules


def SCRIPT_LIST(force_compile=False):
    return [module for module in MODULE_LIST(force_compile)]


def get_script(dataset):
    """Return the script for a named dataset."""
    scripts = {script.name: script for script in SCRIPT_LIST()}
    if dataset in scripts:
        return scripts[dataset]
    else:
        raise KeyError("No dataset named: {}".format(dataset))

class Singleton_scripts:
    def __init__(self):
        self._shared_scripts = SCRIPT_LIST()

    def _getScripts(self):
        return self._shared_scripts

global_temp_scripts = Singleton_scripts()