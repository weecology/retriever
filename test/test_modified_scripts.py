"""This module, when run, attempts to install datasets for modified Retriever
scripts in the /scripts folder (except for those listed in ignore_list)
"""
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from distutils.version import LooseVersion
from imp import reload
from retriever.lib.tools import choose_engine
from retriever import MODULE_LIST, ENGINE_LIST, ENCODING
from retriever.lib.tools import get_module_version

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding(ENCODING)

def to_string(value_to_str):
    if sys.version_info >= (3, 0, 0):
        return value_to_str.decode("UTF-8")
    else:
        return value_to_str

def get_modified_scripts():
    """Get modified script list, using version.txt in repo and master upstream"""
    modified_list = []
    version_file = urllib.request.urlopen("https://raw.githubusercontent.com/weecology/retriever/master/version.txt")
    local_repo_scripts = get_module_version()  # local repo versions

    upstream_versions = {}
    version_file.readline()
    for line in version_file.readlines():
        master_script_name, master_script_version = to_string(line).lower().strip().split(",")
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


def install_modified(engine_list=ENGINE_LIST()):
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

    if os.path.exists("test_modified"):
        os.system("rm -r test_modified")
    os.makedirs("test_modified")
    os.chdir("test_modified")
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
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
                  'database_name': 'testdb',
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
    for engine in engine_list:
        if engine.abbreviation in engine_test:
            try:
                opts = engine_test[engine.abbreviation]
                test_engines[engine.abbreviation] = choose_engine(opts)
            except:
                test_engines[engine.abbreviation] = None
                pass

    module_list = MODULE_LIST()
    errors = []
    for module in module_list:
        for (key, value) in list(test_engines.items()):
            shortname = module.SCRIPT.name.lower()
            if module.__name__ in modified_scripts and shortname not in ignore_list:
                if value is not None:
                    print("==>", module.__name__, value.name, "..........", module.SCRIPT.name)
                    try:
                        module.SCRIPT.download(value)
                        module.SCRIPT.engine.final_cleanup()
                    except KeyboardInterrupt:
                        pass
                    except Exception as e:
                        print("ERROR.")
                        errors.append((key, module.__name__, e))
                else:
                    errors.append((key, "No connection detected......" + module.SCRIPT.name))
    os.chdir("..")
    os.system("rm -r test_modified")
    return errors


def test_install_modified():
    assert install_modified() == []


def main():
    engine_list = ENGINE_LIST()
    # If engine argument, tests are only run on given engines
    if len(sys.argv) > 1:
        engine_list = [
            e for e in engine_list
            if e.name in sys.argv[1:] or
            e.abbreviation in sys.argv[1:]
            ]

    errors = install_modified(engine_list)
    if errors:
        print("Engine, Dataset, Error")
        for error in errors:
            print(error)
    else:
        print("All tests passed. All scripts are updated to latest version.")


if __name__ == "__main__":
    main()
