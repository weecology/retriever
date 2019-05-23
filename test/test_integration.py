# -*- coding: latin-1  -*-
# """Integrations tests for Data Retriever"""
from __future__ import print_function

import json
import os
import sys
import shlex
import shutil
import subprocess

from retriever.lib.defaults import ENCODING, DATA_DIR

import pytest
from retriever.lib.load_json import read_json
from retriever.lib.defaults import HOME_DIR
from retriever.engines import engine_list
from retriever.lib.engine_tools import file_2list
from retriever.lib.engine_tools import create_file
from retriever.lib.engine_tools import to_str

encoding = ENCODING.lower()
# Set postgres password, Appveyor service needs the password given
# The Travis service obtains the password from the config file.
os_password = ""
pgdb_host = "localhost"
mysqldb_host = "localhost"
testdb_retriever = "testdb_retriever"
testschema = "testschema_retriever"

if os.name == "nt":
    os_password = "Password12!"

docker_or_travis = os.environ.get("IN_DOCKER")
if docker_or_travis == "true":
    os_password = 'Password12!'
    pgdb_host = "pgdb_retriever"
    mysqldb_host = "mysqldb_retriever"

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, \
csv_engine, download_engine, json_engine, xml_engine = engine_list

simple_csv = {
    'name': 'simple_csv',
    'raw_data': ['a,b,c',
                 '1,2,3',
                 '4,5,6'],
    'script': {"name": "simple_csv",
               "resources": [
                   {"dialect": {"do_not_bulk_insert": "True"},
                    "name": "simple_csv",
                    "schema": {},
                    "url": "http://example.com/simple_csv.csv"}
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {"simple_csv": "http://example.com/simple_csv.csv"}
               },
    'expect_out': ['a,b,c', '1,2,3', '4,5,6']
}

comma_delimiter = {
    'name': 'comma_delimiter',
    'raw_data': ['a,b,c',
                 '1,2,3',
                 '4,5,6'],
    'script': {"name": "comma_delimiter",
               "resources": [
                   {"dialect": {"delimiter": ",", "do_not_bulk_insert": "True"},
                   "name": "comma_delimiter",
                   "schema": {},
                   "url": "http://example.com/comma_delimiter.csv"}
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {"comma_delimiter": "http://example.com/comma_delimiter.csv"}
               },
    'expect_out': ['a,b,c', '1,2,3', '4,5,6']
}

tab_delimiter = {
    'name': 'tab_delimiter',
    'raw_data': ['a	b	c',
                 '1	2	3',
                 '4	5	6'],
    'script': {"name": "tab_delimiter",
               "resources": [
                   {"dialect": {"delimiter": "\t", "do_not_bulk_insert": "True" },
                   "name": "tab_delimiter",
                   "schema": {},
                   "url": "http://example.com/tab_delimiter.csv"}
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {"tab_delimiter": "http://example.com/tab_delimiter.csv"}
               },
    'expect_out': ['a,b,c', '1,2,3', '4,5,6']
}

data_no_header = {
    'name': 'data_no_header',
    'raw_data': ['1,2,3',
                 '4,5,6'],
    'script': {"name": "data_no_header",
               "resources": [
                   {"dialect":
                        {"do_not_bulk_insert": "True", "header_rows": 0},
                    "name": "data_no_header",
                    "schema": {
                        "fields": [
                            {
                                "name": "a",
                                "type": "char"
                            },
                            {
                                "name": "b",
                                "size": "20",
                                "type": "char"
                            },
                            {
                                "name": "c",
                                "size": "20",
                                "type": "char"
                            }
                        ]
                    },
                    "url": "http://example.com/data_no_header.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {"data_no_header": "http://example.com/data_no_header.csv"}
               },
    'expect_out': ['a,b,c', '1,2,3', '4,5,6']
}

csv_latin1_encoding = {
    'name': 'csv_latin1_encoding',
    'raw_data': ['a,b,c',
                 u'1,2,4Löve',
                 '4,5,6'],
    'script': {"name": "csv_latin1_encoding",
               "resources": [
                   {"dialect": {"delimiter": ",","do_not_bulk_insert": "True"},
                    "name": "csv_latin1_encoding",
                    "schema": {},
                    "url": "http://example.com/csv_latin1_encoding.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {"csv_latin1_encoding":
                        "http://example.com/csv_latin1_encoding.csv"
                    }
               },
    'expect_out': [u'a,b,c', to_str('1,2,4Löve', object_decoder="latin-1"), u'4,5,6']
}


autopk_csv = {
    'name': 'autopk_csv',
    'raw_data': ['a,b,c',
                 '1,2,3',
                 '4,5,6'],
    'script': {"name": "autopk_csv",
               "resources": [
                   {"dialect": {"do_not_bulk_insert": "True"},
                    "name": "autopk_csv",
                    "schema": {
                        "fields": [
                            {
                                "name": "record_id",
                                "type": "pk-auto"
                            },
                            {
                                "name": "a",
                                "type": "int"
                            },
                            {
                                "name": "b",
                                "type": "int"
                            },
                            {
                                "name": "c",
                                "type": "int"
                            }
                        ]
                    },
                    "url": "http://example.com/autopk_csv.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls": {"autopk_csv": "http://example.com/autopk_csv.csv"}
               },
    'expect_out': ['record_id,a,b,c', '1,1,2,3', '2,4,5,6']
}

crosstab = {
    'name': 'crosstab',
    'raw_data': ['a,b,c1,c2',
                 '1,1,1.1,1.2',
                 '1,2,2.1,2.2'],
    'script': {"name": "crosstab",
               "resources": [
                   {"dialect": {"do_not_bulk_insert": "True"},
                    "name": "crosstab",
                    "schema": {
                        "ct_column": "c",
                        "ct_names": ["c1", "c2"],
                        "fields": [
                            {
                                "name": "a",
                                "type": "int"
                            },
                            {
                                "name": "b",
                                "type": "int"
                            },
                            {
                                "name": "val",
                                "type": "ct-double"
                            }
                        ]
                    },
                    "url": "http://example.com/crosstab.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls": {"crosstab": "http://example.com/crosstab.csv"}
               },
    'expect_out': ['a,b,c,val',
                   '1,1,c1,1.1',
                   '1,1,c2,1.2',
                   '1,2,c1,2.1',
                   '1,2,c2,2.2']
}

autopk_crosstab = {
    'name': 'autopk_crosstab',
    'raw_data': ['a,b,c1,c2',
                 '1,1,1.1,1.2',
                 '1,2,2.1,2.2'],
    'script': {"name": "autopk_crosstab",
               "resources": [
                   {"dialect": {"do_not_bulk_insert": "True"},
                    "name": "autopk_crosstab",
                    "schema": {
                        "ct_column": "c",
                        "ct_names": ["c1", "c2"],
                        "fields": [
                            {
                                "name": "record_id",
                                "type": "pk-auto"
                            },
                            {
                                "name": "a",
                                "type": "int"
                            },
                            {
                                "name": "b",
                                "type": "int"
                            },
                            {
                                "name": "val",
                                "type": "ct-double"
                            }
                        ]
                    },
                    "url": "http://example.com/autopk_crosstab.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {"autopk_crosstab": "http://example.com/autopk_crosstab.csv"}
               },
    'expect_out': ['record_id,a,b,c,val',
                   '1,1,1,c1,1.1',
                   '2,1,1,c2,1.2',
                   '3,1,2,c1,2.1',
                   '4,1,2,c2,2.2']
}

skip_csv = {
    'name': 'skip_csv',
    'raw_data': ['a,b,c',
                 '1,2,3',
                 '4,5,6'],
    'script': {"name": "skip_csv",
               "resources": [
                   {"dialect": {"do_not_bulk_insert": "True"},
                    "name": "skip_csv",
                    "schema": {
                        "fields": [
                            {
                                "name": "a",
                                "type": "skip"
                            },
                            {
                                "name": "b",
                                "type": "int"
                            },
                            {
                                "name": "c",
                                "type": "int"
                            }
                        ]
                    },
                    "url": "http://example.com/skip_csv.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls": {"skip_csv": "http://example.com/skip_csv.csv"}
               },
    'expect_out': ['b,c', '2,3', '5,6']
}

extra_newline = {
    'name': 'extra_newline',
    'raw_data': ['col1,col2,col3',
                 'ab,"e',
                 'f",cd'],
    'script': {"name": "extra_newline",
               "resources": [
                   {"dialect": {"do_not_bulk_insert": "True"},
                    "name": "extra_newline",
                    "schema": {},
                    "url": "http://example.com/extra_newline.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {"extra_newline": "http://example.com/extra_newline.csv"}
               },
    'expect_out': ['col1,col2,col3', 'ab,e f,cd']
}

change_header_values = {
    'name': 'change_header_values',
    'raw_data': ['a,b,c',
                 '1,2,3',
                 '4,5,6'],
    'script': {"name": "change_header_values",
               "resources": [
                   {
                       "dialect":
                           {"do_not_bulk_insert": "True", "header_rows": 1},
                       "name": "change_header_values",
                       "schema": {
                           "fields": [
                               {
                                   "name": "aa",
                                   "type": "char"
                               },
                               {
                                   "name": "bb",
                                   "size": "20",
                                   "type": "char"
                               },
                               {
                                   "name": "c c",
                                   "size": "20",
                                   "type": "char"
                               }
                           ]
                       },
                       "url": "http://example.com/change_header_values.csv"
                   }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls":
                   {
                       "change_header_values":
                           "http://example.com/change_header_values.csv"
                   }
               },
    'expect_out': ['aa,bb,c_c', '1,2,3', '4,5,6']
}

underscore_csv = {
    'name': 'underscore_csv',
    'raw_data': ['a,b,c',
                 '1,2,y',
                 '4,5,2_0'],
    'script': {"name": "underscore_csv",
               "resources": [
                   {"dialect": {"do_not_bulk_insert": "True"},
                    "name": "underscore_csv",
                    "schema": {
                        "fields": [
                            {
                                "name": "record_id",
                                "type": "pk-auto"
                            },
                            {
                                "name": "a",
                                "type": "int"
                            },
                            {
                                "name": "b",
                                "type": "int"
                            },
                            {
                                "name": "c",
                                "type": "char"
                            }
                        ]
                    },
                    "url": "http://example.com/underscore_csv.csv"
                    }
               ],
               "retriever": "True",
               "retriever_minimum_version": "2.0.dev",
               "version": "1.0.0",
               "urls": {"underscore_csv": "http://example.com/underscore_csv.csv"}
               },
    'expect_out': ['record_id,a,b,c', '1,1,2,y', '2,4,5,2_0']
}


tests = [
    simple_csv,
    comma_delimiter,
    tab_delimiter,
    data_no_header,
    csv_latin1_encoding,
    autopk_csv,
    crosstab,
    autopk_crosstab,
    skip_csv,
    extra_newline,
    change_header_values,
    underscore_csv
]

# Create a tuple of all test scripts with their expected values
test_parameters = [(test, test['expect_out']) for test in tests]

# Skip testing xml on non-ascii data.
# Xml parser raises error, "ParseError: not well-formed (invalid token)"
# and only passes on python3.
# internally xml reads a file as "rb" using the default encoding.
# When it encounters non ascii characters that can not be mapped correctly
# it will raise an error.
# pytest captures that error and fails.
xml_test_parameters = [(test, test['expect_out'])
                       for test in tests if test != csv_latin1_encoding]

file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))


def setup_module():
    """Put raw data and scripts in appropriate .retriever directories."""
    for test in tests:
        if not os.path.exists(os.path.join(HOME_DIR, "raw_data", test['name'])):
            os.makedirs(os.path.join(HOME_DIR, "raw_data", test['name']))
        rd_path = os.path.join(HOME_DIR,
                               "raw_data", test['name'], test['name'] + '.csv')
        create_file(test['raw_data'], rd_path)

        path_js = os.path.join(HOME_DIR, "scripts", test['name'] + '.json')
        with open(path_js, 'w') as js:
            json.dump(test['script'], js, indent=2)
        read_json(os.path.join(HOME_DIR, "scripts", test['name']))


def teardown_module():
    """Remove test data and scripts from .retriever directories."""
    for test in tests:
        shutil.rmtree(os.path.join(HOME_DIR, "raw_data", test['name']))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.json'))
        subprocess.call(['rm', '-r', test['name']])


def get_script_module(script_name):
    """Load a script module."""
    return read_json(os.path.join(HOME_DIR, "scripts", script_name))


def get_output_as_csv(dataset, engines, tmpdir, db):
    """Install dataset and return the output as a string version of the csv."""
    workdir = tmpdir.mkdtemp()
    workdir.chdir()

    # Since we are writing scripts to the .retriever directory,
    # we don't have to change to the main source directory in order
    # to have the scripts loaded
    script_module = get_script_module(dataset["name"])
    engines.script_table_registry = {}
    script_module.download(engines)
    script_module.engine.final_cleanup()
    script_module.engine.to_csv(sort=False)
    # get filename and append .csv
    csv_file = engines.opts['table_name'].format(db=db, table=dataset["name"])
    # csv engine already has the .csv extension
    if engines.opts["engine"] != 'csv':
        csv_file += '.csv'
    obs_out = file_2list(csv_file)
    os.chdir(retriever_root_dir)
    return obs_out


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_csv_integration(dataset, expected, tmpdir):
    csv_engine.opts = {'engine': 'csv', 'table_name': '{db}_{table}', 'data_dir': DATA_DIR}
    assert get_output_as_csv(dataset, csv_engine, tmpdir, db=dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_sqlite_integration(dataset, expected, tmpdir):
    dbfile = 'testdb_retriever.sqlite'
    sqlite_engine.opts = {
        'engine': 'sqlite',
        'file': dbfile,
        'table_name': '{db}_{table}',
        'data_dir': DATA_DIR}
    subprocess.call(['rm', '-r', 'testdb_retriever.sqlite'])
    assert get_output_as_csv(dataset, sqlite_engine, tmpdir, dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", xml_test_parameters)
def test_xmlengine_integration(dataset, expected, tmpdir):
    """Check for xmlenginee regression."""
    xml_engine.opts = {'engine': 'xml', 'table_name': '{db}_{table}', 'data_dir': DATA_DIR}
    assert get_output_as_csv(dataset, xml_engine, tmpdir, db=dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_jsonengine_integration(dataset, expected, tmpdir):
    """Check for jsonenginee regression."""
    json_engine.opts = {'engine': 'json', 'table_name': '{db}_{table}', 'data_dir': DATA_DIR}
    assert get_output_as_csv(dataset, json_engine, tmpdir, db=dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_postgres_integration(dataset, expected, tmpdir):
    """Check for postgres regression."""
    cmd = 'psql -U postgres -d ' + testdb_retriever +' -h ' + pgdb_host + ' -w -c \"DROP SCHEMA IF EXISTS ' + testschema + ' CASCADE\"'
    subprocess.call(shlex.split(cmd))
    postgres_engine.opts = {'engine': 'postgres', 'user': 'postgres',
                            'password': os_password, 'host': pgdb_host,
                            'port': 5432, 'database': testdb_retriever,
                            'database_name': testschema,
                            'table_name': '{db}.{table}'}
    assert get_output_as_csv(dataset, postgres_engine, tmpdir,
                             db=postgres_engine.opts['database_name']) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_mysql_integration(dataset, expected, tmpdir):
    """Check for mysql regression."""
    cmd = 'mysql -u travis -Bse "DROP DATABASE IF EXISTS {testdb_retriever}"'.format(testdb_retriever=testdb_retriever)
    subprocess.call(shlex.split(cmd))
    mysql_engine.opts = {
        'engine': 'mysql',
        'user': 'travis',
        'password': '',
        'host': mysqldb_host,
        'port': 3306,
        'database_name': testdb_retriever,
        'table_name': '{db}.{table}'}
    assert get_output_as_csv(dataset, mysql_engine, tmpdir, db=mysql_engine.opts['database_name']) == expected
