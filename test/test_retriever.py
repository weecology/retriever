"""Tests for the EcoData Retriever"""

from StringIO import StringIO
from engine import Engine
from table import Table
from nose.tools import with_setup

# Create simple engine fixture
test_engine = Engine()
test_engine.table = Table("test")


def test_escape_single_quotes():
    """Test escaping of single quotes"""
    assert test_engine.escape_single_quotes("1,2,3,'a'") == "1,2,3,\\'a\\'"

def test_escape_double_quotes():
    """Test escaping of double quotes"""
    assert test_engine.escape_double_quotes('"a",1,2,3') == '\\"a\\",1,2,3'

def test_drop_statement():
    "Test the creation of drop statements"
    assert test_engine.drop_statement('TABLE', 'tablename') == "DROP TABLE IF EXISTS tablename"

def test_auto_get_delimiter_comma():
    """Test if commas are properly detected as delimiter"""
    test_engine.auto_get_delimiter("a,b,c;,d")
    assert test_engine.table.delimiter == ","

def test_auto_get_delimiter_tab():
    """Test if commas are properly detected as delimiter"""
    test_engine.auto_get_delimiter("a\tb\tc\td,")
    assert test_engine.table.delimiter == "\t"

def test_auto_get_delimiter_semicolon():
    """Test if commas are properly detected as delimiter"""
    test_engine.auto_get_delimiter("a;b;c;,d")
    assert test_engine.table.delimiter == ";"

def test_auto_get_columns():
    """Basic test of getting column labels from header"""
    test_engine.table.delimiter = ","
    columns, column_values = test_engine.table.auto_get_columns("a,b,c,d")
    assert columns == [['a', None], ['b', None], ['c', None], ['d', None]]

def test_auto_get_columns_cleanup():
    """Test of automatically cleaning up column labels from header"""
    test_engine.table.delimiter = ","
    columns, column_values = test_engine.table.auto_get_columns("a),b.b,c/c,d___d,group")
    assert columns == [['a', None], ['bb', None], ['c_c', None], ['d_d', None],
                       ['grp', None]]

def test_extract_values():
    """Test extraction of values from line of data with already know delimiter"""
    test_engine.table.delimiter = ","
    assert test_engine.table.extract_values('abcd,1,2,3.3') == ['abcd', '1', '2', '3.3']

def test_extract_values_fixed_width():
    """Test extraction of values from line of fixed width data"""
    test_engine.table.fixed_width = [5, 2, 2, 3, 4]
    assert test_engine.table.extract_values('abc  1 2 3  def ') == ['abc', '1', '2', '3', 'def']
