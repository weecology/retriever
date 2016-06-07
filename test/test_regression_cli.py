from __future__ import print_function
import imp
import os

import pytest
from retriever.lib.tools import getmd5
from retriever import HOME_DIR, ENGINE_LIST

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = ENGINE_LIST()
dir_path = os.path.dirname(os.path.abspath(__file__))

download_md5 = [
    # ('DelMoral2010', '0'),
    ('avianbodysize', 'dce81ee0f040295cd14c857c18cc3f7e'),
    ('mom2003', 'b54b80d0d1959bdea0bb8a59b70fa871')
]

csv_md5 = [
    # ('DelMoral2010', '0'),
    ('EA_avianbodysize2007', '873597e93bb6163aedd88e285b246c34'),
    ('EA_mom2003', '5fe8b4f182ba2b8be3bb0ddecdb4673c')
]

db_md5 = [
    # ('DelMoral2010', '0'),
    ('EA_avianbodysize2007', '79680888f7768474479e70c87cd36c9d'),
    ('EA_mom2003', '520b29f78dc96e8f2d48b5ef9264ff86')
]

filedb_md5 = [
    # ('DelMoral2010', '0'),
    ('EA_avianbodysize2007', '91aa87a438ddf8fc6c9f9054fe4fda90'),
    ('EA_mom2003', '8dc11ac8d3d3a33e938662dfe39e22c2')
]


def get_script_module(script_name):
    """Load a script module"""
    file, pathname, desc = imp.find_module(script_name, [os.path.join(HOME_DIR, "scripts")])
    return imp.load_module(script_name, file, pathname, desc)


def get_csv_md5(dataset, engines):
    dump_dir()
    script_module = get_script_module(dataset)
    script_module.SCRIPT.download(engines)
    script_module.SCRIPT.engine.final_cleanup()
    script_module.SCRIPT.engine.to_csv()
    os.chdir("..")
    current_md5 = getmd5(data='output_dumps', data_type='dir')
    return current_md5


def setup_module():
    """Update retriever scripts and cd to test directory to find data"""
    os.chdir("./test/")
    os.system("retriever update")


def teardown_module():
    """Cleanup temporary output files after testing and return to root directory"""
    os.system("rm output*")
    os.system("rm -r raw_data/MoM2003")
    os.system("rm -r raw_data/EA*")
    os.chdir("..")


def dump_dir():
    if os.path.exists("output_dumps"):
        os.system("rm -r output_dumps")
    os.makedirs("output_dumps")
    os.chdir("output_dumps")


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_sqlite_regression(dataset, expected):
    """Check for sqlite regression"""
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
    sqlite_engine.opts = {'engine': 'sqlite', 'file': dbfile, 'table_name': '{db}_{table}'}
    assert get_csv_md5(dataset, sqlite_engine) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_postgres_regression(dataset, expected):
    """Check for postgres regression"""
    os.system('psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
    postgres_engine.opts = {'engine': 'postgres', 'user': 'postgres', 'password': "", 'host': 'localhost', 'port': 5432,
                            'database': 'testdb', 'database_name': 'testschema', 'table_name': '{db}.{table}'}
    assert get_csv_md5(dataset, postgres_engine) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_mysql_regression(dataset, expected):
    """Check for mysql regression"""
    os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
    mysql_engine.opts = {'engine': 'mysql', 'user': 'travis', 'password': '', 'host': 'localhost', 'port': 3306,
                         'database_name': 'testdb', 'table_name': '{db}.{table}'}
    assert get_csv_md5(dataset, mysql_engine) == expected


@pytest.mark.parametrize("dataset, expected", filedb_md5)
def test_xmlenginee_regression(dataset, expected):
    """Check for xmlenginee regression"""
    xml_engine.opts = {'engine': 'xml', 'table_name': 'output_file_{table}.xml'}
    assert get_csv_md5(dataset, xml_engine) == expected


@pytest.mark.parametrize("dataset, expected", filedb_md5)
def test_jsonenginee_regression(dataset, expected):
    """Check for jsonenginee regression"""
    json_engine.opts = {'engine': 'json', 'table_name': 'output_file_{table}.json'}
    assert get_csv_md5(dataset, json_engine) == expected


@pytest.mark.parametrize("dataset, expected", csv_md5)
def test_csv_regression(dataset, expected):
    """Check csv regression"""
    csv_engine.opts = {'engine': 'csv', 'table_name': 'output_file_{table}.csv'}
    assert get_csv_md5(dataset, csv_engine) == expected


@pytest.mark.parametrize("dataset, expected", download_md5)
def test_download_regression(dataset, expected):
    """Check for regression for a particular dataset downloaded only"""
    os.system("retriever download {0} -p raw_data/{0}".format(dataset))
    current_md5 = getmd5(data="raw_data/{0}".format(dataset), data_type='dir', mode="rU")
    assert current_md5 == expected
