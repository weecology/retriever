from __future__ import absolute_import
from __future__ import print_function

import os
from collections import OrderedDict

from retriever.engines import choose_engine
from retriever.lib.defaults import DATA_DIR, SCRIPT_WRITE_PATH
from retriever.lib.scripts import SCRIPT_LIST
from retriever.lib.engine_tools import name_matches
from retriever.lib.repository import check_for_updates


def _install(args, use_cache, debug):
    """Install datasets for retriever."""
    engine = choose_engine(args)
    engine.use_cache = use_cache

    script_list = SCRIPT_LIST()
    if not (script_list or os.listdir(SCRIPT_WRITE_PATH)):
        check_for_updates()
        script_list = SCRIPT_LIST()
    data_sets_scripts = name_matches(script_list, args['dataset'])
    if data_sets_scripts:
        for data_sets_script in data_sets_scripts:
            try:
                engine.script_table_registry = OrderedDict()
                data_sets_script.download(engine, debug=debug)
                data_sets_script.engine.final_cleanup()
            except Exception as e:
                print(e)
                if debug:
                    raise
    else:
        message = "Run retriever.datasets() to list the currently available " \
                  "datasets."
        raise ValueError(message)
    return engine


def install_csv(dataset,
                table_name='{db}_{table}.csv',
                data_dir=DATA_DIR, debug=False, use_cache=True):
    """Install datasets into csv."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'csv',
        'table_name': table_name,
        'data_dir': data_dir
    }
    return _install(args, use_cache, debug)


def install_mysql(dataset, user='root', password='', host='localhost',
                  port=3306, database_name='{db}', table_name='{db}.{table}',
                  debug=False, use_cache=True):
    """Install datasets into mysql."""
    args = {
        'command': 'install',
        'database_name': database_name,
        'engine': 'mysql',
        'dataset': dataset,
        'host': host,
        'port': port,
        'password': password,
        'table_name': table_name,
        'user': user
    }
    return _install(args, use_cache, debug)


def install_postgres(dataset, user='postgres', password='',
                     host='localhost', port=5432, database='postgres',
                     database_name='{db}', table_name='{db}.{table}', bbox=[],
                     debug=False, use_cache=True):
    """Install datasets into postgres."""
    args = {
        'command': 'install',
        'database': database,
        'database_name': database_name,
        'engine': 'postgres',
        'dataset': dataset,
        'host': host,
        'port': port,
        'password': password,
        'table_name': table_name,
        'user': user,
        'bbox': bbox
    }
    return _install(args, use_cache, debug)


def install_sqlite(dataset, file='sqlite.db',
                   table_name='{db}_{table}',
                   data_dir=DATA_DIR,
                   debug=False, use_cache=True):
    """Install datasets into sqlite."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'sqlite',
        'file': file,
        'table_name': table_name,
        'data_dir': data_dir
    }
    return _install(args, use_cache, debug)


def install_msaccess(dataset, file='access.mdb',
                     table_name='[{db} {table}]',
                     data_dir=DATA_DIR,
                     debug=False, use_cache=True):
    """Install datasets into msaccess."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'msaccess',
        'file': file,
        'table_name': table_name,
        'data_dir': data_dir
    }
    return _install(args, use_cache, debug)


def install_json(dataset,
                 table_name='{db}_{table}.json',
                 data_dir=DATA_DIR, debug=False, use_cache=True, pretty=False):
    """Install datasets into json."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'json',
        'table_name': table_name,
        'data_dir': data_dir,
        'pretty': pretty
    }
    return _install(args, use_cache, debug)


def install_xml(dataset,
                table_name='{db}_{table}.xml',
                data_dir=DATA_DIR, debug=False, use_cache=True):
    """Install datasets into xml."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'xml',
        'table_name': table_name,
        'data_dir': data_dir
    }
    return _install(args, use_cache, debug)
