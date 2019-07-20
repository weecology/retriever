from __future__ import print_function

from future import standard_library

standard_library.install_aliases()
import csv
import imp
import io
import os
import re
import sys
import json
import requests
from os.path import join, exists
from collections import OrderedDict

from pkg_resources import parse_version
from distutils.version import LooseVersion

from retriever.lib.defaults import REPOSITORY, RETRIEVER_REPOSITORY, SCRIPT_SEARCH_PATHS, VERSION, ENCODING, SCRIPT_WRITE_PATH, RETRIEVER_SCRIPTS, RETRIEVER_DATASETS
from retriever.lib.load_json import read_json
from retriever.lib.repository import check_for_updates

global_script_list = None


def check_retriever_minimum_version(module):
    """Return true if a script's version number is greater
    than the retriever's version."""
    mod_ver = module.retriever_minimum_version
    m = module.name

    if hasattr(module, "retriever_minimum_version"):
        if not parse_version(VERSION) >= parse_version("{}".format(mod_ver)):
            print("{} is supported by Retriever version ""{}".format(m, mod_ver))
            print("Current version is {}".format(VERSION))
            return False
    return True


def reload_scripts():
    """Load scripts from scripts directory and return list of modules."""
    modules = []
    loaded_files = []
    loaded_scripts = []
    if not os.path.isdir(SCRIPT_WRITE_PATH):
        os.makedirs(SCRIPT_WRITE_PATH)

    for search_path in [search_path for search_path in SCRIPT_SEARCH_PATHS if exists(search_path)]:
        data_packages = [file_i for file_i in os.listdir(search_path) if file_i.endswith(".json")]

        for script in data_packages:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_files:
                read_script = read_json(join(search_path, script_name))
                if read_script and read_script.name.lower() not in loaded_scripts:
                    if not check_retriever_minimum_version(read_script):
                        continue
                    setattr(read_script, "_file", os.path.join(search_path, script))
                    setattr(read_script, "_name", script_name)
                    modules.append(read_script)
                    loaded_files.append(script_name)
                    loaded_scripts.append(read_script.name.lower())

        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_" and
                 ('#retriever' in
                  ' '.join(open_fr(join(search_path, file), encoding=ENCODING).readlines()[:2]).lower())
                 ]

        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_files:
                loaded_files.append(script_name)
                file, pathname, desc = imp.find_module(script_name, [search_path])
                try:
                    new_module = imp.load_module(script_name, file, pathname, desc)
                    if hasattr(new_module.SCRIPT, "retriever_minimum_version"):
                        # a script with retriever_minimum_version should be loaded
                        # only if its compliant with the version of the retriever
                        if not check_retriever_minimum_version(new_module.SCRIPT):
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
    if global_script_list:
        global_script_list.set_scripts(modules)
    return modules


def SCRIPT_LIST():
    """Return Loaded scripts.

    Ensure that only one instance of SCRIPTS is created."""
    if global_script_list:
        return global_script_list.get_scripts()
    return reload_scripts()


def get_script(dataset):
    """Return the script for a named dataset."""
    scripts = {script.name: script for script in SCRIPT_LIST()}
    if dataset in scripts:
        script = scripts[dataset]
        local_version = script.version
        if dataset in RETRIEVER_DATASETS:
            upstream_version = get_script_version_upstream(dataset, repo=RETRIEVER_REPOSITORY)
        else:
            upstream_version = get_script_version_upstream(dataset)
        if upstream_version is None or LooseVersion(local_version) >= LooseVersion(upstream_version):
            return script
        prompt = "A newer version of {dataset} is available. Would you like to download it? (y/N): ".format(dataset=dataset)
        should_download = input(prompt)
        while not (should_download.lower() in ['y', 'n', '']):
            print("Please enter either y or n.")
            should_download = input()
        if should_download.lower() == 'y':
            if dataset in RETRIEVER_DATASETS:
                read_script = get_script_upstream(dataset, repo=RETRIEVER_REPOSITORY)
            else:
                read_script = get_script_upstream(dataset)
            if read_script is None:
                print("Unable to download {dataset}.".format(dataset=dataset))
                return script
            else:
                return read_script
        else:
            return script
    else:
        if dataset in RETRIEVER_DATASETS:
            read_script = get_script_upstream(dataset, repo=RETRIEVER_REPOSITORY)
        else:
            read_script = get_script_upstream(dataset)
        if read_script is None:
            raise KeyError("No dataset named: {}".format(dataset))
        else:
            return read_script


