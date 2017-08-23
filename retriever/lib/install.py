from __future__ import absolute_import
from __future__ import print_function

import os

from retriever.engines import choose_engine
from retriever.lib.defaults import DATA_DIR
from retriever.lib.scripts import SCRIPT_LIST
from retriever.lib.tools import name_matches


def _install(args, use_cache, debug, compile):
    """Install scripts for retriever."""
    engine = choose_engine(args)
    engine.use_cache = use_cache

    script_list = SCRIPT_LIST(force_compile=True)
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
        message = "The dataset \"{}\" isn't available in the Retriever. " \
                  "Run retriever.datasets()to list the currently available " \
                  "datasets".format(args['dataset'])
        raise ValueError(message)


def install_csv(dataset, table_name=None, compile=False, debug=False,
                quite=False, use_cache=True):
    """Install scripts in csv."""
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


def install_mysql(dataset, user='root', password='', host='localhost',
                  port=3306, database_name=None, table_name=None,
                  compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in mysql."""
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


def install_postgres(dataset, user='postgres', password='',
                     host='localhost', port=5432, database='postgres',
                     database_name=None, table_name=None,
                     compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in postgres."""
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


def install_sqlite(dataset, file=None, table_name=None,
                   compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in sqlite."""
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


def install_msaccess(dataset, file=None, table_name=None,
                     compile=False, debug=False, quite=False, use_cache=True):
    """Install scripts in msaccess."""
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


def install_json(dataset, table_name=None, compile=False,
                 debug=False, quite=False, use_cache=True):
    """Install scripts in json."""
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


def install_xml(dataset, table_name=None, compile=False, debug=False,
                quite=False, use_cache=True):
    """Install scripts in xml."""
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
