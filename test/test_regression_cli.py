import os
import nose
from unittest import TestCase
from hashlib import md5

# First md5 is for csv, second md5 is for sqlite
known_md5s = {'sqlite': {'AvianBodySize' : '72256f681cdce96eba32d4ece270bcb2',
                         'DelMoral2010' : '92b6cd535f8e6c82d6fc19802d6ba64f',
                         'MoM2003' : 'd3bdce86e0fc5888449884dfb0ef4611'},
              'csv': {'AvianBodySize' : 'f42702a53e7d99d16e909676f30e5aa8',
                      'DelMoral2010' : '606f97c3ddbfd6d63b474bc76d01646a',
                      'MoM2003' : 'ef0a31c132cfe1c6594739c872f70f54'},
              'mysql': {'AvianBodySize' : 'f60ac93d9be4671dbef77da9d10676b8',
                        'DelMoral2010' : 'f241fd296130512d4e1029376b58a4ea',
                        'MoM2003' : '9728728d72af4c21a2a6e29fec3edb48'},
              'postgres': {'AvianBodySize' : '60c252af74d914e3c15fa9af43edefca',
                         'DelMoral2010' : '1e8de8fa3ddbd4ca3a7cab921926e70e',
                         'MoM2003' : 'a55c8308722c8e20950e0d1e6d9639e6'}}


def setup_module():
    """Update retriever scripts and cd to test directory to find data"""
    os.chdir("./test/")
    os.system("retriever update")

def teardown_module():
    """Cleanup temporary output files after testing and return to root directory"""
    os.system("rm output_*")
    os.chdir("..")

def getmd5(filename):
    """Get MD5 value for a file"""
    lines = open(filename, 'rU')
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()

def _test_factory(test_method, name, *args):
    stub_test = lambda self: getattr(self, test_method)(*args)
    stub_test.func_name = stub_test.__name__ = 'test_%s' % dataset
    return stub_test

class SqliteRegression(TestCase):
    def check_sqlite_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to sqlite"""
        os.system("rm output_database") #reinstalling changes checksum in sqlite
        os.system("retriever install sqlite %s -f output_database" % dataset)
        os.system("echo '.dump' | sqlite3 output_database > output_file")
        current_md5 = getmd5('output_file')
        assert current_md5 == known_md5


class CSVRegression(TestCase):
    def check_csv_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to csv"""
        os.system("rm output_file*")
        os.system("retriever install csv %s -t output_file_{table}" % dataset)
        os.system("cat output_file_* > output_file")
        current_md5 = getmd5('output_file')
        assert current_md5 == known_md5


class MySQLRegression(TestCase):
    def check_mysql_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to sqlite"""
        os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"') # installing over an existing database changes the dump
        os.system("retriever install mysql %s -u travis -d testdb" % dataset)   #user 'travis' for Travis CI
        os.system("mysqldump testdb -u travis --compact --compatible=no_table_options --no-create-db --no-create-info --result-file=output_file")
        current_md5 = getmd5('output_file')
        assert current_md5 == known_md5


class PostgreSQLRegression(TestCase):
    def check_postgres_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to sqlite"""
        os.system('psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
        os.system("retriever install postgres %s -u postgres -d testdb -a testschema" % dataset)
        os.system("pg_dump -n testschema --data-only -U postgres -h localhost -f output_file testdb")
        current_md5 = getmd5('output_file')
        assert current_md5 == known_md5

dbms_test_classes = {'sqlite': SqliteRegression, 'csv': CSVRegression,
                     'mysql': MySQLRegression, 'postgres': PostgreSQLRegression}

for dbms in known_md5s:
    for dataset in known_md5s[dbms]:
        stub_test = _test_factory('check_%s_regression' % dbms, 'test_%s' % dataset,
                                  dataset, known_md5s[dbms][dataset])
        setattr(dbms_test_classes[dbms], stub_test.__name__, stub_test)
        del(stub_test)

if __name__ == '__main__':
    nose.runmodule()
