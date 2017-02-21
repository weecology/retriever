from __future__ import absolute_import
from imp import reload
import imp
import os
import sys
import shutil

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('latin-1')
import pytest
from retriever.lib.tools import getmd5
from retriever import ENGINE_LIST

# Set postgres password, Appveyor service needs the password given
# The Travis service obtains the password from the config file.
if os.name == "nt":
    os_password = "Password12!"
else:
    os_password = ""

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = ENGINE_LIST()
file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))
working_script_dir = os.path.abspath(os.path.join(retriever_root_dir, "scripts"))
HOMEDIR = os.path.expanduser('~')

download_md5 = [
    ('mt-st-helens-veg', '9f81bbccfd6a99938e5455a489fdb7b5'),
    ('bird-size', 'dce81ee0f040295cd14c857c18cc3f7e'),
    ('mammal-masses', 'b54b80d0d1959bdea0bb8a59b70fa871')
]

db_md5 = [
    # ('mt_st_helens_veg', '0'),
    ('bird_size', '98dcfdca19d729c90ee1c6db5221b775'),
    ('mammal_masses', '6fec0fc63007a4040d9bbc5cfcd9953e')
]


def get_script_module(script_name):
    """Load a script module from the downloaded scripts directory in the retriever"""
    file, pathname, desc = imp.find_module(script_name, [working_script_dir])
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
    os.chdir(retriever_root_dir)
    os.system('cp -r {0} {1}'.format(os.path.join(retriever_root_dir, "test/raw_data"), retriever_root_dir))


def teardown_module():
    """Cleanup temporary output files after testing and return to root directory"""
    os.chdir(retriever_root_dir)
    os.system("rm -r output*")
    shutil.rmtree(os.path.join(retriever_root_dir, "raw_data"))
    os.system("rm testdb.sqlite")


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_sqlite_regression(dataset, expected, tmpdir):
    """Check for sqlite regression"""
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
    sqlite_engine.opts = {'engine': 'sqlite', 'file': dbfile, 'table_name': '{db}_{table}'}
    assert get_csv_md5(dataset, sqlite_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_postgres_regression(dataset, expected, tmpdir):
    """Check for postgres regression"""
    os.system(
        'psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
    postgres_engine.opts = {'engine': 'postgres',
                            'user': 'postgres',
                            'password': os_password,
                            'host': 'localhost',
                            'port': 5432,
                            'database': 'testdb',
                            'database_name': 'testschema',
                            'table_name': '{db}.{table}'}
    assert get_csv_md5(dataset, postgres_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_mysql_regression(dataset, expected, tmpdir):
    """Check for mysql regression"""
    os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
    mysql_engine.opts = {'engine': 'mysql',
                         'user': 'travis',
                         'password': '',
                         'host': 'localhost',
                         'port': 3306,
                         'database_name': 'testdb',
                         'table_name': '{db}.{table}'}
    assert get_csv_md5(dataset, mysql_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_xmlengine_regression(dataset, expected, tmpdir):
    """Check for xmlenginee regression"""
    xml_engine.opts = {'engine': 'xml',
                       'table_name': 'output_file_{table}.xml'}
    assert get_csv_md5(dataset, xml_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_jsonengine_regression(dataset, expected, tmpdir):
    """Check for jsonenginee regression"""
    json_engine.opts = {'engine': 'json',
                        'table_name': 'output_file_{table}.json'}
    assert get_csv_md5(dataset, json_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_csv_regression(dataset, expected, tmpdir):
    """Check csv regression"""
    csv_engine.opts = {'engine': 'csv',
                       'table_name': 'output_file_{table}.csv'}
    assert get_csv_md5(dataset, csv_engine, tmpdir) == expected


@pytest.mark.parametrize("dataset, expected", download_md5)
def test_download_regression(dataset, expected):
    """Check for regression for a particular dataset downloaded only"""
    os.chdir(retriever_root_dir)
    os.system("retriever download {0} -p raw_data/{0}".format(dataset))
    current_md5 = getmd5(data="raw_data/{0}".format(dataset), data_type='dir')
    assert current_md5 == expected
