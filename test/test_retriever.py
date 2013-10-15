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
    columns, column_values = test_engine.auto_get_columns("a,b,c,d")
    assert columns == [['a', None], ['b', None], ['c', None], ['d', None]]

def test_auto_get_columns_cleanup():
    """Test of automatically cleaning up column labels from header"""
    test_engine.table.delimiter = ","
    columns, column_values = test_engine.auto_get_columns("a),b.b,c/c,d___d,group")
    assert columns == [['a', None], ['bb', None], ['c_c', None], ['d_d', None],
                       ['grp', None]]
