"""Integrations tests for EcoData Retriever"""

import os
import shutil
from retriever.lib.compile import compile_script
from retriever import HOME_DIR, ENGINE_LIST

simple_csv = {'name': 'simple_csv',
              'raw_data': "a,b,c\n1,2,3\n4,5,6",
              'script': "shortname: simple_csv\ntable: simple_csv, http://example.com/simple_csv.txt",
              'expect_out': "a,b,c\n1,2,3\n4,5,6"}

crosstab = {'name': 'crosstab',
            'raw_data': "a,b,c1,c2\n1,1,1.1,1.2\n1,2,2.1,2.2",
            'script': "shortname: crosstab\ntable: crosstab, http://example.com/crosstab.txt\n*column: a, int\n*column: b, int\n*ct_column: c\n*column: val, ct-double\n*ct_names: c1,c2",
            'expect_out': "a,b,c,val\n1,1,c1,1.1\n1,1,c2,1.2\n1,2,c1,2.1\n1,2,c2,2.2"}

tests = [simple_csv, crosstab]

def setup_module():
    """Put raw data and scripts in appropriate .retriever directories"""
    for test in tests:
        if not os.path.exists(os.path.join(HOME_DIR, "raw_data", test['name'])):
            os.makedirs(os.path.join(HOME_DIR, "raw_data", test['name']))
        data_file = open(os.path.join(HOME_DIR, "raw_data", test['name'], test['name'] + '.txt'), 'w')
        script_file = open(os.path.join(HOME_DIR, "scripts", test['name'] + '.script'), 'w')
        data_file.write(test['raw_data'])
        script_file.write(test['script'])
        compile_script(os.path.join(HOME_DIR, "scripts", test['name']))

def teardown_module():
    """Remove test data and scripts from .retriever directories"""
    for test in tests:
        shutil.rmtree(os.path.join(HOME_DIR, "raw_data", test['name']))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.script'))

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine = ENGINE_LIST()
csv_engine.opts = {'engine': 'csv', 'table_name': './{db}_{table}.csv'}
