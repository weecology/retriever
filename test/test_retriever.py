"""Tests for the EcoData Retriever"""

from StringIO import StringIO
from engine import Engine

def test_escape_single_quotes():
    """Test escaping of single quotes"""
    test_engine = Engine()
    assert test_engine.escape_single_quotes("1,2,3,'a'") == "1,2,3,\\'a\\'"

def test_escape_double_quotes():
    """Test escaping of double quotes"""
    test_engine = Engine()
    assert test_engine.escape_double_quotes('"a",1,2,3') == '\\"a\\",1,2,3'

def test_drop_statement():
    "Test the creation of drop statements"
    test_engine = Engine()
    assert test_engine.drop_statement('TABLE', 'tablename') == "DROP TABLE IF EXISTS tablename"
