from __future__ import print_function
from __future__ import absolute_import
import os
from retriever.engines import choose_engine
from retriever.lib.defaults import DATA_DIR
from retriever.lib.tools import name_matches
from retriever.lib.scripts import SCRIPT_LIST

script_list = SCRIPT_LIST()


def install_csv(dataset, table_name=os.path.join(DATA_DIR, '{db}_{table}.csv'), compile=False, debug=False, quite=False, use_cache=False):
    """Install scripts in csv for retriever."""
    args = {
        'command': 'install',
        'compile': compile,
        'dataset': dataset,
        'engine': 'csv',
        'quite': quite,
        'table_name': table_name
    }

    engine = choose_engine(args)
    engine.use_cache = use_cache

    scripts = name_matches(script_list, args['dataset'])
    if scripts:
        for script in scripts:
            print("=> Downloading", script.name)
            try:
                script.download(engine, debug=debug)
                script.engine.final_cleanup()
            except Exception as e:
                print(e)
                if debug:
                    raise
    else:
        print("The dataset {} isn't currently available in the Retriever".format(args['dataset']))
        print("Run 'retriever ls to see a list of currently available datasets")


def install_mysql(dataset, user='root', password='', host='localhost', port=3306, database_name='{db}', table_name='{db}.{table}', compile=False, debug=False, quite=False, use_cache=False):
    """Install scripts in mysql for retriever."""
    args = {
        'command': 'install',
        'compile': compile,
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
    }

    engine = choose_engine(args)
    engine.use_cache = use_cache

    scripts = name_matches(script_list, args['dataset'])
    if scripts:
        for script in scripts:
            print("=> Downloading", script.name)
            try:
                script.download(engine, debug=debug)
                script.engine.final_cleanup()
            except Exception as e:
                print(e)
                if debug:
                    raise
    else:
        print("The dataset {} isn't currently available in the Retriever".format(args['dataset']))
        print("Run 'retriever ls to see a list of currently available datasets")
