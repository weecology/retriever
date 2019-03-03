from __future__ import absolute_import

import imp
import numpy as np
import os
import shlex
import shutil
import subprocess
import sys
from imp import reload

from retriever import download
from retriever import fetch
from retriever import install_csv
from retriever import install_json
from retriever import install_mysql
from retriever import install_postgres
from retriever import install_sqlite
from retriever import install_xml
from retriever.lib.defaults import ENCODING, DATA_DIR
from retriever.lib.load_json import read_json

encoding = ENCODING.lower()

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding(encoding)
import pytest
from retriever.lib.engine_tools import getmd5
from retriever.engines import engine_list

# Set postgres password, Appveyor service needs the password given
# The Travis service obtains the password from the config file.
os_password = ""
pgdb_host = "localhost"
mysqldb_host = "localhost"
testdb_retriever = "testdb_retriever"
testschema = "testschema_retriever"

if os.name == "nt":
    os_password = "Password12!"

docker_or_travis = os.environ.get("IN_DOCKER")
if docker_or_travis == "true":
    os_password = 'Password12!'
    pgdb_host = "pgdb_retriever"
    mysqldb_host = "mysqldb_retriever"

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, \
csv_engine, download_engine, json_engine, xml_engine = engine_list
file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))
working_script_dir = os.path.abspath(os.path.join(retriever_root_dir, "scripts"))
HOMEDIR = os.path.expanduser('~')
script_home = '{}/.retriever/scripts'.format(HOMEDIR)

download_md5 = [
    ('mt-st-helens-veg', 'd5782e07241cb3fe9f5b2e1bb804a794'),
    ('bird-size', '45c7507ae945868c71b5179f7682ea9c'),
    ('mammal-masses', 'b54b80d0d1959bdea0bb8a59b70fa871')
]

db_md5 = [
    ('flensburg_food_web', '89c8ae47fb419d0336b2c22219f23793'),
    ('bird_size', '98dcfdca19d729c90ee1c6db5221b775'),
    ('mammal_masses', '6fec0fc63007a4040d9bbc5cfcd9953e')
]

# Tuple of (dataset_name, list of dict values corresponding to a table)
fetch_tests = [
    ('iris',
     [{'Iris': [[5.1, 3.5, 1.4, 0.2, 'Iris-setosa'],
                     ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'classes']]
       }]
     ),
    ('flensburg-food-web',
     [{'nodes': [
         [2, 2, 1, 'Adult', 2.1, 'Carrion', 'Detritus', 'Detritus/Stock', 'Assemblage',
          '', '', '', '', '', None, None, 'Low', '', None, None, None, None, None, None,
          None, None, '', '', None, None, '', None, '', None, None, None, '', '', '',
          None, None],
         ['node_id', 'species_id', 'stage_id', 'stage', 'species_stageid', 'workingname',
          'organismalgroup', 'nodetype', 'resolution', 'resolutionnotes', 'feeding',
          'lifestylestage', 'lifestylespecies', 'consumerstrategystage', 'systems',
          'habitataffiliation', 'mobility', 'residency', 'nativestatus',
          'bodysize_g', 'bodysizeestimation', 'bodysizenotes', 'bodysizen',
          'biomass_kg_ha', 'biomassestimation', 'biomassnotes', 'kingdom', 'phylum',
          'subphylum', 'superclass', 'classes', 'subclass', 'ordered', 'suborder',
          'infraorder', 'superfamily', 'family', 'genus', 'specific_epithet', 'subspecies',
          'node_notes']
     ],
         'links': [
             [39, 79, 39, 79, 1, 1, 14, 'Concomitant Predation on Symbionts',
              None, None, None, None, None, None, None,
              None],
             ['consumernodeid', 'resourcenodeid', 'consumerspeciesid', 'resourcespeciesid',
              'consumerstageid', 'resourcestageid', 'linknumber', 'linktype', 'linkevidence',
              'linkevidencenotes', 'linkfrequency', 'linkn',
              'dietfraction', 'consumptionrate', 'vectorfrom', 'preyfrom']
         ]
     }])
]

fetch_order_tests = [
    ('acton-lake',
     ['ActonLakeDepth', 'ActonLakeIntegrated', 'StreamDischarge', 'StreamNutrients',
      'SiteCharacteristics']
     ),
    ('forest-plots-michigan',
     ['all_plots_1935_1948', 'all_plots_1974_1980', 'swamp', 'species_codes',
      'upland_plots_1989_2007', 'sampling_history']
     )
]

python_files = ['flensburg_food_web']


def setup_module():
    """Update retriever scripts and cd to test directory to find data."""
    os.chdir(retriever_root_dir)
    subprocess.call(['cp', '-r', 'test/raw_data', retriever_root_dir])


def teardown_module():
    """Cleanup temporary output files and return to root directory."""
    os.chdir(retriever_root_dir)
    shutil.rmtree(os.path.join(retriever_root_dir, 'raw_data'))
    subprocess.call(['rm', '-r', 'testdb_retriever.sqlite'])


def get_script_module(script_name):
    """Load a script module"""
    if script_name in python_files:
        file, pathname, desc = imp.find_module(script_name,
                                               [working_script_dir])
        return imp.load_module(script_name + '.py', file, pathname, desc)
    return read_json(os.path.join(retriever_root_dir, 'scripts', script_name))


