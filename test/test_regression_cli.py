import os
import nose
from hashlib import md5

# First md5 is for csv, second md5 is for sqlite
known_md5s_sqlite = {'AvianBodySize' : '72256f681cdce96eba32d4ece270bcb2',
                     'DelMoral2010' : '92b6cd535f8e6c82d6fc19802d6ba64f',
                     'MoM2003' : 'd3bdce86e0fc5888449884dfb0ef4611'}

known_md5s_csv = {'AvianBodySize' : 'f42702a53e7d99d16e909676f30e5aa8',
                  'DelMoral2010' : '606f97c3ddbfd6d63b474bc76d01646a',
                  'MoM2003' : 'ef0a31c132cfe1c6594739c872f70f54'}

def getmd5(filename):
    """Get MD5 value for a file"""
    lines = open(filename, 'r')
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()

def test_sqlite_regression():
    """Regression tests for CLI imports to sqlite based on md5 checksums"""
    for dataset in known_md5s_sqlite:
            yield check_sqlite_regression, dataset, known_md5s_sqlite[dataset]
        
def check_sqlite_regression(dataset, known_md5):
    """Check for regression for a particular dataset imported to sqlite"""
    os.system("rm output_database") #reinstalling changes checksum in sqlite
    os.system("retriever install sqlite %s -f output_database" % dataset)
    os.system("echo '.dump' | sqlite3 output_database > output_file")
    current_md5 = getmd5('output_file')
    assert current_md5 == known_md5

def test_csv_regression():
    """Regression tests for CLI imports to csv based on md5 checksums"""
    for dataset in known_md5s_csv:
        yield check_csv_regression, dataset, known_md5s_csv[dataset]
    
def check_csv_regression(dataset, known_md5):
    """Check for regression for a particular dataset imported to csv"""
    os.system("rm output_file*")
    os.system("retriever install csv %s -t output_file_{table}" % dataset)
    os.system("cat output_file_* > output_file")
    current_md5 = getmd5('output_file')
    assert current_md5 == known_md5

if __name__ == '__main__':
    nose.runmodule()