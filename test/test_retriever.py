"""Tests for the EcoData Retriever"""
from future import standard_library
standard_library.install_aliases()
from imp import reload

import os

import sys
reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')
from io import StringIO
from retriever.lib.engine import Engine
from retriever.lib.table import Table
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.tools import getmd5
from retriever.lib.cleanup import correct_invalid_value
from retriever.lib.tools import xml2csv
from retriever.lib.tools import json2csv
from retriever.lib.tools import sort_file
from retriever.lib.tools import sort_csv
from retriever.lib.tools import create_file
from retriever.lib.tools import file_2string


# Create simple engine fixture
test_engine = Engine()
test_engine.table = Table("test")
test_engine.script = BasicTextTemplate(tables={'test': test_engine.table},
                                       shortname='test')
test_engine.opts = {'database_name': '{db}_abc'}
HOMEDIR = os.path.expanduser('~')


def setup_module():
    """"change directory to test directory"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def teardown_method():
    """Cleanup temporary output files after testing"""
    os.chdir("..")

def test_auto_get_columns():
    """Basic test of getting column labels from header"""
    test_engine.table.delimiter = ","
    columns, column_values = test_engine.table.auto_get_columns("a,b,c,d")
    assert columns == [['a', None], ['b', None], ['c', None], ['d', None]]


def test_auto_get_columns_cleanup():
    """Test of automatically cleaning up column labels from header"""
    test_engine.table.delimiter = ","
    columns, column_values = test_engine.table.auto_get_columns("a),b.b,c/c,d___d,group")
    assert columns == [['a', None], ['b_b', None], ['c_c', None], ['d_d', None],
                       ['grp', None]]


def test_auto_get_delimiter_comma():
    """Test if commas are properly detected as delimiter"""
    test_engine.auto_get_delimiter("a,b,c;,d")
    assert test_engine.table.delimiter == ","


def test_auto_get_delimiter_tab():
    """Test if commas are properly detected as delimiter"""
    test_engine.auto_get_delimiter("a\tb\tc\td,")
    assert test_engine.table.delimiter == "\t"


def test_auto_get_delimiter_semicolon():
    """Test if semicolons are properly detected as delimiter"""
    test_engine.auto_get_delimiter("a;b;c;,d")
    assert test_engine.table.delimiter == ";"


def test_correct_invalid_value_string():
    assert correct_invalid_value('NA', {'nulls': ['NA', '-999']}) == None


def test_correct_invalid_value_number():
    assert correct_invalid_value(-999, {'nulls': ['NA', '-999']}) == None


def test_correct_invalid_value_exception():
    assert correct_invalid_value(-999, {}) == -999


def test_create_db_statement():
    """Test creating the create database SQL statement"""
    assert test_engine.create_db_statement() == 'CREATE DATABASE test_abc'


def test_database_name():
    """Test creating database name"""
    assert test_engine.database_name() == 'test_abc'


def test_drop_statement():
    "Test the creation of drop statements"
    assert test_engine.drop_statement('TABLE', 'tablename') == "DROP TABLE IF EXISTS tablename"


def test_escape_single_quotes():
    """Test escaping of single quotes"""
    assert test_engine.escape_single_quotes("1,2,3,'a'") == "1,2,3,\\'a\\'"


def test_escape_double_quotes():
    """Test escaping of double quotes"""
    assert test_engine.escape_double_quotes('"a",1,2,3') == '\\"a\\",1,2,3'


def test_extract_values():
    """Test extraction of values from line of data with already know delimiter"""
    test_engine.table.delimiter = ","
    assert test_engine.table.extract_values('abcd,1,2,3.3') == ['abcd', '1', '2', '3.3']


def test_extract_values_fixed_width():
    """Test extraction of values from line of fixed width data"""
    test_engine.table.fixed_width = [5, 2, 2, 3, 4]
    assert test_engine.table.extract_values('abc  1 2 3  def ') == ['abc', '1', '2', '3', 'def']


def test_find_file_absent():
    """Test if find_file() properly returns false if no file is present"""
    assert test_engine.find_file('missingfile.txt') is False


def test_find_file_present():
    """Test if existing datafile is found

    Using the AvianBodySize dataset which is included for regression testing
    Because all testing code and data is located in ./test/ it is necessary to
    move into this directory for DATA_SEARCH_PATHS to work properly.

    """
    test_engine.script.shortname = 'AvianBodySize'
    assert test_engine.find_file('avian_ssd_jan07.txt') == os.path.normpath(
        'raw_data/AvianBodySize/avian_ssd_jan07.txt')


def test_format_data_dir():
    "Test if directory for storing data is properly formated"
    test_engine.script.shortname = "TestName"
    assert os.path.normpath(test_engine.format_data_dir()) == os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/TestName'))


def test_format_filename():
    "Test if filenames for stored files are properly formated"
    test_engine.script.shortname = "TestName"
    assert os.path.normpath(test_engine.format_filename('testfile.csv')) == os.path.normpath(
        os.path.join(HOMEDIR, '.retriever/raw_data/TestName/testfile.csv'))


def test_format_insert_value_int():
    """Test formatting of values for insert statements"""
    assert test_engine.format_insert_value(42, 'int') == 42


def test_format_insert_value_double():
    """Test formatting of values for insert statements"""
    assert test_engine.format_insert_value(26.22, 'double') == '26.22'


def test_format_insert_value_string_simple():
    """Test formatting of values for insert statements"""
    assert test_engine.format_insert_value('simple text', 'char') == "'simple text'"


def test_format_insert_value_string_complex():
    """Test formatting of values for insert statements"""
    assert test_engine.format_insert_value('my notes: "have extra, stuff"',
                                           'char') == '\'my notes: \\"have extra, stuff\\"\''


def test_getmd5_lines():
    """Test md5 sum calculation given a line"""
    lines = ['a,b,c\n', '1,2,3\n', '4,5,6\n']
    assert getmd5(data=lines, data_type='lines') == '0bec5bf6f93c547bc9c6774acaf85e1a'


def test_getmd5_path():
    """Test md5 sum calculation given a path to data source"""
    data_file = create_file('a,b,c\n1,2,3\n4,5,6\n')
    assert getmd5(data=data_file, data_type='file',mode='rU') == '0bec5bf6f93c547bc9c6774acaf85e1a'


def test_json2csv():
    """Test json2csv function
    creates a json file and tests the md5 sum calculation"""
    json_file = create_file("""[ {"User": "Alex", "Country": "US", "Age": "25"} ]""", 'output.json')
    output_json = json2csv(json_file, "output_json.csv", header_values=["User", "Country", "Age"])
    obs_out = file_2string(output_json)
    os.remove(output_json)
    assert obs_out == 'User,Country,Age\nAlex,US,25'


def test_xml2csv():
    """Test xml2csv function
    creates a xml file and tests the md5 sum calculation"""
    xml_file = create_file("<root>\n<row>\n"
                           "<User>Alex</User>\n"
                           "<Country>US</Country>\n"
                           "<Country>PT</Country>\n"
                           "<Age>25</Age>\n</row>\n"
                           "<row>\n<User>Ben</User>\n"
                           "<Country>US</Country>S\n"
                           "<Age>24</Age>\n"
                           "</row>\n</root>", 'output.xml')
    output_xml = xml2csv(xml_file, "output_xml.csv", header_values=["User", "Country", "Age"])
    obs_out = file_2string(output_xml)
    os.remove(output_xml)
    assert obs_out == "User,Country,Age\nAlex,US,25\nAlex,PT,25\nBen,US,24"


def test_sort_file():
    """Test md5 sum calculation"""
    data_file = create_file("Ben,US,24\nAlex,US,25\nAlex,PT,25")
    out_file = sort_file(data_file)
    obs_out = file_2string(out_file)
    os.remove(out_file)
    assert obs_out == 'Alex,PT,25\nAlex,US,25\nBen,US,24\n'


def test_sort_csv():
    """Test md5 sum calculation"""
    data_file = create_file("User,Country,Age\nBen,US,24\nAlex,US,25\nAlex,PT,25")
    out_file = sort_csv(data_file)
    obs_out = file_2string(out_file)
    os.remove(out_file)
    assert obs_out == "User,Country,Age\nAlex,PT,25\nAlex,US,25\nBen,US,24\n"
