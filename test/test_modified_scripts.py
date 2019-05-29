"""This module, when run, attempts to install datasets for modified Retriever
scripts in the /scripts folder (except for those listed in ignore_list)
"""
from __future__ import absolute_import
from __future__ import print_function

from future import standard_library

standard_library.install_aliases()
import os
import sys
import subprocess
import requests
from distutils.version import LooseVersion
from retriever.engines import choose_engine, engine_list
from retriever.lib.defaults import ENCODING
from retriever.lib.scripts import SCRIPT_LIST
from retriever.lib.engine_tools import get_script_version


file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))
working_script_dir = os.path.abspath(os.path.join(retriever_root_dir, "scripts"))
home_dir = os.path.expanduser('~')
script_home = "{}/.retriever/scripts".format(home_dir)


def setup_module():
    """Make sure that you are in the source main directory

    This ensures that scripts obtained are from the script directory
    and not the .retriever's script directory
    """
    os.chdir(retriever_root_dir)


def get_modified_scripts():
    """Get modified script list, using version.txt in repo and master upstream"""

    os.chdir(retriever_root_dir)
    modified_list = []
    version_file = requests.get("https://raw.githubusercontent.com/weecology/retriever/master/version.txt")
    local_repo_scripts = get_script_version()  # local repo versions

    upstream_versions = {}
    version_file = version_file.text.splitlines()[1:]
    for line in version_file:
        master_script_name, master_script_version = line.lower().strip().split(",")
        upstream_versions[master_script_name] = master_script_version

    for item in local_repo_scripts:
        local_script, local_version = item.lower().split(",")
        # check for new scripts or a change in versions for present scripts
        # repo script versions compared with upstream.
        if local_script not in upstream_versions.keys():
            modified_list.append(os.path.basename(local_script).split('.')[0])
        else:
            if LooseVersion(local_version) != upstream_versions[local_script]:
                modified_list.append(os.path.basename(local_script).split('.')[0])

    return modified_list


def install_modified():
    """Installs modified scripts and returns any errors found"""

    os_password = ""
    if os.name == "nt":
        os_password = "Password12!"

    ignore = [
        "forest-inventory-analysis",
        "bioclim",
        "prism-climate",
        "vertnet",
        "NPN",
        "mammal-super-tree"
    ]
    ignore_list = [dataset.lower() for dataset in ignore]

    modified_scripts = get_modified_scripts()
    if modified_scripts is None:
        print("No new scripts found. Database is up to date.")
        sys.exit()

    engine_list_install = engine_list
    if os.path.exists("test_modified"):
        subprocess.call(['rm', '-r', 'test_modified'])
    os.makedirs("test_modified")
    os.chdir("test_modified")
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb_retriever.sqlite'))
    engine_test = {
        "postgres": {'engine': 'postgres',
                     'user': 'postgres',
                     'password': os_password,
                     'host': 'localhost',
                     'port': 5432,
                     'database': 'postgres',
                     'database_name': 'testschema',
                     'table_name': '{db}.{table}'},

        "mysql": {'engine': 'mysql',
                  'user': 'travis',
                  'password': '',
                  'host': 'localhost',
                  'port': 3306,
                  'database_name': 'testdb_retriever',
                  'table_name': '{db}.{table}'},

        "xml": {'engine': 'xml',
                'table_name': 'output_file_{table}.xml'},

        "json": {'engine': 'json',
                 'table_name': 'output_file_{table}.json'},

        "csv": {'engine': 'csv',
                'table_name': 'output_file_{table}.csv'},

        "sqlite": {'engine': 'sqlite',
                   'file': dbfile, 'table_name': '{db}_{table}'}
    }

    test_engines = {}
    for engine in engine_list_install:
        if engine.abbreviation in engine_test:
            try:
                opts = engine_test[engine.abbreviation]
                test_engines[engine.abbreviation] = choose_engine(opts)
            except BaseException:
                test_engines[engine.abbreviation] = None
                pass

    module_list = SCRIPT_LIST()
    errors = []
    for module in module_list:
        for (key, value) in list(test_engines.items()):
            shortname = module.name.lower()
            if module._name in modified_scripts and shortname not in ignore_list:
                if value is not None:
                    print("==>", module._name, value.name, "..........", module.name)
                    try:
                        module.download(value)
                        module.engine.final_cleanup()
                    except KeyboardInterrupt:
                        pass
                    except Exception as e:
                        print("ERROR.")
                        errors.append((key, module._name, e))
                else:
                    errors.append((key, "No connection detected......" + module.name))
    os.chdir("..")
    subprocess.call(['rm', '-r', 'test_modified'])
    return errors


# def test_install_modified():
#     assert install_modified() == []


def main():
    setup_module()
    errors = install_modified()
    if errors:
        print("Engine, Dataset, Error")
        for error in errors:
            print(error)
    else:
        print("All tests passed. All scripts are updated to latest version.")


if __name__ == "__main__":
    main()
