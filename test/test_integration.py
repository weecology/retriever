# -*- coding: latin-1  -*-
# """Integrations tests for Data Retriever"""
from __future__ import print_function
import imp
import os
import sys
import shutil
from imp import reload

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('latin-1')
import pytest
from retriever.lib.compile import compile_json
from retriever import HOME_DIR, ENGINE_LIST
from retriever.lib.tools import file_2string
from retriever.lib.tools import create_file

# Set postgres password, Appveyor service needs the password given
# The Travis service obtains the password from the config file.
if os.name == "nt":
    os_password = "Password12!"
else:
    os_password = ""

simple_csv = {'name': 'simple_csv',
              'raw_data': "a,b,c\n1,2,3\n4,5,6\n",
              'script': """{\n
                        "name": "simple_csv",\n
                        "resources": [\n
                            {\n
                                "dialect": {\n
                                "do_not_bulk_insert": "True"\n
                            },\n
                            "name": "simple_csv",\n
                                "schema": {},\n
                                "url": "http://example.com/simple_csv.txt"\n
                            }\n
                        ],\n
                        "retriever": "True",\n
                        "retriever_minimum_version": "2.0.dev",\n
                        "version": "1.0.0",\n
                        "urls": {\n
                            "simple_csv": "http://example.com/simple_csv.txt"\n
                        }\n
                    }\n""",
              'expect_out': 'a,b,c\n1,2,3\n4,5,6\n'}

data_no_header = {'name': 'data_no_header',
              'raw_data': "1,2,3\n4,5,6\n",
              'script': """{\n
                        "name": "data_no_header",\n
                        "resources": [\n
                            {\n
                                "dialect": {\n
                                "do_not_bulk_insert": "True",\n
                                "header_rows": 0\n
                            },\n
                            "name": "data_no_header",\n
                                "schema": {\n
                                "fields": [\n
                                            {\n
                                                "name": "a",\n
                                                "type": "char"\n
                                            },\n
                                            {\n
                                                "name": "b",\n
                                                "size": "20",\n
                                                "type": "char"\n
                                            },\n
                                            {\n
                                                "name": "c",\n
                                                "size": "20",\n
                                                "type": "char"\n
                                            }\n
                                ]\n
                                },\n
                                "url": "http://example.com/data_no_header.txt"\n
                            }\n
                        ],\n
                        "retriever": "True",\n
                        "retriever_minimum_version": "2.0.dev",\n
                        "version": "1.0.0",\n
                        "urls": {\n
                            "data_no_header": "http://example.com/data_no_header.txt"\n
                        }\n
                    }\n""",
              'expect_out': 'a,b,c\n1,2,3\n4,5,6\n'}

csv_latin1_encoding = {'name': 'csv_latin1_encoding',
              'raw_data': 'a,b,c\n1,2,4Löve\n4,5,6\n',
              'script': """{\n
              "name": "csv_latin1_encoding",\n
              "resources": [\n
                            {\n
                                "dialect": {\n
                                "do_not_bulk_insert": "True"\n
                            },\n
                            "name": "csv_latin1_encoding",\n
                                "schema": {},\n
                                "url": "http://example.com/csv_latin1_encoding.txt"\n
                  }\n
              ],\n
              "retriever": "True",\n
              "retriever_minimum_version": "2.0.dev",\n
              "version": "1.0.0",\n
              "urls": {\n
                  "csv_latin1_encoding": "http://example.com/csv_latin1_encoding.txt"\n
              }\n
          }\n""",
              'expect_out': u'a,b,c\n1,2,4Löve\n4,5,6\n'}


