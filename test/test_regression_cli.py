import os
import nose
from hashlib import md5

# First md5 is for csv, second md5 is for sqlite
known_md5s = {'AvianBodySize' : {'s' : 'bbf85e30cd05b622da71508ee70d3b5f'},
              'DelMoral2010' : {'s' : '2630b6db704d88def23bca8929c24ce0'}}

def getmd5(filename):
    """Get MD5 value for a file"""
    lines = open(filename, 'r')
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()

def test_sqlite_regression():
    """Regression tests for CLI imports based on md5 checksums"""
    for dataset in known_md5s:
        yield check_sqlite_regression, dataset, known_md5s[dataset]['s']
        
def check_sqlite_regression(dataset, known_md5):
    """Check for regression for a particular dataset and engine"""
    os.system("rm output_file") #reinstalling changes checksum in sqlite
    os.system("retriever install %s -e s -f output_file" % dataset)
    current_md5 = getmd5('output_file')
    assert current_md5 == known_md5
    
if __name__ == '__main__':
    nose.runmodule()