def get_csv_md5(dataset, engine, tmpdir, install_function, config):
    workdir = tmpdir.mkdtemp()
    src = os.path.join(retriever_root_dir, 'scripts')
    dest = os.path.join(str(workdir), 'scripts')
    subprocess.call(['cp', '-r', src, dest])
    workdir.chdir()
    final_direct = os.getcwd()
    engine.script_table_registry = {}
    engine_obj = install_function(dataset.replace('_', '-'), **config)
    engine_obj.to_csv()
    # need to remove scripts before checking md5 on dir
    subprocess.call(['rm', '-r', 'scripts'])
    current_md5 = getmd5(data=final_direct, data_type='dir')
    os.chdir(retriever_root_dir)
    return current_md5


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_sqlite_regression(dataset, expected, tmpdir):
    """Check for sqlite regression."""
    subprocess.call(['rm', '-r', 'testdb_retriever.sqlite'])
    dbfile = 'testdb_retriever.sqlite'
    if os.path.exists(dbfile):
        subprocess.call(['rm', '-r', dbfile])
    # SQlite should install datasets into a different folder from where .csv are dumped
    # This avoids having the `testdb.sqlite` being considered for md5 sum
    sqlite_engine.opts = {
        'engine': 'sqlite',
        'file': dbfile,
        'table_name': '{db}_{table}',
        'data_dir': DATA_DIR}
    interface_opts = {'file': dbfile, 'data_dir': retriever_root_dir}
    assert get_csv_md5(dataset, sqlite_engine, tmpdir, install_sqlite, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_postgres_regression(dataset, expected, tmpdir):
    """Check for postgres regression."""
    cmd = 'psql -U postgres -d ' + testdb_retriever + ' -h ' + pgdb_host + ' -w -c \"DROP SCHEMA IF EXISTS ' + testschema + ' CASCADE\"'
    subprocess.call(shlex.split(cmd))
    postgres_engine.opts = {'engine': 'postgres',
                            'user': 'postgres',
                            'password': os_password,
                            'host': pgdb_host,
                            'port': 5432,
                            'database': testdb_retriever,
                            'database_name': testschema,
                            'table_name': '{db}.{table}'}
    interface_opts = {"user": 'postgres',
                      "password": postgres_engine.opts['password'],
                      'host': postgres_engine.opts['host'],
                      'port': postgres_engine.opts['port'],
                      "database": postgres_engine.opts['database'],
                      "database_name": postgres_engine.opts['database_name'],
                      "table_name": postgres_engine.opts['table_name']}
    assert get_csv_md5(dataset, postgres_engine, tmpdir, install_postgres, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_mysql_regression(dataset, expected, tmpdir):
    cmd = 'mysql -u travis -Bse "DROP DATABASE IF EXISTS {testdb_retriever}"'.format(testdb_retriever=testdb_retriever)
    subprocess.call(shlex.split(cmd))
    mysql_engine.opts = {'engine': 'mysql',
                         'user': 'travis',
                         'password': os_password,
                         'host': mysqldb_host,
                         'port': 3306,
                         'database_name': testdb_retriever,
                         'table_name': '{db}.{table}'}
    interface_opts = {"user": mysql_engine.opts['user'],
                      'password': mysql_engine.opts['password'],
                      'host': mysql_engine.opts['host'],
                      'port': mysql_engine.opts['port'],
                      "database_name": mysql_engine.opts['database_name'],
                      "table_name": mysql_engine.opts['table_name']}
    assert get_csv_md5(dataset, mysql_engine, tmpdir, install_mysql, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_xmlengine_regression(dataset, expected, tmpdir):
    """Check for xmlenginee regression."""
    xml_engine.opts = {
        'engine': 'xml',
        'table_name': '{db}_output_{table}.xml',
        'data_dir': DATA_DIR}
    interface_opts = {'table_name': '{db}_output_{table}.xml'}
    assert get_csv_md5(dataset, xml_engine, tmpdir, install_xml, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_jsonengine_regression(dataset, expected, tmpdir):
    """Check for jsonenginee regression."""
    json_engine.opts = {
        'engine': 'json',
        'table_name': '{db}_output_{table}.json',
        'data_dir': DATA_DIR}
    interface_opts = {'table_name': '{db}_output_{table}.json'}
    assert get_csv_md5(dataset, json_engine, tmpdir, install_json, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", db_md5)
def test_csv_regression(dataset, expected, tmpdir):
    """Check csv regression."""
    csv_engine.opts = {
        'engine': 'csv',
        'table_name': '{db}_output_{table}.csv',
        'data_dir': DATA_DIR}
    interface_opts = {'table_name': '{db}_output_{table}.csv'}
    assert get_csv_md5(dataset, csv_engine, tmpdir, install_csv, interface_opts) == expected


@pytest.mark.parametrize("dataset, expected", download_md5)
def test_download_regression(dataset, expected):
    """Test download regression."""
    os.chdir(retriever_root_dir)
    download(dataset, "raw_data/{0}".format(dataset))
    current_md5 = getmd5(data="raw_data/{0}".format(dataset), data_type='dir')
    assert current_md5 == expected


# @pytest.mark.parametrize("dataset, expected", fetch_tests)
def test_fetch():
    """Test fetch interface"""
    for dataset, expected in fetch_tests:
        data_frame = fetch(dataset)
        for itm in expected:
            for table_i in itm:
                expected_data = itm[table_i][0]
                expected_column_values = itm[table_i][1]
                column_values = list(data_frame[table_i].dtypes.index)
                first_row_data = list(data_frame[table_i].iloc[0])
                assert expected_data == first_row_data
                assert expected_column_values == column_values


def test_interface_table_registry():
    # Test if script_table_registry keeps only the latest
    # table names of the installed data packages in
    # script_table_registry
    install_csv("iris")
    wine_data = fetch("wine-composition")
    assert "iris" not in wine_data.keys()


@pytest.mark.parametrize("dataset, expected", fetch_order_tests)
def test_fetch_order(dataset, expected):
    """Test fetch dataframe order"""
    data_frame_dict = fetch(dataset)
    assert list(data_frame_dict.keys()) == expected
