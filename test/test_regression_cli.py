import os
import nose
import shutil
from unittest import TestCase
from hashlib import md5
from retriever.lib.tools import get_path_md5, getmd5_u

known_md5s = {

    'sqlite':    {'AvianBodySize': '0f503559426ba0c2dbd56e58882988f5',
                 'DelMoral2010':   '734831950c432d0002b84ed1d26f949e',
                 'MoM2003':        '527456ac4f9abdfef36c76c4c4f4295f'},

    'download': {'AvianBodySize':  'dce81ee0f040295cd14c857c18cc3f7e',
                 'DelMoral2010':   '2b6e92b014ae73ea1f0195ecfdf6248d',
                 'MoM2003':        'b54b80d0d1959bdea0bb8a59b70fa871'},

    'csv':      {'AvianBodySize':  'f42702a53e7d99d16e909676f30e5aa8',
                 'DelMoral2010':   'e79d55ac15f1a70a6c7d3ad4e678ec0e',
                 'MoM2003':        'ef0a31c132cfe1c6594739c872f70f54'},

    'mysql':     {'AvianBodySize': '0f503559426ba0c2dbd56e58882988f5',
                 'DelMoral2010':   '734831950c432d0002b84ed1d26f949e',
                 'MoM2003':        '527456ac4f9abdfef36c76c4c4f4295f'},

    'postgres':  {'AvianBodySize': '0f503559426ba0c2dbd56e58882988f5',
                 'DelMoral2010':   '734831950c432d0002b84ed1d26f949e',
                 'MoM2003':        '527456ac4f9abdfef36c76c4c4f4295f'},
}


def setup_module():
    """Update retriever scripts and cd to test directory to find data"""
    os.chdir("./test/")
    os.system("retriever update")


def teardown_module():
    """Cleanup temporary output files after testing and return to root directory"""
    os.system("rm output_*")
    os.system("rm -r raw_data/MoM2003")
    os.chdir("..")


def _test_factory(test_method, name, *args):
    stub_test = lambda self: getattr(self, test_method)(*args)
    stub_test.func_name = stub_test.__name__ = 'test_%s' % dataset
    return stub_test


class CSVRegression(TestCase):

    def check_csv_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to csv"""
        os.system("rm output_file*")
        os.system("retriever install csv %s -t output_file_{table}" % dataset)
        os.system("cat output_file_* > output_file")
        current_md5 = getmd5_u('output_file')
        assert current_md5 == known_md5


class DownloadRegression(TestCase):

    def check_download_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset downloaded only"""
        os.system("retriever download {0} -p raw_data/{0}".format(dataset))
        current_md5 = getmd5_u("raw_data/%s" % (dataset))
        assert current_md5 == known_md5


class SqliteRegression(TestCase):

    def check_sqlite_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to sqlite"""

        dbfile = os.path.normpath(os.path.join(os.getcwd(), "output_database"))
        os.system("retriever install sqlite {0} -f {1}".format(dataset, dbfile))
        if os.path.exists(dataset):
            shutil.rmtree(dataset)
        os.makedirs(dataset)
        os.chdir(dataset)
        os.system("retriever export --sorted  sqlite {0} -f {1}".format(dataset, dbfile))
        os.chdir("..")
        current_md5 = get_path_md5(dataset)
        shutil.rmtree(dataset)
        os.remove(dbfile)
        assert current_md5 == known_md5


class MySQLRegression(TestCase):

    def check_mysql_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to mysql"""
        os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
        os.system("retriever install mysql %s -u travis -d  testdb" %dataset)
        if os.path.exists(dataset):
            shutil.rmtree(dataset)
        os.makedirs(dataset)
        os.chdir(dataset)
        os.system("retriever export --sorted  mysql %s -u travis -d testdb" %dataset)
        os.chdir("..")
        current_md5 = get_path_md5(dataset)
        shutil.rmtree(dataset)
        assert current_md5 == known_md5


class PostgreSQLRegression(TestCase):

    def check_postgres_regression(self, dataset, known_md5):
        """Check for regression for a particular dataset imported to postgres"""
        os.system('psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
        os.system("retriever install postgres %s -u postgres -d testdb -a testschema" % dataset)
        if os.path.exists(dataset):
            shutil.rmtree(dataset)
        os.makedirs(dataset)
        os.chdir(dataset)
        os.system("retriever export --sorted postgres %s -u postgres -d testdb -a testschema" % dataset)
        os.chdir("..")
        current_md5 = get_path_md5(dataset)
        shutil.rmtree(dataset)
        assert current_md5 == known_md5


dbms_test_classes = {'sqlite':   SqliteRegression,
                     'csv':      CSVRegression,
                     'mysql':    MySQLRegression,
                     'postgres': PostgreSQLRegression,
                     'download': DownloadRegression
                     }

for dbms in known_md5s:
    for dataset in known_md5s[dbms]:
        stub_test = _test_factory('check_%s_regression' % dbms, 'test_%s' % dataset,
                                  dataset, known_md5s[dbms][dataset])
        setattr(dbms_test_classes[dbms], stub_test.__name__, stub_test)
        del(stub_test)

if __name__ == '__main__':
    nose.runmodule()
