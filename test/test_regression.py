from __future__ import absolute_import

import io
import os
import shutil
import sys
from imp import reload
import imp

from retriever import datasets
from retriever import download
from retriever import install_csv
from retriever import install_json
from retriever import install_mysql
from retriever import install_postgres
from retriever import install_sqlite
from retriever import install_xml
from retriever.lib.defaults import ENCODING
from retriever.lib.defaults import HOME_DIR
from retriever.lib.load_json import read_json


encoding = ENCODING.lower()

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding(encoding)
import pytest
from collections import OrderedDict
from retriever.lib.engine_tools import getmd5
from retriever.engines import engine_list

# Set postgres password, Appveyor service needs the password given
# The Travis service obtains the password from the config file.
if os.name == "nt":
    os_password = "Password12!"
else:
    os_password = ""

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, \
csv_engine, download_engine, json_engine, xml_engine = engine_list
file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))
working_script_dir = os.path.abspath(os.path.join(retriever_root_dir, "scripts"))
HOMEDIR = os.path.expanduser('~')
script_home = "{}/.retriever/scripts".format(HOMEDIR)

download_md5 = [
    ('mt-st-helens-veg', 'd5782e07241cb3fe9f5b2e1bb804a794'),
    ('bird-size', '45c7507ae945868c71b5179f7682ea9c'),
    ('mammal-masses', 'b54b80d0d1959bdea0bb8a59b70fa871')
]

db_md5 = [
    ('flensburg_food_web', '3f0e3c60b80f0bb9326e33c74076b14c'),
    ('bird_size', '98dcfdca19d729c90ee1c6db5221b775'),
    ('mammal_masses', '6fec0fc63007a4040d9bbc5cfcd9953e')
]

python_files = ['flensburg_food_web']


def setup_module():
    """Update retriever scripts and cd to test directory to find data."""
    os.chdir(retriever_root_dir)
    os.system('cp -r {0} {1}'.format("test/raw_data", retriever_root_dir))


def teardown_module():
    """Cleanup temporary output files and return to root directory."""
    os.chdir(retriever_root_dir)
    os.system("rm -r *output*")
    shutil.rmtree(os.path.join(retriever_root_dir, "raw_data"))
    os.system("rm testdb.sqlite")


def get_script_module(script_name):
    """Load a script module"""
    if script_name in python_files:
        file, pathname, desc = imp.find_module(script_name,
                                               [working_script_dir])
        return imp.load_module(script_name + ".py", file, pathname, desc)
    return read_json(os.path.join(retriever_root_dir, "scripts", script_name))


def get_csv_md5(dataset, engine, tmpdir, install_function, config):
    workdir = tmpdir.mkdtemp()
    os.system("cp -r {} {}/".format(os.path.join(retriever_root_dir, 'scripts'), os.path.join(str(workdir), 'scripts')))
    workdir.chdir()
    final_direct = os.getcwd()
    engine.script_table_registry = {}
    engine_obj = install_function(dataset.replace("_", "-"), **config)
    engine_obj.to_csv()
    engine_obj.script_table_registry = {}
    engine.script_table_registry = {}
    # need to remove scripts before checking md5 on dir
    os.system("rm -r scripts")
    current_md5 = getmd5(data=final_direct, data_type='dir')
    os.chdir(retriever_root_dir)
    return current_md5


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_sqlite_regression(dataset, expected, tmpdir):
    """Check for sqlite regression."""
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb.sqlite'))
    sqlite_engine.opts = {
        'engine': 'sqlite',
        'file': dbfile,
        'table_name': '{db}_{table}'}
    interface_opts = {'file': dbfile}
    assert get_csv_md5(dataset, sqlite_engine, tmpdir, install_sqlite, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_postgres_regression(dataset, expected, tmpdir):
    """Check for postgres regression."""
    os.system('psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
    postgres_engine.opts = {'engine': 'postgres',
                            'user': 'postgres',
                            'password': os_password,
                            'host': 'localhost',
                            'port': 5432,
                            'database': 'testdb',
                            'database_name': 'testschema',
                            'table_name': '{db}.{table}'}
    interface_opts = {"user": 'postgres',
                      "password": postgres_engine.opts['password'],
                      "database": postgres_engine.opts['database'],
                      "database_name": postgres_engine.opts['database_name'],
                      "table_name": postgres_engine.opts['table_name']}
    assert get_csv_md5(dataset, postgres_engine, tmpdir, install_postgres, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_mysql_regression(dataset, expected, tmpdir):
    """Check for mysql regression."""
    os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
    mysql_engine.opts = {'engine': 'mysql',
                         'user': 'travis',
                         'password': '',
                         'host': 'localhost',
                         'port': 3306,
                         'database_name': 'testdb',
                         'table_name': '{db}.{table}'}
    interface_opts = {"user": mysql_engine.opts['user'],
                      "database_name": mysql_engine.opts['database_name'],
                      "table_name": mysql_engine.opts['table_name']}
    assert get_csv_md5(dataset, mysql_engine, tmpdir, install_mysql, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_xmlengine_regression(dataset, expected, tmpdir):
    """Check for xmlenginee regression."""
    xml_engine.opts = {
        'engine': 'xml',
        'table_name': '{db}_output_{table}.xml'}
    interface_opts = {'table_name': '{db}_output_{table}.xml'}
    assert get_csv_md5(dataset, xml_engine, tmpdir, install_xml, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_jsonengine_regression(dataset, expected, tmpdir):
    """Check for jsonenginee regression."""
    json_engine.opts = {
        'engine': 'json',
        'table_name': '{db}_output_{table}.json'}
    interface_opts = {'table_name': '{db}_output_{table}.json'}
    assert get_csv_md5(dataset, json_engine, tmpdir, install_json, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_csv_regression(dataset, expected, tmpdir):
    """Check csv regression."""
    csv_engine.opts = {
        'engine': 'csv',
        'table_name': '{db}_output_{table}.csv'}
    interface_opts = {'table_name': '{db}_output_{table}.csv'}
    assert get_csv_md5(dataset, csv_engine, tmpdir, install_csv, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", download_md5)
def test_download_regression(dataset, expected):
    """Test download regression."""
    os.chdir(retriever_root_dir)
    download(dataset, "raw_data/{0}".format(dataset))
    current_md5 = getmd5(data="raw_data/{0}".format(dataset), data_type='dir')
    assert current_md5 == expected
