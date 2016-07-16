"""Integrations tests for EcoData Retriever"""
from __future__ import print_function
import imp
import os
import shutil
import pytest

from retriever.lib.compile import compile_script
from retriever import HOME_DIR, ENGINE_LIST
from retriever.lib.tools import file_2string
from retriever.lib.tools import create_file


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

# Create a tuple of all test scripts and expected values
# (simple_csv, '"a","b","c"\n1,2,3\n4,5,6')
test_parameters = [(test, test['expect_out']) for test in tests]


def setup_module():
    """Put raw data and scripts in appropriate .retriever directories"""
    for test in tests:
        if not os.path.exists(os.path.join(HOME_DIR, "raw_data", test['name'])):
            os.makedirs(os.path.join(HOME_DIR, "raw_data", test['name']))
        create_file(test['raw_data'], os.path.join(HOME_DIR, "raw_data", test['name'], test['name'] + '.txt'))
        create_file(test['script'], os.path.join(HOME_DIR, "scripts", test['name'] + '.script'))
        compile_script(os.path.join(HOME_DIR, "scripts", test['name']))


def teardown_module():
    """Remove test data and scripts from .retriever directories"""
    for test in tests:
        shutil.rmtree(os.path.join(HOME_DIR, "raw_data", test['name']))
        os.remove(os.path.join(HOME_DIR, "scripts", test['name'] + '.script'))
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
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return obs_out


def get_script_module(script_name):
    """Load a script module"""
    file, pathname, desc = imp.find_module(script_name, [os.path.join(HOME_DIR, "scripts")])
    return imp.load_module(script_name, file, pathname, desc)

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = ENGINE_LIST()


@pytest.mark.parametrize("dataset, expected",test_parameters)
def test_csv_integration(dataset, expected, tmpdir):
    csv_engine.opts = {'engine': 'csv', 'table_name': '{db}_{table}'}
    assert get_output_as_csv(dataset, csv_engine, tmpdir, db=dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected",test_parameters)
def test_sqlite_integration(dataset, expected, tmpdir):
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
    sqlite_engine.opts = {'engine': 'sqlite', 'file': dbfile, 'table_name': '{db}_{table}'}
    os.system("rm testdb.sqlite")
    assert get_output_as_csv(dataset, sqlite_engine, tmpdir, dataset["name"]) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
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
    postgres_engine.opts = {'engine': 'postgres', 'user': 'postgres', 'password': "", 'host': 'localhost', 'port': 5432,
                            'database': 'testdb', 'database_name': 'testschema', 'table_name': '{db}.{table}'}
    assert get_output_as_csv(dataset, postgres_engine, tmpdir, db=postgres_engine.opts['database_name']) == expected


@pytest.mark.parametrize("dataset, expected", test_parameters)
def test_mysql_integration(dataset, expected, tmpdir):
    """Check for mysql regression"""
    os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
    mysql_engine.opts = {'engine': 'mysql', 'user': 'travis', 'password': '', 'host': 'localhost', 'port': 3306,
                         'database_name': 'testdb', 'table_name': '{db}.{table}'}
    assert get_output_as_csv(dataset, mysql_engine, tmpdir, db=mysql_engine.opts['database_name']) == expected