autopk_csv = {'name': 'autopk_csv',
              'raw_data': "a,b,c\n1,2,3\n4,5,6\n",
              'script': """{\n
                        "name": "autopk_csv",\n
                        "resources": [\n
                            {\n
                                "dialect": {},\n
                                "name": "autopk_csv",\n
                                "schema": {\n
                                    "fields": [\n
                                        {\n
                                            "name": "record_id",\n
                                            "type": "pk-auto"\n
                                        },\n
                                        {\n
                                            "name": "a",\n
                                            "type": "int"\n
                                        },\n
                                        {\n
                                            "name": "b",\n
                                            "type": "int"\n
                                        },\n
                                        {\n
                                            "name": "c",\n
                                            "type": "int"\n
                                        }\n
                                    ]\n
                                },\n
                                "url": "http://example.com/autopk_csv.txt"\n
                            }\n
                        ],\n
                        "retriever": "True",\n
                        "retriever_minimum_version": "2.0.dev",\n
                        "version": "1.0.0",\n
                        "urls": {\n
                            "autopk_csv": "http://example.com/autopk_csv.txt"\n
                        }\n
                    }\n
                    """,
              'expect_out': 'record_id,a,b,c\n1,1,2,3\n2,4,5,6\n'}

crosstab = {'name': 'crosstab',
            'raw_data': "a,b,c1,c2\n1,1,1.1,1.2\n1,2,2.1,2.2\n",
            'script': """{\n
                    "name": "crosstab",\n
                    "resources": [\n
                        {\n
                            "dialect": {},\n
                            "name": "crosstab",\n
                            "schema": {\n
                                "ct_column": "c",\n
                                "ct_names": [\n
                                    "c1",\n
                                    "c2"\n
                                ],\n
                                "fields": [\n
                                    {\n
                                        "name": "a",\n
                                        "type": "int"\n
                                    },\n
                                    {\n
                                        "name": "b",\n
                                        "type": "int"\n
                                    },\n
                                    {\n
                                        "name": "val",\n
                                        "type": "ct-double"\n
                                    }\n
                                ]\n
                            },\n
                            "url": "http://example.com/crosstab.txt"\n
                        }\n
                    ],\n
                    "retriever": "True",\n
                    "retriever_minimum_version": "2.0.dev",\n
                    "version": "1.0.0",\n
                    "urls": {\n
                        "crosstab": "http://example.com/crosstab.txt"\n
                    }\n
                }\n
                """,
            'expect_out': 'a,b,c,val\n1,1,c1,1.1\n1,1,c2,1.2\n1,2,c1,2.1\n1,2,c2,2.2\n'}

autopk_crosstab = {'name': 'autopk_crosstab',
                   'raw_data': "a,b,c1,c2\n1,1,1.1,1.2\n1,2,2.1,2.2\n",
                   'script': """{\n
                            "name": "autopk_crosstab",\n
                            "resources": [\n
                                {\n
                                    "dialect": {},\n
                                    "name": "autopk_crosstab",\n
                                    "schema": {\n
                                        "ct_column": "c",\n
                                        "ct_names": [\n
                                            "c1",\n
                                            "c2"\n
                                        ],\n
                                        "fields": [\n
                                            {\n
                                                "name": "record_id",\n
                                                "type": "pk-auto"\n
                                            },\n
                                            {\n
                                                "name": "a",\n
                                                "type": "int"\n
                                            },\n
                                            {\n
                                                "name": "b",\n
                                                "type": "int"\n
                                            },\n
                                            {\n
                                                "name": "val",\n
                                                "type": "ct-double"\n
                                            }\n
                                        ]\n
                                    },\n
                                    "url": "http://example.com/autopk_crosstab.txt"\n
                                }\n
                            ],\n
                            "retriever": "True",\n
                            "retriever_minimum_version": "2.0.dev",\n
                            "version": "1.0.0",\n
                            "urls": {\n
                                "autopk_crosstab": "http://example.com/autopk_crosstab.txt"\n
                            }\n
                        }\n
                        """,
                   'expect_out': 'record_id,a,b,c,val\n1,1,1,c1,1.1\n2,1,1,c2,1.2\n3,1,2,c1,2.1\n4,1,2,c2,2.2\n'}

