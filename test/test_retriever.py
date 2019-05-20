# -*- coding: latin-1  -*-
"""Tests for the Data Retriever"""
from future import standard_library

standard_library.install_aliases()
import os
import subprocess
import random

import retriever as rt
from retriever.lib.engine import Engine
from retriever.lib.table import TabularDataset
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.cleanup import correct_invalid_value
from retriever.lib.engine_tools import getmd5
from retriever.lib.engine_tools import xml2csv
from retriever.lib.engine_tools import json2csv
from retriever.lib.engine_tools import sort_file
from retriever.lib.engine_tools import sort_csv
from retriever.lib.engine_tools import create_file
from retriever.lib.engine_tools import file_2list
from retriever.lib.datapackage import clean_input, is_empty

# Create simple engine fixture
test_engine = Engine()
test_engine.table = TabularDataset(**{"name": "test"})
test_engine.script = BasicTextTemplate(
    **{"tables": test_engine.table, "name": "test"})
test_engine.opts = {'database_name': '{db}_abc'}

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
    assert [length[0][1][1], length[1][1][1], length[2][1][1]] == \
           [101, 102, 104]


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
    dataset_names = [dataset.name for dataset in datasets]
    assert 'mammal-masses' in dataset_names


def test_datasets_keywords():
    """Check if datasets lookup on keyword includes a known value"""
    datasets = rt.datasets(keywords=['mammals'])
    dataset_names = [dataset.name for dataset in datasets]
    assert 'mammal-masses' in dataset_names


def test_datasets_licenses():
    """Check if datasets lookup on license includes a known value"""
    datasets = rt.datasets(licenses=['CC0-1.0'])
    dataset_names = [dataset.name for dataset in datasets]
    assert 'amniote-life-hist' in dataset_names


def test_dataset_names():
    """Check if dataset names lookup includes a known value"""
    assert 'mammal-masses' in rt.dataset_names()


def test_drop_statement():
    """Test the creation of drop statements."""
    assert test_engine.drop_statement(
        'TABLE', 'tablename') == "DROP TABLE IF EXISTS tablename"


def test_download_archive_gz_known():
    """Download and extract known files

    from a gzipped file to the .retriever/data  dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(
        url=gz_url, file_names=['test/sample_tar.csv'], archive_type='gz')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_gz_unknown():
    """Download and extract unknown files

    from a gzipped file to the .retriever/data  dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=gz_url,
                                                    archive_type='gz')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_targz_known():
    """Download and extract known files

    from a targzipped file to the .retriever/data  dir"""
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

    from a targzipped file to the .retriever/data  dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=tar_gz_url,
                                                    archive_type='tar.gz')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_tar_known():
    """Download and extract known files

    from a tarred file to the .retriever/data  dir"""
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

    from a tarred file to the .retriever/data  dir"""
    setup_functions()
    files = test_engine.download_files_from_archive(url=tar_url,
                                                    archive_type='tar')
    r_path = os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/test/test/sample_tar.csv'))
    assert r_path == test_engine.find_file('test/sample_tar.csv')
    assert ['sample_tar.csv'] <= files


def test_download_archive_zip_known():
    """Download and extract known files

    from a zipped file to the .retriever/data  dir"""
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

    from a zipped file to the .retriever/data  dir"""
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


def test_json2csv():
    """Test json2csv function.

    Creates a json file and tests the md5 sum calculation.
    """
    json_file = create_file([
        """[ {"User": "Alex", "Country": "US", "Age": "25"} ]"""],
        'output.json')

    output_json = json2csv(json_file, "output_json.csv",
                           header_values=["User", "Country", "Age"])
    obs_out = file_2list(output_json)
    os.remove(output_json)
    assert obs_out == ['User,Country,Age', 'Alex,US,25']


def test_xml2csv():
    """Test xml2csv function.

    Creates a xml file and tests the md5 sum calculation.
    """
    xml_file = create_file(['<root>', '<row>',
                            '<User>Alex</User>',
                            '<Country>US</Country>',
                            '<Age>25</Age>', '</row>',
                            '<row>', '<User>Ben</User>',
                            '<Country>US</Country>',
                            '<Age>24</Age>',
                            '</row>', '</root>'], 'output.xml')

    output_xml = xml2csv(xml_file, "output_xml.csv",
                         header_values=["User", "Country", "Age"])
    obs_out = file_2list(output_xml)
    os.remove(output_xml)
    assert obs_out == ['User,Country,Age', 'Alex,US,25', 'Ben,US,24']


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
    dataset = random.choice(rt.dataset_names())
    rt.reset_retriever(dataset)
    rt.reload_scripts()
    assert dataset not in rt.dataset_names()
    rt.check_for_updates()
    rt.reload_scripts()
    assert dataset in rt.dataset_names()
    os.chdir(pwd_name)


def test_setup_functions():
    """Test the set up function.

    Function uses teardown_module and setup_module functions."""
    file_path = raw_dir_files.format(file_name='')
    subprocess.call(['rm', '-r', file_path])
    assert os.path.exists(raw_dir_files.format(file_name="")) is False
    setup_functions()
    assert os.path.exists(raw_dir_files.format(file_name=""))
