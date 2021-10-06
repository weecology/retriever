# -*- coding: utf-8  -*-
"""Tests for the Data Retriever"""
import os
import random
import subprocess
from tqdm import tqdm

import pytest
import requests
import retriever as rt
from retriever.lib.cleanup import correct_invalid_value
from retriever.lib.engine import Engine
from retriever.lib.engine_tools import getmd5
from retriever.lib.engine_tools import json2csv
from retriever.lib.engine_tools import xml2csv_test
from retriever.lib.table import TabularDataset
from retriever.lib.templates import BasicTextTemplate

try:
    from retriever.lib.engine_tools import geojson2csv
except ModuleNotFoundError:
    pass

from retriever.lib.engine_tools import sqlite2csv
from retriever.lib.engine_tools import sort_file
from retriever.lib.engine_tools import sort_csv
from retriever.lib.engine_tools import create_file
from retriever.lib.engine_tools import file_2list
from retriever.lib.datapackage import clean_input, is_empty
from retriever.lib.defaults import HOME_DIR, RETRIEVER_DATASETS, RETRIEVER_REPOSITORY, KAGGLE_TOKEN_PATH

# Create simple engine fixture
test_engine = Engine()
test_engine.table = TabularDataset(**{"name": "test"})
test_engine.script = BasicTextTemplate(
    **{"tables": test_engine.table, "name": "test"})
test_engine.opts = {'database_name': '{db}_abc'}

geojson2csv_dataset = [
    ("simple_geojson2csv", "lake_county.geojson", "http://data-lakecountyil.opendata.arcgis.com/datasets/cd63911cc52841f38b289aeeeff0f300_1.geojson", 'fid,zip,colorectal,lung_bronc,breast_can,prostate_c,urinary_sy,all_cancer,shape_length,shape_area,geometry')
]

sqlite2csv_dataset = [
    ("simple_sqlite2csv", "portal_project.sqlite", "https://ndownloader.figshare.com/files/11188550", "plots", ['plot_id,plot_type'])
]

json2csv_datasets = [
    # test_name, json_data, header_values, row_key, expected
    ("simple_json", ["""{"User": "Alex", "Country": "US", "Age": "25"}"""], ['User','Country','Age'], None, ['user,country,age', 'Alex,US,25']),
    ("nested_json", ["""{"prizes":[{"year":"2019","category":"chemistry","laureates":[{"id":"976","firstname":"John","surname":"Goodenough","motivation":"text shorted","share":"3"}]}]}"""], ["id", "firstname", "surname", "motivation", "share"], 'prizes', ['id,firstname,surname,motivation,share', '976,John,Goodenough,text shorted,3']),
    ("null_data_json", ["""[{"User":"Alex","id":"US1","Age":"25","kt":"2.0","qt":"1.00"},{"User":"Tom","id":"US2","Age":"20","kt":"0.0","qt":"1.0"},{"User":"Dan","id":"44","Age":"2","kt":"0","qt":"1"},{"User":"Kim","id":"654","Age":"","kt":"","qt":""}]"""], ["User", "id", "Age", "kt", "qt"], None, ['User,id,Age,kt,qt', 'Alex,US1,25,2.0,1.00', 'Tom,US2,20,0.0,1.0', 'Dan,44,2,0,1', 'Kim,654,,,'])
]

xml2csv_dataset = [
    ("simple_xml", ["""<root><row><User>Alex</User><Country>US</Country><Age>25</Age></row><row><User>Ben</User><Country>US</Country><Age>24</Age></row></root>"""], ["User", "Country", "Age"], 1, ['User,Country,Age', 'Alex,US,25', 'Ben,US,24'])
]

# Main paths
HOMEDIR = os.path.expanduser('~')
file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))

# Setup paths for the raw data files used
raw_dir_files = os.path.normpath(os.path.join(retriever_root_dir,
                                              'raw_data/{file_name}'))
# file: sample_zip.csv
achive_zip = raw_dir_files.format(file_name='sample_zip.zip')

# file: test/sample_tar.csv
achive_tar = raw_dir_files.format(file_name='sample_tar.tar')
achive_tar_gz = raw_dir_files.format(file_name='sample_tar.tar.gz')
achive_gz = raw_dir_files.format(file_name='sample.gz')

# Setup urls for downloading raw data from the test/raw_data directory

achive_url = """file://{loc}/raw_data/""" \
    .format(loc=file_location) + '{file_path}'

zip_url = os.path.normpath(achive_url.format(file_path='sample_zip.zip'))
tar_url = os.path.normpath(achive_url.format(file_path='sample_tar.tar'))
tar_gz_url = os.path.normpath(achive_url.format(file_path='sample_tar.tar.gz'))
gz_url = os.path.normpath(achive_url.format(file_path='sample.gz'))

