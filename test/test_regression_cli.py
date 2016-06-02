import os

import pytest
from retriever import SCRIPT_LIST
from retriever.lib.get_opts import parser
from retriever.lib.tools import getmd5
from retriever.lib.tools import name_matches
from retriever.lib.tools import choose_engine

download_md5 = [
    # ('DelMoral2010', '0'),
    ('AvianBodySize', 'dce81ee0f040295cd14c857c18cc3f7e'),
    ('MoM2003', 'b54b80d0d1959bdea0bb8a59b70fa871')
]

db_md5 = [
    # ('DelMoral2010', '0'),
    ('AvianBodySize', '92ab6bddeb94af8126a8c06d660d418f'),
    ('MoM2003', 'e0d38086326753eff2fd538864ce3664')
]

csv_md5 = [
    # ('DelMoral2010', '0'),
    ('AvianBodySize', 'e49470d9ca0b2e6142e4b06a96e8b4a0'),
    ('MoM2003', '8b2d159c3727ea0eb46027033a46a58b')
]

filedb_md5 = [
    # ('DelMoral2010', '0'),
    ('AvianBodySize', '47bdcf49c28fad5a444709f33cbc5c20'),
    ('MoM2003', 'a605380ab4610d54f431e5413ef35c5e')
]


def setup_module(module):
    """Set working directory for running tests
     and update the retriever scripts before starting
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir_path)
    # os.chdir("./test/")
    os.system("retriever update")


def teardown_module():
    """Cleanup temporary output files after testing and return to root directory"""
    os.system(" rm -r output_*")
    os.system("rm -r raw_data/MoM2003")
    os.chdir("..")


def tocsv(arg=None, mode="rb"):
    # at this point the current directory is ./test
    if os.path.exists("output_dumps"):
        os.system("rm -r output_dumps")
    os.makedirs("output_dumps")
    os.chdir("output_dumps")
    if arg:
        engine = choose_engine(arg.__dict__)
        script_list = SCRIPT_LIST()
        scripts = name_matches(script_list, arg.dataset)
        for dataset_i in scripts:
            if arg.engine in ["csv", 'json', 'xml']:
                # the engines in the list need to download the data
                dataset_i.download(engine, arg.debug, False)
                dataset_i.engine.final_cleanup()

            dataset_i.download(engine, arg.debug, True)
            dataset_i.engine.final_cleanup()
    os.chdir("..")
    current_md5 = getmd5("output_dumps",data_type='dir', mode=mode)
    return current_md5


@pytest.mark.parametrize("dataset,expected", download_md5)
def test_download_regression(dataset, expected):
    """Check for regression for a particular dataset downloaded only"""
    os.system("retriever download {0} -p raw_data/{0}".format(dataset))
    current_md5 = getmd5("raw_data/%s" % (dataset), data_type='dir', mode="rU")
    assert current_md5 == expected


@pytest.mark.parametrize("dataset,expected", db_md5)
def test_sqlite_regression(dataset, expected):
    """Check for regression for a particular dataset imported to sqlite"""
    dbfile = os.path.normpath(os.path.join(os.getcwd(), "output_database"))
    os.system("retriever install sqlite {0} -f {1}".format(dataset, dbfile))
    arg = parser.parse_args(['install', 'sqlite', dataset, '-f', dbfile])
    current_md5 = tocsv(arg)
    assert current_md5 == expected


@pytest.mark.parametrize("dataset,expected", db_md5)
def test_mysql_regression(dataset, expected):
    """Check for regression for a particular dataset imported to mysql"""
    os.system('mysql -u travis -Bse "DROP DATABASE IF EXISTS testdb"')
    os.system("retriever install mysql %s -u travis -d testdb" % dataset)
    arg = parser.parse_args(['install', 'mysql', dataset, '-u', 'travis', '-d', 'testdb'])
    current_md5 = tocsv(arg)
    assert current_md5 == expected


@pytest.mark.parametrize("dataset,expected", db_md5)
def test_postgres_regression(dataset, expected):
    """Check for regression for a particular dataset imported to postgres"""
    os.system('psql -U postgres -d testdb -h localhost -c "DROP SCHEMA IF EXISTS testschema CASCADE"')
    os.system("retriever install postgres %s -u postgres  -d testdb -a testschema" % dataset)
    arg = parser.parse_args(['install', 'postgres', dataset, '-u', 'postgres', '-d', 'testdb', '-a', 'testschema'])
    current_md5 = tocsv(arg)
    assert current_md5 == expected


@pytest.mark.parametrize("dataset,expected", csv_md5)
def test_csvengine_regression(dataset, expected):
    """Check for regression for a particular dataset imported to csv"""
    arg = parser.parse_args(['install', 'csv', dataset, '-t', 'output_file_{table}.csv'])
    current_md5 = tocsv(arg, mode="rb")
    assert current_md5 == expected


@pytest.mark.parametrize("dataset,expected", filedb_md5)
def test_jsonengine_regression(dataset, expected):
    """Check for regression for a particular dataset imported to csv"""
    arg = parser.parse_args(['install', 'json', dataset, '-t', 'output_file_{table}.json'])
    current_md5 = tocsv(arg, mode="rb")
    assert current_md5 == expected


@pytest.mark.parametrize("dataset,expected", filedb_md5)
def test_xmlengine_regression(dataset, expected):
    """Check for regression for a particular dataset imported to csv"""
    arg = parser.parse_args(['install', 'xml', dataset, '-t', 'output_file_{table}.xml'])
    current_md5 = tocsv(arg, mode="rb")
    assert current_md5 == expected