skip_csv = {'name': 'skip_csv',
            'raw_data': "a,b,c\n1,2,3\n4,5,6\n",
            'script': """{\n
                    "name": "skip_csv",\n
                    "resources": [\n
                        {\n
                            "dialect": {\n
                                "do_not_bulk_insert": "True"\n
                            },\n
                            "name": "skip_csv",\n
                            "schema": {\n
                                "fields": [\n
                                    {\n
                                        "name": "a",\n
                                        "type": "skip"\n
                                    },\n
                                    {\n
                                        "name": "b",\n
                                        "type": "int"\n
                                    },\n
                                    {\n
                                        "name": "c",\n
                                        "type": "int"\n
                                    }\n
                                ]\n
                            },\n
                            "url": "http://example.com/skip_csv.txt"\n
                        }\n
                    ],\n
                    "retriever": "True",\n
                    "retriever_minimum_version": "2.0.dev",\n
                    "version": "1.0.0",\n
                    "urls": {\n
                        "skip_csv": "http://example.com/skip_csv.txt"\n
                    }\n
                }\n
                """,
            'expect_out': 'b,c\n2,3\n5,6\n'}

extra_newline = {'name': 'extra_newline',
                 'raw_data': 'col1,col2,col3\nab,"e\nf",cd',

                 'script': """{\n
                        "name": "extra_newline",\n
                        "resources": [\n
                            {\n
                            "dialect": {\n
                                "do_not_bulk_insert": "True"\n
                            },\n
                                "name": "extra_newline",\n
                                "schema": {},\n
                                "url": "http://example.com/extra_newline.txt"\n
                            }\n
                        ],\n
                        "retriever": "True",\n
                        "retriever_minimum_version": "2.0.dev",\n
                        "version": "1.0.0",\n
                        "urls": {\n
                            "extra_newline": "http://example.com/extra_newline.txt"\n
                        }\n
                    }\n
                    """,
                 'expect_out': "col1,col2,col3\nab,e f,cd\n"}

change_header_values = {'name': 'change_header_values',
              'raw_data': "a,b,c\n1,2,3\n4,5,6\n",
              'script': """{\n
                        "name": "change_header_values",\n
                        "resources": [\n
                            {\n
                                "dialect": {\n
                                "do_not_bulk_insert": "True",\n
                                "header_rows": 1\n
                            },\n
                            "name": "change_header_values",\n
                                "schema": {\n
                                "fields": [\n
                                            {\n
                                                "name": "aa",\n
                                                "type": "char"\n
                                            },\n
                                            {\n
                                                "name": "bb",\n
                                                "size": "20",\n
                                                "type": "char"\n
                                            },\n
                                            {\n
                                                "name": "c c",\n
                                                "size": "20",\n
                                                "type": "char"\n
                                            }\n
                                ]\n
                                },\n
                                "url": "http://example.com/change_header_values.txt"\n
                            }\n
                        ],\n
                        "retriever": "True",\n
                        "retriever_minimum_version": "2.0.dev",\n
                        "version": "1.0.0",\n
                        "urls": {\n
                            "change_header_values": "http://example.com/change_header_values.txt"\n
                        }\n
                    }\n""",
              'expect_out': 'aa,bb,c_c\n1,2,3\n4,5,6\n'}

tests = [simple_csv, data_no_header, csv_latin1_encoding, autopk_csv, crosstab, autopk_crosstab, skip_csv, extra_newline, change_header_values]

# Create a tuple of all test scripts and expected values
# (simple_csv, '"a","b","c"\n1,2,3\n4,5,6')
test_parameters = [(test, test['expect_out']) for test in tests]

# Skip testing xml on non-ascii data
# Xml parser raises error  ParseError: not well-formed (invalid token) using and only passes on python3
# internally xml reads a file as "rb" using the default encoding. When it encounters non ascii characters that
# can not be mapped correctly it will raise an error. pytest captures that error and fails.
xml_test_parameters = [(test, test['expect_out']) for test in tests if test != csv_latin1_encoding]

file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))