clinic_utah = {
    "archived": "fill or remove this field if not archived",
    "citation": "fill",
    "description": "fill",
    "encoding": "utf-8",
    "homepage": "fill",
    "keywords": [],
    "licenses": [],
    "name": "fill",
    "resources": [
        {
            "name": "35s3_nmpm",
            "path": "35s3-nmpm.csv",
            "url": "fill"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "2.1.0",
    "title": "fill",
    "version": "1.0.0"
}

updated_clinic_utah = {
    "citation": "",
    "description": "This data set includes comparative information for clinics with five or more physicians for medical claims in 2015 - 2016. \r\n\r\nThis data set was calculated by the Utah Department of Health, Office of Healthcare Statistics (OHCS) using Utah\u2019s All Payer Claims Database (APCD).",
    "encoding": "utf-8",
    "homepage": "https://opendata.utah.gov/Health/2016-2015-Clinic-Quality-Comparisons-for-Clinics-w/35s3-nmpm",
    "keywords": ["health","socrata"],
    "licenses": [{"name": "Public Domain"}],
    "name": "clinic-35s3",
    "resources": [
        {
            "name": "clinic_35s3",
            "url": "https://opendata.utah.gov/resource/35s3-nmpm.csv"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "3.0.1-dev",
    "socrata": "True",
    "title": "2016 & 2015 Clinic Quality Comparisons for Clinics with Five or More Service Providers",
    "version": "1.0.0"
}

fish_utah = {
    "archived": "fill or remove this field if not archived",
    "citation": "fill",
    "description": "fill",
    "encoding": "utf-8",
    "homepage": "fill",
    "keywords": [],
    "licenses": [],
    "name": "fill",
    "resources": [
        {
            "name": "9m7z-mzh9",
            "path": "9m7z-mzh9.csv",
            "url": "fill"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "2.1.0",
    "title": "fill",
    "version": "1.0.0"
}

updated_fish_utah = {
    "citation": "",
    "description": "Utah Fish Stocking Report 2013",
    "encoding": "utf-8",
    "homepage": "https://opendata.utah.gov/Recreation/Fish-Stocked-in-Utah-by-Species/9m7z-mzh9",
    "keywords": ["socrata"],
    "licenses": [{"name": "Public Domain"}],
    "name": "fish-stock-utah",
    "resources": [
        {
            "name": "fish_stock_utah",
            "url": "https://opendata.utah.gov/resource/9m7z-mzh9.csv"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "3.0.1-dev",
    "socrata": "True",
    "title": "Fish Stocked in Utah by Species",
    "version": "1.0.0"
}

affairs_json = {
    "archived": "fill or remove this field if not archived",
    "citation": "fill",
    "description": "fill",
    "encoding": "utf-8",
    "homepage": "fill",
    "keywords": [],
    "licenses": [],
    "name": "fill",
    "resources": [
        {
            "name": "affairs",
            "path": "Affairs.csv",
            "url": "fill"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "2.1.0",
    "title": "fill",
    "version": "1.0.0"
}

updated_affairs_json = {
    "citation": "",
    "description": "This is a rdataset from aer",
    "encoding": "utf-8",
    "homepage": "https://vincentarelbundock.github.io/Rdatasets/doc/AER/Affairs.html",
    "keywords": ["rdataset","affairs","aer"],
    "licenses": [{"name": "Public Domain"}],
    "name": "rdataset-aer-affairs",
    "package": "aer",
    "rdatasets": "True",
    "resources": [
        {
            "name": "affairs",
            "url": "https://vincentarelbundock.github.io/Rdatasets/csv/AER/Affairs.csv"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "3.0.1-dev",
    "title": "Fair's Extramarital Affairs Data",
    "version": "1.0.0"
}

kaggle_datasets = [
    # test_name, data_source, dataset_identifier, dataset_name, repath, expected
    ("kaggle_competition", "competition", "titanic", "titanic", ["gender_submission.csv",  "test.csv", "train.csv"]),
    ("kaggle_unknown", "dataset", "uciml/iris", "iris", ['Iris.csv', 'database.sqlite']),
    ("kaggle_dataset", "competition", "non_existent_dataset", "non_existent_dataset", []),
]

socrata_datasets = [
    # test_name, filename, url, path, expected
    ("utah_clinic_pass", "35s3-nmpm.csv", "https://opendata.utah.gov/resource/35s3-nmpm.csv", True),
    ("utah_clinic_fail", "35s3-nmpm.csv", "https://opendata.utah.gov/resource/35s3nmpm", False),
    ("utah_fish_pass", "9m7z-mzh9.csv", "https://opendata.utah.gov/resource/9m7z-mzh9.csv", True),
    ("wa_patrol_fail", "iakd-awbx.csv", "https://data.auburnwa.gov/resource/iakd-awbx.csv", False),
]

update_socrata_datasets = [
    # test_name, id, json_file, script_name, url, expected
    ('utah_clinic_pass','35s3-nmpm', clinic_utah, 'clinic-35s3', "https://opendata.utah.gov/resource/35s3-nmpm.csv", [True, updated_clinic_utah]),
    ('utah_fish_pass','9m7z-mzh9', fish_utah, 'fish-stock-utah', "https://opendata.utah.gov/resource/9m7z-mzh9.csv", [True, updated_fish_utah]),
    ('utah_fish_fail','9m7z-mzh8', fish_utah, 'fish-stock-utah', "https://opendata.utah.gov/resource/9m7z-mzh9.csv", [False, None]),
]

update_rdatasets = [
    # test_name, package, dataset_name, json_file, expected
    ('affairs_pass', 'aer', 'affairs', affairs_json, [True, updated_affairs_json]),
    ('affairs_fail', 'aer', 'affairs', affairs_json, [False, None]),
]

def setup_module():
    """"Automatically sets up the environment before the module runs.

    Make sure you are in the main local retriever directory.
    """
    os.chdir(retriever_root_dir)
    subprocess.call(['cp', '-r', 'test/raw_data', retriever_root_dir])


def teardown_module():
    """Automatically clean up after the module.

    Make sure you are in the main local retriever directory after these tests.
    """
    os.chdir(retriever_root_dir)
    subprocess.call(['rm', '-r', 'raw_data'])
    subprocess.call(['rm', '-r', test_engine.format_data_dir()])


def setup_functions():
    """Set up function.

    Tests can use the function to clean up before running.
    Not automatically run.
    """
    teardown_module()
    setup_module()


def test_auto_get_columns():
    """Basic test of getting column labels from header."""
    test_engine.table.delimiter = ","
    columns, _ = test_engine.table.auto_get_columns(
        ['a', 'b', 'c', 'd'])
    assert columns == [['a', None], ['b', None], ['c', None], ['d', None]]


def test_auto_get_datatypes():
    """Test the length detected by auto_get_datatype.

    The function adds 100 to the auto detected length of column
    """
    test_engine.auto_get_datatypes(None,
                                   [["ö", 'bb', 'Löve']],
                                   [['a', None], ['b', None], ['c', None]])
    length = test_engine.table.columns
    # encoded char "?" will return 2 in length
    assert [length[0][1][1], length[1][1][1], length[2][1][1]] == \
           [2, 2, 5]


def test_auto_get_columns_extra_whitespace():
    """Test getting column labels from header with extra whitespace."""
    test_engine.table.delimiter = ","
    columns, _ = test_engine.table.auto_get_columns(
        ['a', 'b', 'c', 'd  '])
    assert columns == [['a', None], ['b', None], ['c', None], ['d', None]]


def test_auto_get_columns_cleanup():
    """Test of automatically cleaning up column labels from header."""
    test_engine.table.delimiter = ","
    columns, _ = test_engine.table.auto_get_columns([
        'a)', 'a\nd', 'b.b', 'c/c', 'd___d', 'group'])

    assert columns == [['a', None],
                       ['ad', None],
                       ['b_b', None],
                       ['c_c', None],
                       ['d_d', None],
                       ['grp', None]]


def test_auto_get_delimiter_comma():
    """Test if commas are properly detected as delimiter."""
    test_engine.auto_get_delimiter("a,b,c;,d")
    assert test_engine.table.delimiter == ","


def test_auto_get_delimiter_tab():
    """Test if commas are properly detected as delimiter."""
    test_engine.auto_get_delimiter("a\tb\tc\td,")
    assert test_engine.table.delimiter == "\t"


def test_auto_get_delimiter_semicolon():
    """Test if semicolons are properly detected as delimiter."""
    test_engine.auto_get_delimiter("a;b;c;,d")
    assert test_engine.table.delimiter == ";"


def test_correct_invalid_value_string():
    assert \
        correct_invalid_value('NA', {'missingValues': ['NA', '-999']}) is None


def test_correct_invalid_value_number():
    assert \
        correct_invalid_value(-999, {'missingValues': ['NA', '-999']}) is None


def test_correct_invalid_value_exception():
    assert correct_invalid_value(-999, {}) == -999


def test_create_db_statement():
    """Test creating the create database SQL statement."""
    assert test_engine.create_db_statement() == 'CREATE DATABASE test_abc'


def test_database_name():
    """Test creating database name."""
    assert test_engine.database_name() == 'test_abc'


def test_datasets():
    """Check if datasets lookup includes a known value"""
    datasets = rt.datasets(keywords=['mammals'])
    dataset_names = [dataset.name for dataset in datasets['offline']]
    dataset_names.extend(datasets['online'])
    assert 'mammal-masses' in dataset_names


def test_datasets_keywords():
    """Check if datasets lookup on keyword includes a known value"""
    datasets = rt.datasets(keywords=['mammals'])
    dataset_names = [dataset.name for dataset in datasets['offline']]
    dataset_names.extend(datasets['online'])
    assert 'mammal-masses' in dataset_names


def test_datasets_licenses():
    """Check if datasets lookup on license includes a known value"""
    datasets = rt.datasets(licenses=['CC0-1.0'])
    dataset_names = [dataset.name for dataset in datasets['offline']]
    dataset_names.extend(datasets['online'])
    assert 'amniote-life-hist' in dataset_names


def test_dataset_names():
    """Check if dataset names lookup includes a known value"""
    datasets = rt.dataset_names()
    dataset_names = datasets['offline']
    dataset_names.extend(datasets['online'])
    assert 'mammal-masses' in dataset_names


def test_dataset_names_upstream():
    """Check if upstream datasets include a known value"""
    datasets = rt.get_dataset_names_upstream()
    assert 'portal' in datasets
    license_datasets = rt.get_dataset_names_upstream(licenses=['CC0-1.0'])
    assert 'bird-size' in license_datasets
    keyword_datasets = rt.get_dataset_names_upstream(keywords=['plants'])
    assert 'biodiversity-response' in keyword_datasets


def test_socrata_autocomplete_search():
    """Check if autocomplete search returns a list of names or not"""
    names = rt.socrata_autocomplete_search(["building", "permits"])
    assert isinstance(names, list) and (len(names) != 0)
    names = rt.socrata_autocomplete_search([" "])
    assert isinstance(names, list) and (len(names) == 0)
    names = rt.socrata_autocomplete_search(["fshing"])
    assert isinstance(names, list) and (len(names) == 0)


def test_socrata_dataset_info():
    """Check if socrata dataset info returns metadata for a dataset name"""
    resource = rt.socrata_dataset_info("Building Permits")
    assert all([isinstance(resource, list), len(resource), resource[0]["id"]])
    resource = rt.socrata_dataset_info(" ")
    assert isinstance(resource, list) and (len(resource) == 0)
    resource = rt.socrata_dataset_info("Cook County - Fishing Lakes")
    assert all([isinstance(resource, list), len(resource), resource[0]["id"]])


def test_find_socrata_dataset_by_id():
    """Check if find socrata dataset by id returns metadata for a dataset id"""
    resource = rt.find_socrata_dataset_by_id("35s3-nmpm")
    assert isinstance(resource, dict) and ("error" not in resource.keys())
    resource = rt.find_socrata_dataset_by_id("35s3-Nmpm")
    assert isinstance(resource, dict) and (len(resource.keys()) == 0)
    resource = rt.find_socrata_dataset_by_id("abcde-12345")
    assert isinstance(resource, dict) and (len(resource.keys()) == 0)
    resource = rt.find_socrata_dataset_by_id("abcd-1234")
    assert isinstance(resource, dict) and (len(resource.keys()) == 0)
    resource = rt.find_socrata_dataset_by_id("nawu-wcvv")
    assert isinstance(resource, dict) and ("error" in resource.keys())


def test_update_rdataset_catalog():
    """Checks if update_rdataset_catalog creates a correct dict object or not"""
    rdatasets = rt.update_rdataset_catalog(test=True)
    assert isinstance(rdatasets, dict)
    assert isinstance(rdatasets['aer'], dict)
    assert isinstance(rdatasets['aer']['affairs'], dict)
    keys = ['csv', 'doc', 'title']
    assert all([True for key in keys if key in rdatasets['aer']['affairs']])


def test_get_rdataset_names():
    """Checks if get_rdataset_names returns a list of script names and if the script names are correct"""
    script_names = rt.get_rdataset_names()
    assert isinstance(script_names, list)
    assert len(script_names)
    assert (len(script_names[0].split('-')) == 3) and script_names[0].startswith('rdataset')


@pytest.mark.parametrize("test_name, package, dataset_name, json_file, expected", update_rdatasets)
def test_update_rdataset_contents(test_name, package, dataset_name, json_file, expected):
    """Checks if the update_rdataset_contents function updates the contents correctly"""
    rdatasets = rt.update_rdataset_catalog(test=True)
    if test_name == 'affairs_fail':
        data_obj = {'xyz': 'abc'}
    else:
        data_obj = rdatasets[package][dataset_name]
    result, updated_json = rt.update_rdataset_contents(data_obj, package, dataset_name, json_file)
    assert (result == expected[0]) and (updated_json == expected[1])


@pytest.mark.parametrize("test_name, id, json_file, script_name, url, expected", update_socrata_datasets)
def test_update_socrata_contents(test_name, id, json_file, script_name, url, expected):
    """Checks if the update socrata script updates the default script contents"""
    resource = rt.find_socrata_dataset_by_id(id)
    result, updated_json = rt.update_socrata_contents(json_file, script_name, url, resource)
    assert (result == expected[0]) and (updated_json == expected[1])


def test_drop_statement():
    """Test the creation of drop statements."""
    assert test_engine.drop_statement(
        'TABLE', 'tablename') == "DROP TABLE IF EXISTS tablename"


@pytest.mark.parametrize("test_name, data_source, dataset_identifier,  repath, expected", kaggle_datasets)
def test_download_kaggle_dataset(test_name, data_source, dataset_identifier,  repath, expected):
    """Test the downloading of dataset from kaggle."""
    setup_functions()
    files = test_engine.download_from_kaggle(
        data_source=data_source,
        dataset_name=dataset_identifier,
        archive_dir=raw_dir_files,
        archive_full_path=os.path.join(raw_dir_files, repath)
    )

    kaggle_token = os.path.isfile(KAGGLE_TOKEN_PATH)
    kaggle_username = os.getenv('KAGGLE_USERNAME', "").strip()
    kaggle_key = os.getenv('KAGGLE_KEY', "").strip()
    if kaggle_token or (kaggle_username and kaggle_key):
        assert files == expected
    else:
        assert files == None


@pytest.mark.parametrize("test_name, filename, url, expected", socrata_datasets)
def test_download_socrata_dataset(test_name, filename, url, expected):
    """Test the downloading of dataset from socrata"""
    setup_functions()
    path = os.path.normpath(raw_dir_files.format(file_name=filename))
    progbar = tqdm(
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                miniters=1,
                desc='Downloading {}'.format(filename),
            )
    result = test_engine.download_from_socrata(url, path, progbar)
    progbar.close()
    assert (result == expected) and (os.path.exists(path) == expected)


def test_download_archive_gz_known():
    """Download and extract known files

    from a gzipped file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(
        url=gz_url, file_names=['test/sample_tar.csv'], archive_type='gz')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_gz_unknown():
    """Download and extract unknown files

    from a gzipped file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=gz_url,
                                                    archive_type='gz')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_targz_known():
    """Download and extract known files

    from a targzipped file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=tar_gz_url,
                                                    file_names=['test/sample_tar.csv'],
                                                    archive_type='tar.gz')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_targz_unknown():
    """Download and extract unknown files

    from a targzipped file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=tar_gz_url,
                                                    archive_type='tar.gz')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_tar_known():
    """Download and extract known files

    from a tarred file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(
        url=tar_url,
        file_names=['test/sample_tar.csv'],
        archive_type='tar')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_tar_unknown():
    """Download and extract unknown files

    from a tarred file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=tar_url,
                                                    archive_type='tar')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_zip_known():
    """Download and extract known files

    from a zipped file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=zip_url,
                                                    file_names=['sample_zip.csv'],
                                                    archive_type='zip')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/sample_zip.csv'))
    assert r_path == test_engine.find_file('sample_zip.csv')
    assert ['sample_zip.csv'] <= files


def test_download_archive_zip_unkown():
    """Download and extract unknown files

    from a zipped file to the .retriever/data dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=zip_url,
                                                    archive_type='zip')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/sample_zip.csv'))
    assert r_path == test_engine.find_file('sample_zip.csv')
    assert ['sample_zip.csv'] <= files


def test_extract_known_tar():
    """Test extraction of known tarred filename"""
    setup_functions()
    archivedir_write_path = raw_dir_files.format(file_name="")
    expected = test_engine.extract_tar(achive_tar,
                                       archivedir_write_path,
                                       archive_type="tar",
                                       file_name='test/sample_tar.csv')
    assert ['test/sample_tar.csv'] == expected
    assert os.path.exists(
        raw_dir_files.format(file_name='test/sample_tar.csv'))


def test_extract_unknown_tar():
    """Test extraction of unknown tarred filename"""
    setup_functions()
    archivedir_write_path = raw_dir_files.format(file_name="")
    expected = test_engine.extract_tar(achive_tar,
                                       archivedir_write_path,
                                       archive_type='tar',
                                       file_name=None)
    assert ['test/sample_tar.csv'] == expected
    assert os.path.exists(
        raw_dir_files.format(file_name='test/sample_tar.csv'))


def test_extract_known_zip():
    """Test extraction of known zipped filename"""
    setup_functions()
    zip_known = raw_dir_files.format(file_name='zip_known')
    expected = test_engine.extract_zip(achive_zip,
                                       archivedir_write_path=zip_known,
                                       file_name='sample_zip.csv')

    assert ['sample_zip.csv'] == expected
    assert os.path.exists(os.path.join(
        raw_dir_files.format(file_name='zip_known'), 'sample_zip.csv'))
    os.system("rm -r {}".format(zip_known))


def test_extract_unknown_zip():
    """Test extraction of unknown zipped filename"""
    setup_functions()
    zip_unknown = raw_dir_files.format(file_name='zip_unknown')
    expected = test_engine.extract_zip(achive_zip,
                                       archivedir_write_path=zip_unknown)
    assert ['sample_zip.csv'] == expected
    assert os.path.exists(os.path.join(raw_dir_files.format(
        file_name='zip_unknown'), 'sample_zip.csv'))
    os.system('rm -r {}'.format(zip_unknown))


def test_extract_unknown_targz():
    """Test extraction of unknown tarred filename"""
    setup_functions()
    archivedir_write_path = raw_dir_files.format(file_name="")
    expected = test_engine.extract_tar(achive_tar_gz,
                                       archivedir_write_path,
                                       archive_type='tar.gz',
                                       file_name=None)
    assert ['test/sample_tar.csv'] == expected
    assert os.path.exists(
        raw_dir_files.format(file_name='test/sample_tar.csv'))


def test_extract_known_targz():
    """Test extraction of known tarred filename"""
    setup_functions()
    archivedir_write_path = raw_dir_files.format(file_name="")
    expected = test_engine.extract_tar(achive_tar_gz,
                                       archivedir_write_path,
                                       archive_type='tar.gz',
                                       file_name='test/sample_tar.csv')
    assert ['test/sample_tar.csv'] == expected
    assert os.path.exists(
        raw_dir_files.format(file_name='test/sample_tar.csv'))


def test_extract_known_gz():
    """Test extraction of known gzipped filename"""
    setup_functions()
    archivedir_write_path = raw_dir_files.format(file_name="")
    expected = test_engine.extract_gz(achive_gz,
                                      archivedir_write_path,
                                      file_name='test/sample_tar.csv')
    assert ['test/sample_tar.csv'] == expected
    assert os.path.exists(
        raw_dir_files.format(file_name='test/sample_tar.csv'))


def test_extract_unknown_gz():
    """Test extraction of unknown gzipped filename"""
    setup_functions()
    archivedir_write_path = raw_dir_files.format(file_name="")
    expected = test_engine.extract_gz(achive_gz,
                                      archivedir_write_path,
                                      file_name=None)
    expected = [os.path.normpath(file_name)
                for file_name in expected]
    assert [os.path.normpath('test/sample_tar.csv')] == expected
    assert os.path.exists(
        raw_dir_files.format(file_name='test/sample_tar.csv'))


def test_extract_values_fixed_width():
    """Test extraction of values from line of fixed width data."""
    test_engine.table.fixed_width = [5, 2, 2, 3, 4]
    assert test_engine.extract_fixed_width('abc  1 2 3  def ') == [
        'abc', '1', '2', '3', 'def']


def test_find_file_absent():
    """Test if find_file() properly returns false if no file is present."""
    assert test_engine.find_file('missingfile.txt') is False


def test_find_file_present():
    """Test if existing datafile is found.

    Using the bird-size dataset which is included for regression testing.
    We copy the raw_data directory to retriever_root_dir
    which is the current working directory.
    This enables the data to be in the DATA_SEARCH_PATHS.
    """
    test_engine.script.name = 'bird-size'
    assert test_engine.find_file('5599229') == os.path.normpath(
        'raw_data/bird-size/5599229')


def test_format_data_dir():
    """Test if directory for storing data is properly formated."""
    test_engine.script.name = "TestName"
    r_path = '.retriever/raw_data/TestName'
    assert os.path.normpath(test_engine.format_data_dir()) == \
           os.path.normpath(os.path.join(HOMEDIR, r_path))


def test_format_filename():
    """Test if filenames for stored files are properly formated."""
    test_engine.script.name = "TestName"
    r_path = '.retriever/raw_data/TestName/testfile.csv'
    assert os.path.normpath(test_engine.format_filename('testfile.csv')) == \
           os.path.normpath(os.path.join(HOMEDIR, r_path))


def test_format_insert_value_int():
    """Test formatting of values for insert statements."""
    assert test_engine.format_insert_value(42, 'int') == 42


def test_format_insert_value_double():
    """Test formatting of values for insert statements."""
    assert test_engine.format_insert_value(26.22, 'double') == 26.22


def test_format_insert_value_string_simple():
    """Test formatting of values for insert statements."""
    test_str = "simple text"
    assert test_engine.format_insert_value(test_str, 'char') == test_str


def test_format_insert_value_string_complex():
    """Test formatting of values for insert statements."""
    test_str = 'my notes: "have extra, stuff"'
    assert test_engine.format_insert_value(test_str, 'char') == test_str


def test_get_retriever_citation():
    citation = rt.get_retriever_citation()
    sub_str = "The EcoData Retriever: Improving Access to Existing Ecological Data"
    assert sub_str.lower() in citation.lower()


def test_get_script_citation():
    """Test get citation of a script"""
    cite = rt.get_script_citation("iris")
    expected_cite = "R. A. Fisher. 1936."
    assert expected_cite.lower() in cite[0].lower()

def test_getmd5_lines():
    """Test md5 sum calculation given a line."""
    lines = ['a,b,c', '1,2,3', '4,5,6']
    exp_hash = 'ca471abda3ebd4ae8ce1b0814b8f470c'
    assert getmd5(data=lines, data_type='lines') == exp_hash


def test_getmd5_line_end():
    """Test md5 sum calculation given a line with end of line character."""
    lines_end = ['a,b,c\n', '1,2,3\n', '4,5,6\n']
    exp_hash = '0bec5bf6f93c547bc9c6774acaf85e1a'
    assert getmd5(data=lines_end, data_type='lines') == exp_hash


def test_getmd5_path():
    """Test md5 sum calculation given a path to data source."""
    data_file = create_file(['a,b,c', '1,2,3', '4,5,6'])
    exp_hash = '0bec5bf6f93c547bc9c6774acaf85e1a'
    assert getmd5(data=data_file, data_type='file') == exp_hash


@pytest.mark.parametrize("test_name, json_data, header_values, row_key, expected", json2csv_datasets)
def test_json2csv(test_name, json_data, header_values, row_key, expected):
    """Test json2csv function.

    Creates a json file and tests the md5 sum calculation.
    """
    json_file = create_file(json_data, 'output.json')
    output_json = json2csv(json_file, "output_json.csv",
                           header_values=header_values,
                           row_key=row_key)
    obs_out = file_2list(output_json)
    os.remove(output_json)
    assert obs_out == expected


@pytest.mark.parametrize("test_name, table_name, geojson_data_url, expected", geojson2csv_dataset)
def test_geojson2csv(test_name, table_name, geojson_data_url, expected):
    if not os.environ.get("CI"):
        r = requests.get(geojson_data_url, allow_redirects=True)
        open(table_name, 'wb').write(r.content)
        output_geojson = geojson2csv(table_name, "output_file_geojson.csv", encoding=test_engine.encoding)
        header_val = None
        with open(output_geojson, 'r') as fh:
            header_val = fh.readline().split()
        header_val = header_val[0].lower()
        os.remove(output_geojson)
        os.remove(table_name)
        assert header_val == expected

@pytest.mark.parametrize("test_name, db_name, sqlite_data_url, table_name, expected", sqlite2csv_dataset)
def test_sqlite2csv(test_name, db_name, sqlite_data_url, table_name, expected):
    r = requests.get(sqlite_data_url, allow_redirects=True)
    open(db_name, 'wb').write(r.content)
    output_sqlite = sqlite2csv(db_name, "output_file_sqlite.csv", table_name, encoding=test_engine.encoding)
    header_val = None
    with open(output_sqlite, 'r') as fh:
        header_val = fh.readline().split()
    os.remove(output_sqlite)
    os.remove(db_name)
    assert header_val == expected

@pytest.mark.parametrize("test_name, xml_data, header_values, empty_rows, expected", xml2csv_dataset)
def test_xml2csv(test_name, xml_data, header_values, empty_rows, expected):
    """Test xml2csv function.

    Creates a xml file and tests the md5 sum calculation.
    """
    xml_file = create_file(xml_data, 'output.xml')
    input_file = xml_file
    outputfile = "output_xml.csv"

    output_xml = xml2csv_test(input_file, outputfile, header_values, row_tag="row")

    obs_out = file_2list(output_xml)
    os.remove(output_xml)
    assert obs_out == expected


def test_sort_file():
    """Test md5 sum calculation."""
    data_file = create_file(['Ben,US,24', 'Alex,US,25', 'Alex,PT,25'])
    out_file = sort_file(data_file)
    obs_out = file_2list(out_file)
    os.remove(out_file)
    assert obs_out == ['Alex,PT,25', 'Alex,US,25', 'Ben,US,24']


def test_sort_csv():
    """Test md5 sum calculation."""
    data_file = create_file(['User,Country,Age',
                             'Ben,US,24',
                             'Alex,US,25',
                             'Alex,PT,25'])
    out_file = sort_csv(data_file)
    obs_out = file_2list(out_file)
    os.remove(out_file)
    assert obs_out == [
        'User,Country,Age',
        'Alex,PT,25',
        'Alex,US,25',
        'Ben,US,24']


def test_is_empty_null_string():
    """Test for null string."""
    assert is_empty("")


def test_is_empty_empty_list():
    """Test for empty list."""
    assert is_empty([])


def test_is_empty_not_null_string():
    """Test for non-null string."""
    assert is_empty("not empty") == False


def test_is_empty_not_empty_list():
    """Test for not empty list."""
    assert is_empty(["not empty"]) == False


def test_clean_input_empty_input_ignore_empty(monkeypatch):
    """Test with empty input ignored."""

    def mock_input(prompt):
        return ""

    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("", ignore_empty=True) == ""


def test_clean_input_empty_input_not_ignore_empty(monkeypatch):
    """Test with empty input not ignored."""

    def mock_input(prompt):
        mock_input.counter += 1
        if mock_input.counter <= 1:
            return ""
        else:
            return "not empty"

    mock_input.counter = 0
    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("", ignore_empty=False) == "not empty"


def test_clean_input_string_input(monkeypatch):
    """Test with non-empty input."""

    def mock_input(prompt):
        return "not empty"

    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("") == "not empty"


def test_clean_input_empty_list_ignore_empty(monkeypatch):
    """Test with empty list ignored."""

    def mock_input(prompt):
        return ",  ,   ,"

    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("", ignore_empty=True, split_char=",") == []


def test_clean_input_empty_list_not_ignore_empty(monkeypatch):
    """Test with empty list not ignored."""

    def mock_input(prompt):
        mock_input.counter += 1
        if mock_input.counter <= 1:
            return ",  ,   ,"
        else:
            return "1  ,    2,  3,"

    mock_input.counter = 0
    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("", split_char=",") == ["1", "2", "3"]


def test_clean_input_not_empty_list(monkeypatch):
    """Test with list input."""

    def mock_input(prompt):
        return "1,    2,     3"

    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("", ignore_empty=True, split_char=',', dtype=None) == \
           ["1", "2", "3"]


def test_clean_input_bool(monkeypatch):
    """Test with correct datatype input."""

    def mock_input(prompt):
        return "True "

    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("", dtype=bool) == "True"


def test_clean_input_not_bool(monkeypatch):
    """Test with incorrect datatype input."""

    def mock_input(prompt):
        mock_input.counter += 1
        if mock_input.counter <= 1:
            return "non bool input"
        else:
            return "True "

    mock_input.counter = 0
    monkeypatch.setattr('retriever.lib.datapackage.input', mock_input)
    assert clean_input("", dtype=bool) == "True"


def test_reset_retriever(tmpdir):
    """Test the dataset reset function."""

    pwd_name = os.getcwd()
    workdir = tmpdir.mkdtemp()
    workdir.chdir()
    offline_datasets = rt.dataset_names()['offline']
    offline_datasets = [dataset for dataset in offline_datasets if not dataset.startswith('test-')]
    if not offline_datasets:
        return
    dataset = random.choice(offline_datasets)
    rt.reset_retriever(dataset)
    rt.reload_scripts()
    assert os.path.exists(os.path.join(HOME_DIR, dataset.replace("-", "_") + ".json")) == False
    assert os.path.exists(os.path.join(HOME_DIR, dataset.replace("-", "_") + ".py")) == False
    if dataset in RETRIEVER_DATASETS:
        rt.get_script_upstream(dataset, repo=RETRIEVER_REPOSITORY)
    else:
        rt.get_script_upstream(dataset)
    rt.reload_scripts()
    assert dataset in rt.dataset_names()['offline']
    os.chdir(pwd_name)


def test_setup_functions():
    """Test the set up function.

    Function uses teardown_module and setup_module functions."""
    file_path = raw_dir_files.format(file_name='')
    subprocess.call(['rm', '-r', file_path])
    assert os.path.exists(raw_dir_files.format(file_name="")) is False
    setup_functions()
    assert os.path.exists(raw_dir_files.format(file_name=""))
