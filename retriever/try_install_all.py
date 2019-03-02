"""Attempt to install all datasets into all database management systems

This module, when run, attempts to install datasets from all Retriever scripts
in the /scripts folder (except for those listed in IGNORE), for each engine in
engine_list in retriever.engines. In other words, it runs trys to install using
all possible combinations of database platform and script and checks to
see if there are any errors. It does not check the values in the database.

"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from imp import reload

from retriever.engines import engine_list, choose_engine
from retriever.lib.scripts import SCRIPT_LIST

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('latin-1')
if os.name == "nt":
    os_password = "Password12!"
else:
    os_password = ""

MODULE_LIST = SCRIPT_LIST()
if len(sys.argv) > 1:
    engine_list = [
        e for e in engine_list
        if e.name in sys.argv[1:] or
        e.abbreviation in sys.argv[1:]
        ]

if os.path.exists("test_all"):
    os.system("rm -r test_all")
os.makedirs("test_all")
os.chdir("test_all")

dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb_retriever.sqlite'))

engine_test = {
    "postgres": {
        'engine': 'postgres',
        'user': 'postgres',
        'password': os_password,
        'host': 'localhost',
        'port': 5432,
        'database': 'postgres',
        'database_name': 'testschema',
        'table_name': '{db}.{table}'
    },
    "mysql": {
        'engine': 'mysql',
        'user': 'travis',
        'password': '',
        'host': 'localhost',
        'port': 3306,
        'database_name': 'testdb_retriever',
        'table_name': '{db}.{table}'
    },
    "xml": {'engine': 'xml', 'table_name': 'output_file_{table}.xml'},
    "json": {'engine': 'json', 'table_name': 'output_file_{table}.json'},
    "csv": {'engine': 'csv', 'table_name': 'output_file_{table}.csv'},
    "sqlite": {'engine': 'sqlite', 'file': dbfile, 'table_name': '{db}_{table}'}
}

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

for engine in engine_list:
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
        if module.SCRIPT.name.lower() not in IGNORE:
            if value != None:
                print("==>", module.__name__, value.name, "..........", module.SCRIPT.name)
                try:
                    module.SCRIPT.download(value)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print("ERROR.")
                    errors.append((key, module.__name__, e))
            else:
                errors.append((key, "No connection detected......" + module.SCRIPT.name))
print('')
if errors:
    print("Engine, Dataset, Error")
    for error in errors:
        print(error)
else:
    print("All tests passed")