def setup_module():
    """Put raw data and scripts in appropriate .retriever directories"""
    for test in tests:
        if not os.path.exists(os.path.join(HOME_DIR, "raw_data", test['name'])):
            os.makedirs(os.path.join(HOME_DIR, "raw_data", test['name']))
        create_file(test['raw_data'], os.path.join(HOME_DIR, "raw_data", test['name'], test['name'] + '.txt'))
        create_file(test['script'], os.path.join(HOME_DIR, "scripts", test['name'] + '.json'))
        compile_json(os.path.join(HOME_DIR, "scripts", test['name']))


def teardown_module():
    """Remove test data and scripts from .retriever directories"""
    for test in tests:
        shutil.rmtree(os.path.join(HOME_DIR, "raw_data", test['name']))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.json'))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.py'))
        os.system("rm -r *{}".format(test['name']))
        os.system("rm testdb.sqlite")


def get_output_as_csv(dataset, engines, tmpdir, db):
    """Install dataset and return the output as a string version of the csv

    The string version of the csv output returned by this function can be compared
    directly to the expect_out values in the dataset test dictionaries.
    """
    workdir = tmpdir.mkdtemp()
    workdir.chdir()
    script_module = get_script_module(dataset["name"])
    script_module.SCRIPT.download(engines)
    script_module.SCRIPT.engine.final_cleanup()
    script_module.SCRIPT.engine.to_csv()
    # get filename and append .csv
    csv_file = engines.opts['table_name'].format(db=db, table=dataset["name"])
    # csv engine already has the .csv extension
    if engines.opts["engine"] != 'csv':
        csv_file += '.csv'
    obs_out = file_2string(csv_file)
    os.chdir(retriever_root_dir)
    return obs_out


def get_script_module(script_name):
    """Load a script module"""
    file, pathname, desc = imp.find_module(script_name, [os.path.join(HOME_DIR, "scripts")])
    return imp.load_module(script_name, file, pathname, desc)


mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = ENGINE_LIST()


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_csv_integration(dataset, expected, tmpdir):
    csv_engine.opts = {'engine': 'csv', 'table_name': '{db}_{table}'}
    assert get_output_as_csv(dataset, csv_engine, tmpdir, db=dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_sqlite_integration(dataset, expected, tmpdir):
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
    sqlite_engine.opts = {'engine': 'sqlite', 'file': dbfile, 'table_name': '{db}_{table}'}
    os.system("rm testdb.sqlite")
    assert get_output_as_csv(dataset, sqlite_engine, tmpdir, dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", xml_test_parameters)
def test_xmlengine_integration(dataset, expected, tmpdir):
    """Check for xmlenginee regression"""
    xml_engine.opts = {'engine': 'xml', 'table_name': '{db}_{table}'}
    assert get_output_as_csv(dataset, xml_engine, tmpdir, db=dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_jsonengine_integration(dataset, expected, tmpdir):
    """Check for jsonenginee regression"""
    json_engine.opts = {'engine': 'json', 'table_name': '{db}_{table}'}
    assert get_output_as_csv(dataset, json_engine, tmpdir, db=dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_postgres_integration(dataset, expected, tmpdir):
    """Check for postgres regression"""
    os.system('psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
    postgres_engine.opts = {'engine': 'postgres', 'user': 'postgres', 'password': os_password, 'host': 'localhost', 'port': 5432,
                            'database': 'testdb', 'database_name': 'testschema', 'table_name': '{db}.{table}'}
    assert get_output_as_csv(dataset, postgres_engine, tmpdir, db=postgres_engine.opts['database_name']) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_mysql_integration(dataset, expected, tmpdir):
    """Check for mysql regression"""
    os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
    mysql_engine.opts = {'engine': 'mysql', 'user': 'travis', 'password': '', 'host': 'localhost', 'port': 3306,
                         'database_name': 'testdb', 'table_name': '{db}.{table}'}
    assert get_output_as_csv(dataset, mysql_engine, tmpdir, db=mysql_engine.opts['database_name']) == expected
