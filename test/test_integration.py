"""Integrations tests for EcoData Retriever"""

import imp
import os
import shutil
from retriever.lib.compile import compile_script
from retriever import HOME_DIR, ENGINE_LIST

simple_csv = {'name': 'simple_csv',
              'raw_data': "a,b,c\n1,2,3\n4,5,6\n",
              'script': "shortname: simple_csv\ntable: simple_csv, http://example.com/simple_csv.txt",
              'expect_out': '"record_id","a","b","c"\n1,1,2,3\n2,4,5,6'}

crosstab = {'name': 'crosstab',
            'raw_data': "a,b,c1,c2\n1,1,1.1,1.2\n1,2,2.1,2.2",
            'script': "shortname: crosstab\ntable: crosstab, http://example.com/crosstab.txt\n*column: record_id, pk-auto\n*column: a, int\n*column: b, int\n*ct_column: c\n*column: val, ct-double\n*ct_names: c1,c2",
            'expect_out': '"record_id","a","b","c","val"\n3,1,1,"c1",1.1\n4,1,1,"c2",1.2\n5,1,2,"c1",2.1\n6,1,2,"c2",2.2'}

tests = [simple_csv, crosstab]

def setup_module():
    """Put raw data and scripts in appropriate .retriever directories"""
    for test in tests:
        if not os.path.exists(os.path.join(HOME_DIR, "raw_data", test['name'])):
            os.makedirs(os.path.join(HOME_DIR, "raw_data", test['name']))
        with open(os.path.join(HOME_DIR, "raw_data", test['name'], test['name'] + '.txt'), 'w') as data_file:
            data_file.write(test['raw_data'])
        with open(os.path.join(HOME_DIR, "scripts", test['name'] + '.script'), 'w') as script_file:
            script_file.write(test['script'])
        compile_script(os.path.join(HOME_DIR, "scripts", test['name']))

def teardown_module():
    """Remove test data and scripts from .retriever directories"""
    for test in tests:
        shutil.rmtree(os.path.join(HOME_DIR, "raw_data", test['name']))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.script'))

def get_script_module(script_name):
    """Load a script module"""
    file, pathname, desc = imp.find_module(script_name, [os.path.join(HOME_DIR, "scripts")])
    return imp.load_module(script_name, file, pathname, desc)

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = ENGINE_LIST()
csv_engine.opts = {'engine': 'csv', 'table_name': './{db}_{table}.txt'}

def test_csv_from_csv():
    simple_csv_module = get_script_module('simple_csv')
    simple_csv_module.SCRIPT.download(csv_engine)
    simple_csv_module.SCRIPT.engine.disconnect()
    with open("simple_csv_simple_csv.txt", 'r') as obs_out_file:
        obs_out = obs_out_file.read()
    print len(obs_out)
    assert obs_out == simple_csv['expect_out']

def test_crosstab_from_csv():
    crosstab_module = get_script_module('crosstab')
    crosstab_module.SCRIPT.download(csv_engine)
    crosstab_module.SCRIPT.engine.disconnect()
    with open("crosstab_crosstab.txt", 'r') as obs_out_file:
        obs_out = obs_out_file.read()
    print len(obs_out)
    assert obs_out == crosstab['expect_out']
