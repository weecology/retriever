"""Attempt to update datasets in all database management systems.
This module, when run, attempts to install datasets from modified Retriever
scripts in the /scripts folder (except for those listed in IGNORE), for each
engine in ENGINE_LIST() from __init__.py. In other words, it trys to install
using all possible combinations of database platform and script and checks
to see if there are any errors. It does not check the values in the database.
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
from retriever import MODULE_LIST, ENGINE_LIST, SCRIPT_LIST
from version import get_module_version

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('latin-1')
if os.name == "nt":
    os_password = "Password12!"
else:
    os_password = ""

MODULE_LIST = MODULE_LIST()
ENGINE_LIST = ENGINE_LIST()
SCRIPT_LIST = SCRIPT_LIST()
TEST_ENGINES = {}
IGNORE = [
    "forest-inventory-analysis",
    "bioclim",
    "prism-climate",
    "vertnet",
    "NPN",
    "mammal-super-tree"
]
IGNORE = [dataset.lower() for dataset in IGNORE]
UPSTREAM_VERSIONS = {}


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

    version_file.readline()
    for line in version_file.readlines():
        master_script_name, master_script_version = to_string(line).lower().strip().split(",")
        UPSTREAM_VERSIONS[master_script_name] = master_script_version

    for item in local_repo_scripts:
        local_script, local_version = item.lower().split(",")
        # check for new scripts or a change in versions for present scripts
        # repo script versions compared with upstream.
        if local_script not in UPSTREAM_VERSIONS.keys():
            modified_list.append(os.path.basename(local_script).split('.')[0])
        else:
            if LooseVersion(local_version) != UPSTREAM_VERSIONS[local_script]:
                modified_list.append(os.path.basename(local_script).split('.')[0])

    return modified_list

modified_scripts = get_modified_scripts()

if modified_scripts is None:
    print("No new scripts found. Database is up to date.")
    sys.exit()

# If engine argument, tests are only run on given engines
if len(sys.argv) > 1:
    ENGINE_LIST = [
        e for e in ENGINE_LIST
        if e.name in sys.argv[1:] or
        e.abbreviation in sys.argv[1:]
        ]

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

for engine in ENGINE_LIST:
    if engine.abbreviation in engine_test:
        try:
            opts = engine_test[engine.abbreviation]
            TEST_ENGINES[engine.abbreviation] = choose_engine(opts)
        except:
            TEST_ENGINES[engine.abbreviation] = None
            pass

errors = []

for module in MODULE_LIST:
    for (key, value) in list(TEST_ENGINES.items()):
        shortname = module.SCRIPT.shortname.lower()
        if module.__name__ in modified_scripts and shortname not in IGNORE:
            if value is not None:
                print("==>", module.__name__, value.name, "..........", module.SCRIPT.shortname)
                try:
                    module.SCRIPT.download(value)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print("ERROR.")
                    errors.append((key, module.__name__, e))
            else:
                errors.append((key, "No connection detected......" + module.SCRIPT.shortname))
os.chdir("..")
os.system("rm -r test_modified")
if errors:
    print("Engine, Dataset, Error")
    for error in errors:
        print(error)
else:
    print("All tests passed. All scripts are updated to latest version.")
