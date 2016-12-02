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


x= u'{}'.format('a,b,c\n1,2,4Löve\n4,5,6\n')
def test_x():
    assert type(x) == "strd"
simple_csv2 = {'name': 'simple_csv2',
              'raw_data': x,
              'script': """{\n
              "name": "simple_csv2",\n
              "resources": [\n
                  {\n
                      "dialect": {},\n
                      "name": "simple_csv2",\n
                      "schema": {},\n
                      "url": "http://example.com/simple_csv2.txt"\n
                  }\n
              ],\n
              "retriever": "True",\n
              "retriever_minimum_version": "2.0.dev",\n
              "version": 1.0,\n
              "urls": {\n
                  "simple_csv2": "http://example.com/simple_csv2.txt"\n
              }\n
          }\n""",
              'expect_out': u'a,b,c\n1,2,4Löve\n4,5,6\n'}


tests = [simple_csv2]

# Create a tuple of all test scripts and expected values
# (simple_csv, '"a","b","c"\n1,2,3\n4,5,6')
test_parameters = [(test, test['expect_out']) for test in tests]
file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))


def dsetup_module():
    """Put raw data and scripts in appropriate .retriever directories"""
    for test in tests:
        if not os.path.exists(os.path.join(HOME_DIR, "raw_data", test['name'])):
            os.makedirs(os.path.join(HOME_DIR, "raw_data", test['name']))
        create_file(test['raw_data'], os.path.join(HOME_DIR, "raw_data", test['name'], test['name'] + '.txt'))
        create_file(test['script'], os.path.join(HOME_DIR, "scripts", test['name'] + '.json'))
        compile_json(os.path.join(HOME_DIR, "scripts", test['name']))


def dteardown_module():
    """Remove test data and scripts from .retriever directories"""
    for test in tests:
        shutil.rmtree(os.path.join(HOME_DIR, "raw_data", test['name']))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.json'))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.py'))
        os.system("rm -r *{}".format(test['name']))
        os.system("rm testdb.sqlite")


def dget_output_as_csv(dataset, engines, tmpdir, db):
    """Install dataset and return the output as a string version of the csv

    The string version of the csv output returned by this function can be compared
    directly to the expect_out values in the dataset test dictionaries.
    """
    print(tmpdir)
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    os.chdir(tmpdir)
    script_module = dget_script_module(dataset["name"])
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
    print(type(obs_out))


def dget_script_module(script_name):
    """Load a script module"""
    file, pathname, desc = imp.find_module(script_name, [os.path.join(HOME_DIR, "scripts")])
    return imp.load_module(script_name, file, pathname, desc)


mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = ENGINE_LIST()


# @pytest.mark.parametrize("dataset, expected", test_parameters)
def dtest_csv_integration(dataset, expected, tmpdir):
    csv_engine.opts = {'engine': 'csv', 'table_name': '{db}_{table}'}
    dget_output_as_csv(dataset, csv_engine, tmpdir, db=dataset["name"])


def dtest_jsonengine_integration(dataset, expected, tmpdir):
    """Check for jsonenginee regression"""
    json_engine.opts = {'engine': 'json', 'table_name': '{db}_{table}'}
    dget_output_as_csv(dataset, json_engine, tmpdir, db=dataset["name"])


def dtest_sqlite_integration(dataset, expected, tmpdir):
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
    sqlite_engine.opts = {'engine': 'sqlite', 'file': dbfile, 'table_name': '{db}_{table}'}
    os.system("rm testdb.sqlite")
    dget_output_as_csv(dataset, sqlite_engine, tmpdir, dataset["name"])

def dtest_xmlengine_integration(dataset, expected, tmpdir):
    """Check for xmlenginee regression"""
    xml_engine.opts = {'engine': 'xml', 'table_name': '{db}_{table}'}
    dget_output_as_csv(dataset, xml_engine, tmpdir, db=dataset["name"])
# print(simple_csv2["script"])
# print(simple_csv2['expect_out'])
# print(test_parameters)
# print (simple_csv2.get("script"))
dsetup_module()
# test_csv_integration(simple_csv2, simple_csv2.get('expect_out'), "répertoire ")
# test_jsonengine_integration(simple_csv2, simple_csv2.get('expect_out'), "répertoire ")
# dtest_xmlengine_integration(simple_csv2, simple_csv2.get('expect_out'), "rékk")
# dtest_jsonengine_integration(simple_csv2, simple_csv2.get('expect_out'), "répertoire ")
dtest_jsonengine_integration(simple_csv2, simple_csv2.get('expect_out'), "répertoire ")
