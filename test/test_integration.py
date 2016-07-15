"""Integrations tests for EcoData Retriever"""
from __future__ import print_function
import imp
import os
import shutil
import pytest

from retriever.lib.compile import compile_script
from retriever import HOME_DIR, ENGINE_LIST
from retriever.lib.tools import file_2string


simple_csv = {'name': 'simple_csv',
              'raw_data': "a,b,c\n1,2,3\n4,5,6\n",
              'script': "shortname: simple_csv\ntable: simple_csv, http://example.com/simple_csv.txt",
              'expect_out': 'a,b,c\n1,2,3\n4,5,6\n'}

autopk_csv = {'name': 'autopk_csv',
              'raw_data': "a,b,c\n1,2,3\n4,5,6\n",
              'script': "shortname: autopk_csv\ntable: autopk_csv, http://example.com/autopk_csv.txt\n*column: record_id, pk-auto\n*column: a, int\n*column: b, int\n*column: c, int",
              'expect_out': 'record_id,a,b,c\n1,1,2,3\n2,4,5,6\n'}

crosstab = {'name': 'crosstab',
            'raw_data': "a,b,c1,c2\n1,1,1.1,1.2\n1,2,2.1,2.2\n",
            'script': "shortname: crosstab\ntable: crosstab, http://example.com/crosstab.txt\n*column: a, int\n*column: b, int\n*ct_column: c\n*column: val, ct-double\n*ct_names: c1,c2",
            'expect_out': 'a,b,c,val\n1,1,c1,1.1\n1,1,c2,1.2\n1,2,c1,2.1\n1,2,c2,2.2\n'}

autopk_crosstab = {'name': 'autopk_crosstab',
            'raw_data': "a,b,c1,c2\n1,1,1.1,1.2\n1,2,2.1,2.2\n",
            'script': "shortname: autopk_crosstab\ntable: autopk_crosstab, http://example.com/autopk_crosstab.txt\n*column: record_id, pk-auto\n*column: a, int\n*column: b, int\n*ct_column: c\n*column: val, ct-double\n*ct_names: c1,c2",
            'expect_out': 'record_id,a,b,c,val\n1,1,1,c1,1.1\n2,1,1,c2,1.2\n3,1,2,c1,2.1\n4,1,2,c2,2.2\n'}

tests = [simple_csv, autopk_csv, crosstab, autopk_crosstab]

# create a tuple of all test scripts and expected values
# (simple_csv, '"a","b","c"\n1,2,3\n4,5,6')
test_parameters = [(test, test['expect_out']) for test in tests]


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
        os.system("rm -r *{}".format(test['name']))


def get_csv_string(dataset, engines, tmpdir):
    workdir = tmpdir.mkdtemp()
    workdir.chdir()
    script_module = get_script_module(dataset["name"])
    script_module.SCRIPT.download(engines)
    script_module.SCRIPT.engine.final_cleanup()
    script_module.SCRIPT.engine.to_csv()
    obs_out = file_2string(dataset["name"] + "_" + dataset["name"] + ".txt")
    return obs_out


def get_script_module(script_name):
    """Load a script module"""
    file, pathname, desc = imp.find_module(script_name, [os.path.join(HOME_DIR, "scripts")])
    return imp.load_module(script_name, file, pathname, desc)

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = ENGINE_LIST()
csv_engine.opts = {'engine': 'csv', 'table_name': './{db}_{table}.txt'}


@pytest.mark.parametrize("dataset, expected",test_parameters)
def test_csv_engine(dataset, expected, tmpdir):
    csv_engine.opts = {'engine': 'csv', 'table_name': './{db}_{table}.txt'}
    assert get_csv_string(dataset, csv_engine, tmpdir) == expected
