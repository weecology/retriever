import os
import nose
from hashlib import md5

def getmd5(filename):
    """Get MD5 value for a file"""
    lines = open(filename, 'r')
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()

def test_AvianBodySize_csv():
    """Regression test for importing AvianBodySize into csv
    
    Data structure:
    Single table, tab delimited, -999 null replacement
    
    """
    os.system("retriever install AvianBodySize -e c -f avian_body_size.csv")
    current_md5 = getmd5('AvianBodySize_species.csv')
    known_md5 = 'f42702a53e7d99d16e909676f30e5aa8'
    assert current_md5 == known_md5

def test_AvianBodySize_sqlite():
    """Regression test for importing AvianBodySize into sqlite
    
    Data structure:
    Single table, tab delimited, -999 null replacement
    
    """
    os.system("retriever install AvianBodySize -e s -f avian_body_size.sqlite")
    current_md5 = getmd5('avian_body_size.sqlite')
    known_md5 = 'bbf85e30cd05b622da71508ee70d3b5f'
    assert current_md5 == known_md5
    
if __name__ == '__main__':
    nose.runmodule()