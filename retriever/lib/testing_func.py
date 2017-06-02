from os.path import join, isfile, getmtime, exists
from pkg_resources import parse_version
import imp
import os
import platform
import sys

from retriever.lib.compile import compile_json
from retriever._version import __version__

current_platform = platform.system().lower()
if current_platform != 'windows':
    import pwd

VERSION = __version__
COPYRIGHT = "Copyright (C) 2011-2016 Weecology University of Florida"
REPO_URL = "https://raw.github.com/weecology/retriever/"
MASTER_BRANCH = REPO_URL + "master/"
REPOSITORY = MASTER_BRANCH
ENCODING = 'ISO-8859-1'

HOME_DIR = os.path.expanduser('~/.retriever/')
for dir in (HOME_DIR, os.path.join(HOME_DIR, 'raw_data'), os.path.join(HOME_DIR, 'scripts')):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            if (current_platform != 'windows') and os.getenv("SUDO_USER"):
                # owner of .retriever should be user even when installing
                # w/sudo
                pw = pwd.getpwnam(os.getenv("SUDO_USER"))
                os.chown(dir, pw.pw_uid, pw.pw_gid)
        except OSError:
            print("The Retriever lacks permission to access the ~/.retriever/ directory.")
            raise
SCRIPT_SEARCH_PATHS = [
    "./",
    'scripts',
    os.path.join(HOME_DIR, 'scripts/')
]
SCRIPT_WRITE_PATH = SCRIPT_SEARCH_PATHS[-1]
DATA_SEARCH_PATHS = [
    "./",
    "{dataset}",
    "raw_data/{dataset}",
    os.path.join(HOME_DIR, 'raw_data/{dataset}'),
]
DATA_WRITE_PATH = DATA_SEARCH_PATHS[-1]

# Create default data directory
DATA_DIR = '.'


def MODULE_LIST(force_compile=False):
    """Load scripts from scripts directory and return list of modules."""
    modules = []
    loaded_scripts = []

    for search_path in [search_path for search_path in SCRIPT_SEARCH_PATHS if exists(search_path)]:
        to_compile = [
            file for file in os.listdir(search_path) if file[-5:] == ".json" and
            file[0] != "_" and (
                (not isfile(join(search_path, file[:-5] + '.py'))) or (
                    isfile(join(search_path, file[:-5] + '.py')) and (
                        getmtime(join(search_path, file[:-5] + '.py')) < getmtime(
                            join(search_path, file)))) or force_compile)]
        for script in to_compile:
            script_name = '.'.join(script.split('.')[:-1])
            compile_json(join(search_path, script_name))

        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_" and
                 '#retriever' in ' '.join(open(join(search_path, file), 'r').readlines()[:2]).lower()]

        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_scripts:
                loaded_scripts.append(script_name)
                file, pathname, desc = imp.find_module(script_name, [search_path])
                try:
                    new_module = imp.load_module(script_name, file, pathname, desc)
                    if hasattr(new_module.SCRIPT, "retriever_minimum_version"):
                        # a script with retriever_minimum_version should be loaded
                        # only if its compliant with the version of the retriever
                        if not parse_version(VERSION) >= parse_version("{}".format(
                                new_module.SCRIPT.retriever_minimum_version)):
                            print("{} is supported by Retriever version {}".format(script_name,
                                                                                   new_module.SCRIPT.retriever_minimum_version))
                            print("Current version is {}".format(VERSION))
                            continue
                    # if the script wasn't found in an early search path
                    # make sure it works and then add it
                    new_module.SCRIPT.download
                    modules.append(new_module)
                except Exception as e:
                    sys.stderr.write("Failed to load script: %s (%s)\nException: %s \n" % (
                        script_name, search_path, str(e)))
    return modules


def SCRIPT_LIST(force_compile=False):
    return [module.SCRIPT for module in MODULE_LIST(force_compile)]
