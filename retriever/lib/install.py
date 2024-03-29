import os
from collections import OrderedDict

from retriever.engines import choose_engine
from retriever.lib.defaults import DATA_DIR, SCRIPT_WRITE_PATH, PROVENANCE_DIR
from retriever.lib.rdatasets import update_rdataset_catalog, create_rdataset
from retriever.lib.scripts import SCRIPT_LIST, get_script, name_matches
from retriever.lib.repository import check_for_updates
from retriever.lib.provenance import install_committed
from retriever.lib.socrata import find_socrata_dataset_by_id, create_socrata_dataset


def _install(args, use_cache, debug):
    """Install datasets for retriever."""
    engine = choose_engine(args)
    engine.use_cache = use_cache

    if args['dataset'].endswith('.zip') or args.get('hash_value'):
        path_to_archive = args['dataset']
        if args.get('hash_value'):
            path_to_archive = os.path.join(
                PROVENANCE_DIR, args['dataset'],
                '{}-{}.zip'.format(args['dataset'], args['hash_value']))
        if not os.path.exists(path_to_archive):
            print('The committed file does not exist.')
        engine = install_committed(path_to_archive,
                                   engine,
                                   force=args.get('force', False))
        return engine
    script_list = SCRIPT_LIST()
    if not (script_list or os.listdir(SCRIPT_WRITE_PATH)):
        check_for_updates()
        script_list = SCRIPT_LIST()
    data_sets_scripts = name_matches(script_list, args['dataset'])
    if data_sets_scripts:
        for data_sets_script in data_sets_scripts:
            print("=> Installing", data_sets_script.name)
            try:
                if engine.name == "HDF5":
                    sqlite_opts = {
                        'command': 'install',
                        'dataset': data_sets_script,
                        'engine': 'sqlite',
                        'file': (args["file"].split("."))[0] + ".db",
                        'table_name': args["table_name"],
                        'data_dir': args["data_dir"]
                    }
                    sqlite_engine = choose_engine(sqlite_opts)
                    data_sets_script.download(sqlite_engine, debug=debug)
                    data_sets_script.engine.final_cleanup()
                engine.script_table_registry = OrderedDict()
                data_sets_script.download(engine, debug=debug)
                data_sets_script.engine.final_cleanup()
            except Exception as e:
                print(e)
                if debug:
                    raise
    elif args['dataset'].startswith('socrata') and not data_sets_scripts:
        socrata_id = args['dataset'].split('-', 1)[1]
        resource = find_socrata_dataset_by_id(socrata_id)

        if "error" in resource.keys():
            if resource["datatype"][0] == "map":
                print("{} because map type datasets are not supported".format(
                    resource["error"]))
            else:
                print("{} because it is of type {} and not tabular".format(
                    resource["error"], resource["datatype"][1]))
        elif len(resource.keys()) == 0:
            return
        else:
            print("=> Installing", args['dataset'])
            name = f"socrata-{socrata_id}"
            create_socrata_dataset(engine, name, resource)
            if args['command'] == 'download':
                return engine
            else:
                script_list = SCRIPT_LIST()
                script = get_script(args['dataset'])
                script.download(engine, debug=debug)
                script.engine.final_cleanup()
    elif args['dataset'].startswith('rdataset') and not data_sets_scripts:
        print("=> Installing", args['dataset'])
        rdataset = args['dataset'].split('-')
        update_rdataset_catalog()
        package, dataset_name = rdataset[1], rdataset[2]
        create_rdataset(engine, package, dataset_name)
        if args['command'] == 'download':
            return engine
        else:
            script_list = SCRIPT_LIST()
            script = get_script(args['dataset'])
            script.download(engine, debug=debug)
            script.engine.final_cleanup()
    else:
        message = "Run retriever.datasets() to list the currently available " \
                  "datasets."
        raise ValueError(message)
    return engine


def install_csv(dataset,
                table_name='{db}_{table}.csv',
                data_dir=DATA_DIR,
                debug=False,
                use_cache=True,
                force=False,
                hash_value=None):
    """Install datasets into csv."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'csv',
        'table_name': table_name,
        'data_dir': data_dir,
        'force': force,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)


def install_mysql(dataset,
                  user='root',
                  password='',
                  host='localhost',
                  port=3306,
                  database_name='{db}',
                  table_name='{db}.{table}',
                  debug=False,
                  use_cache=True,
                  force=False,
                  hash_value=None):
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
        'user': user,
        'force': force,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)


def install_postgres(dataset,
                     user='postgres',
                     password='',
                     host='localhost',
                     port=5432,
                     database='postgres',
                     database_name='{db}',
                     table_name='{db}.{table}',
                     bbox=[],
                     debug=False,
                     use_cache=True,
                     force=False,
                     hash_value=None):
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
        'bbox': bbox,
        'force': force,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)


def install_sqlite(dataset,
                   file='sqlite.db',
                   table_name='{db}_{table}',
                   data_dir=DATA_DIR,
                   debug=False,
                   use_cache=True,
                   force=False,
                   hash_value=None):
    """Install datasets into sqlite."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'sqlite',
        'file': file,
        'table_name': table_name,
        'data_dir': data_dir,
        'force': force,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)


def install_msaccess(dataset,
                     file='access.mdb',
                     table_name='[{db} {table}]',
                     data_dir=DATA_DIR,
                     debug=False,
                     use_cache=True,
                     force=False,
                     hash_value=None):
    """Install datasets into msaccess."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'msaccess',
        'file': file,
        'table_name': table_name,
        'data_dir': data_dir,
        'force': force,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)


def install_json(dataset,
                 table_name='{db}_{table}.json',
                 data_dir=DATA_DIR,
                 debug=False,
                 use_cache=True,
                 pretty=False,
                 force=False,
                 hash_value=None):
    """Install datasets into json."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'json',
        'table_name': table_name,
        'data_dir': data_dir,
        'pretty': pretty,
        'force': force,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)


def install_xml(dataset,
                table_name='{db}_{table}.xml',
                data_dir=DATA_DIR,
                debug=False,
                use_cache=True,
                force=False,
                hash_value=None):
    """Install datasets into xml."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'xml',
        'table_name': table_name,
        'data_dir': data_dir,
        'force': force,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)


def install_hdf5(dataset,
                 file='hdf5.h5',
                 table_name='{db}_{table}',
                 data_dir=DATA_DIR,
                 debug=False,
                 use_cache=True,
                 hash_value=None):
    """Install datasets into hdf5."""
    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'hdf5',
        'file': file,
        'table_name': table_name,
        'data_dir': data_dir,
        'hash_value': hash_value
    }
    return _install(args, use_cache, debug)
