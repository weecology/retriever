from __future__ import print_function
import imp
import os
import sys

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('latin-1')
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

db_md5 = [
    # ('DelMoral2010', '0'),
    ('EA_avianbodysize2007', '74a5421622ab73c1df2ff8afc9d67e03'),
    ('EA_mom2003', '92bf63eb5b36b777c600d0a95229222c')
]

filedb_md5 = [
    # ('DelMoral2010', '0'),
    ('EA_avianbodysize2007', 'ca8f7e670ff98b520371d3fabf9a8632'),
    ('EA_mom2003', '92bf63eb5b36b777c600d0a95229222c')
]


def get_script_module(script_name):
    """Load a script module"""
    file, pathname, desc = imp.find_module(script_name, [os.path.join(HOME_DIR, "scripts")])
    return imp.load_module(script_name, file, pathname, desc)


def get_csv_md5(dataset, engines, tmpdir):
    workdir = tmpdir.mkdtemp()
    workdir.chdir()
    script_module = get_script_module(dataset)
    script_module.SCRIPT.download(engines)
    script_module.SCRIPT.engine.final_cleanup()
    script_module.SCRIPT.engine.to_csv()
    current_md5 = getmd5(data=str(workdir), data_type='dir')
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


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_sqlite_regression(dataset, expected, tmpdir):
    """Check for sqlite regression"""
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
    sqlite_engine.opts = {'engine': 'sqlite', 'file': dbfile, 'table_name': '{db}_{table}'}
    assert get_csv_md5(dataset, sqlite_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_postgres_regression(dataset, expected, tmpdir):
    """Check for postgres regression"""
    os.system('psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
    postgres_engine.opts = {'engine': 'postgres', 'user': 'postgres', 'password': "", 'host': 'localhost', 'port': 5432,
                            'database': 'testdb', 'database_name': 'testschema', 'table_name': '{db}.{table}'}
    assert get_csv_md5(dataset, postgres_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_mysql_regression(dataset, expected, tmpdir):
    """Check for mysql regression"""
    os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
    mysql_engine.opts = {'engine': 'mysql', 'user': 'travis', 'password': '', 'host': 'localhost', 'port': 3306,
                         'database_name': 'testdb', 'table_name': '{db}.{table}'}
    assert get_csv_md5(dataset, mysql_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", filedb_md5)
def test_xmlenginee_regression(dataset, expected, tmpdir):
    """Check for xmlenginee regression"""
    xml_engine.opts = {'engine': 'xml', 'table_name': 'output_file_{table}.xml'}
    assert get_csv_md5(dataset, xml_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", filedb_md5)
def test_jsonenginee_regression(dataset, expected, tmpdir):
    """Check for jsonenginee regression"""
    json_engine.opts = {'engine': 'json', 'table_name': 'output_file_{table}.json'}
    assert get_csv_md5(dataset, json_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", filedb_md5)
def test_csv_regression(dataset, expected, tmpdir):
    """Check csv regression"""
    csv_engine.opts = {'engine': 'csv', 'table_name': 'output_file_{table}.csv'}
    assert get_csv_md5(dataset, csv_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", download_md5)
def test_download_regression(dataset, expected):
    """Check for regression for a particular dataset downloaded only"""
    os.system("retriever download {0} -p raw_data/{0}".format(dataset))
    current_md5 = getmd5(data="raw_data/{0}".format(dataset), data_type='dir', mode="rU")
    assert current_md5 == expected
