from __future__ import print_function
from __future__ import absolute_import
import imp
import os
import sys
from pkg_resources import parse_version
from retriever.engines import choose_engine
from retriever.lib.compile import compile_json
from retriever.lib.defaults import DATA_DIR, SCRIPT_SEARCH_PATHS, VERSION
from retriever.lib.tools import name_matches
from retriever.lib.scripts import SCRIPT_LIST

script_list = SCRIPT_LIST()


def _compile(dataset):
    json_file = dataset + '.json'
    py_file = dataset + '.py'

    for search_path in [search_path for search_path in SCRIPT_SEARCH_PATHS if os.path.exists(search_path)]:
        files = os.listdir(search_path)
        for file in files:
            if file == json_file:
                compile_json(os.path.join(search_path, dataset))
            if file == py_file:
                file, pathname, desc = imp.find_module(dataset, [search_path])
                try:
                    new_module = imp.load_module(dataset, file, pathname, desc)
                    if hasattr(new_module.SCRIPT, "retriever_minimum_version"):
                        # a script with retriever_minimum_version should be loaded
                        # only if its compliant with the version of the retriever
                        if not parse_version(VERSION) >= parse_version("{}".format(
                                new_module.SCRIPT.retriever_minimum_version)):
                            print("{} is supported by Retriever version {}".format(dataset,
                                                                                   new_module.SCRIPT.retriever_minimum_version))
                            print("Current version is {}".format(VERSION))
                            continue
                    # if the script wasn't found in an early search path
                    # make sure it works and then add it
                    new_module.SCRIPT.download
                except Exception as e:
                    sys.stderr.write("Failed to load script: %s (%s)\nException: %s \n" % (
                        dataset, search_path, str(e)))


def _install(args, use_cache, debug, compile):
    """Calling the download-install function."""
    engine = choose_engine(args)
    engine.use_cache = use_cache

    if compile:
        _compile(args['dataset'])

    scripts = name_matches(script_list, args['dataset'])
    if scripts:
        for script in scripts:
            print("=> Installing", script.name)
            try:
                script.download(engine, debug=debug)
                script.engine.final_cleanup()
            except Exception as e:
                print(e)
                if debug:
                    raise
    else:
        message = "The dataset \"{}\" isn't currently available in the Retriever. Run retriever.datasets() to see a list of currently available datasets".format(args['dataset'])
        raise ValueError(message)


def install_csv(dataset, table_name=None, compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in csv for retriever."""
    if not table_name:
        table_name = os.path.join(DATA_DIR, '{db}_{table}.csv')

    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'csv',
        'quite': quite,
        'table_name': table_name,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)


def install_mysql(dataset, user='root', password='', host='localhost', port=3306, database_name=None, table_name=None, compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in mysql for retriever."""
    if not database_name:
        database_name = '{db}'
    if not table_name:
        table_name = '{db}.{table}'

    args = {
        'command': 'install',
        'database_name': database_name,
        'engine': 'mysql',
        'dataset': dataset,
        'debug': debug,
        'host': host,
        'port': port,
        'password': password,
        'quite': quite,
        'table_name': table_name,
        'user': user,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)


def install_postgres(dataset, user='postgres', password='', host='localhost', port=5432, database='postgres', database_name=None, table_name=None, compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in postgres for retriever."""
    if not table_name:
        table_name = '{db}.{table}'
    if not database_name:
        database_name = '{db}'

    args = {
        'command': 'install',
        'database': database,
        'database_name': database_name,
        'engine': 'postgres',
        'dataset': dataset,
        'debug': debug,
        'host': host,
        'port': port,
        'password': password,
        'quite': quite,
        'table_name': table_name,
        'user': user,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)


def install_sqlite(dataset, file=None, table_name=None, compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in sqlite for retriever."""
    if not table_name:
        table_name = '{db}_table'
    if not file:
        file = os.path.join(DATA_DIR, 'sqlite.db')

    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'sqlite',
        'file': file,
        'quite': quite,
        'table_name': table_name,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)


def install_msaccess(dataset, file=None, table_name=None, compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in msaccess for retriever."""
    if not file:
        file = os.path.join(DATA_DIR, 'access.mdb')
    if not table_name:
        table_name = '[{db} {table}]'

    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'msaccess',
        'file': file,
        'quite': quite,
        'table_name': table_name,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)


def install_json(dataset, table_name=None, compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in json for retriever."""
    if not table_name:
        table_name = os.path.join(DATA_DIR, '{db}_{table}.json')

    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'json',
        'quite': quite,
        'table_name': table_name,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)


def install_xml(dataset, table_name=None, compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in xml for retriever."""
    if not table_name:
        table_name = os.path.join(DATA_DIR, '{db}_{table}.xml')

    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'xml',
        'quite': quite,
        'table_name': table_name,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)