def get_script_upstream(dataset, repo=REPOSITORY):
    """Return the upstream script for a named dataset."""
    try:
        is_json = True
        script = dataset.replace('-', '_')
        script_name = script + ".json"
        filepath = "scripts/" + script_name
        newpath = os.path.normpath(os.path.join(SCRIPT_WRITE_PATH, script_name))
        r = requests.get(repo + filepath, allow_redirects=True, stream=True)
        if r.status_code == 404:
            is_json = False
            script_name = script + ".py"
            filepath = "scripts/" + script_name
            newpath = os.path.normpath(os.path.join(SCRIPT_WRITE_PATH, script_name))
            r = requests.get(repo + filepath, allow_redirects=True, stream=True)
            if r.status_code == 404:
                return None
        with open(newpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        r.close()
        if is_json:
            read_script = read_json(join(SCRIPT_WRITE_PATH, script))
            setattr(read_script, "_file", os.path.join(SCRIPT_WRITE_PATH, script_name))
            setattr(read_script, "_name", script)
            return read_script
        else:
            file, pathname, desc = imp.find_module(script, [SCRIPT_WRITE_PATH])
            new_module = imp.load_module(script, file, pathname, desc)
            setattr(new_module.SCRIPT, "_file", os.path.join(SCRIPT_WRITE_PATH, script_name))
            setattr(new_module.SCRIPT, "_name", script)
            return new_module.SCRIPT
    except requests.exceptions.ConnectionError:
        return None


def get_script_version_upstream(dataset, repo=REPOSITORY):
    """Return the upstream script version for a named dataset."""
    try:
        script = dataset.replace('-', '_') + ".json"
        filepath = "scripts/" + script
        r = requests.get(repo + filepath, allow_redirects=True, stream=True)
        if r.status_code == 404:
            script = dataset.replace('-', '_') + ".py"
            filepath = "scripts/" + script
            r = requests.get(repo + filepath, allow_redirects=True, stream=True)
            if r.status_code == 404:
                return None

        pattern = re.compile(r'[."]version[\'"\s":=]+(\d+\.\d+.\d+)')
        version = re.search(pattern, r.text).group(1)
        return version
    except requests.exceptions.ConnectionError:
        return None


def get_dataset_names_upstream(keywords=None, licenses=None, repo=REPOSITORY):
    """Search all datasets upstream by keywords and licenses."""
    try:
        if not keywords and not licenses:
            version_file = requests.get(repo + "version.txt").text
            version_file = version_file.splitlines()[1:]

            scripts = []
            max_scripts = 100
            for line in version_file:
                script = line.strip('\n').split(',')[0]
                script = '.'.join(script.split('.')[:-1])
                script = script.replace('_', '-')
                scripts.append(script)
                if len(scripts) == max_scripts:
                    break
            return sorted(scripts)

        result_scripts = set()
        if repo == RETRIEVER_REPOSITORY:
            search_url = "https://api.github.com/search/code?q={query}+in:file+path:scripts+repo:weecology/retriever"
        else:
            search_url = "https://api.github.com/search/code?q={query}+in:file+path:scripts+repo:weecology/retriever-recipes"
        if licenses:
            licenses = [l.lower() for l in licenses]
            for l in licenses:
                try:
                    r = requests.get(search_url.format(query=l))
                    r = r.json()
                    for index in range(r['total_count']):
                        script = r['items'][index]['name']
                        script = '.'.join(script.split('.')[:-1])
                        script = script.replace('_', '-')
                        result_scripts.add(script)
                except:
                    raise
        if keywords:
            keywords = [k.lower() for k in keywords]
            for k in keywords:
                try:
                    r = requests.get(search_url.format(query=k))
                    r = r.json()
                    for index in range(r['total_count']):
                        script = r['items'][index]['name']
                        script = '.'.join(script.split('.')[:-1])
                        script = script.replace('_', '-')
                        result_scripts.add(script)
                except:
                    raise
        return sorted(result_scripts)
    except requests.exceptions.ConnectionError:
        return []


def open_fr(file_name, encoding=ENCODING, encode=True):
    """Open file for reading respecting Python version and OS differences.

    Sets newline to Linux line endings on Windows and Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if os.name == 'nt':
            file_obj = io.open(file_name, 'r', newline='', encoding=encoding)
        else:
            if encode:
                file_obj = io.open(file_name, "r", encoding=encoding)
            else:
                file_obj = io.open(file_name, "r")
    else:
        file_obj = io.open(file_name, "r", encoding=encoding)
    return file_obj


def open_fw(file_name, encoding=ENCODING, encode=True):
    """Open file for writing respecting Python version and OS differences.

    Sets newline to Linux line endings on Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if encode:
            file_obj = io.open(file_name, 'w', newline='', encoding=encoding)
        else:
            file_obj = io.open(file_name, 'w', newline='')
    else:
        file_obj = io.open(file_name, 'wb')
    return file_obj


def open_csvw(csv_file, encode=True):
    """Open a csv writer forcing the use of Linux line endings on Windows.

    Also sets dialect to 'excel' and escape characters to '\\'
    """
    if os.name == 'nt':
        csv_writer = csv.writer(csv_file, dialect='excel',
                                escapechar='\\', lineterminator='\n')
    else:
        csv_writer = csv.writer(csv_file, dialect='excel', escapechar='\\')
    return csv_writer


def to_str(object, object_encoding=sys.stdout, object_decoder=ENCODING):
    enc = object_encoding.encoding
    return str(object).encode(enc, errors='backslashreplace').decode(object_decoder)


def read_json_version(json_file):
    json_object = OrderedDict()
    json_file_encoding = None

    try:
        file_obj = open_fr(json_file)
        json_object = json.load(file_obj)
        if "encoding" in json_object:
            json_file_encoding = json_object['encoding']
        file_obj.close()
    except ValueError:
        pass

    try:
        if json_file_encoding:
            file_obj = open_fr(json_file, encoding=json_file_encoding)
        else:
            file_obj = open_fr(json_file)
        json_object = json.load(file_obj)
        file_obj.close()
    except ValueError:
        pass

    return json_object.get("version", None)


def read_py_version(script_name, search_path):
    file, pathname, desc = imp.find_module(script_name, [search_path])
    try:
        new_module = imp.load_module(script_name, file, pathname, desc)
        if hasattr(new_module.SCRIPT, "version"):
            return new_module.SCRIPT.version
    except:
        pass
    return None


def get_retriever_script_versions():
    search_path = "scripts"
    scripts = []
    if exists(search_path):
        for script in RETRIEVER_SCRIPTS:
            if script.endswith(".json"):
                script_version = read_json_version(join(search_path, script))
                scripts.append(','.join([script, str(script_version)]))
            elif script.endswith(".py"):
                script_name = '.'.join(script.split('.')[:-1])
                script_version = read_py_version(script_name, search_path)
                scripts.append(','.join([script, str(script_version)]))
    scripts = sorted(scripts, key=str.lower)
    return scripts


class StoredScripts:
    def __init__(self):
        self._shared_scripts = SCRIPT_LIST()

    def get_scripts(self):
        return self._shared_scripts

    def set_scripts(self, script_list):
        self._shared_scripts = script_list


global_script_list = StoredScripts()
