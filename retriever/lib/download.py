import os

from retriever.engines import choose_engine
from retriever.lib.defaults import SCRIPT_WRITE_PATH
from retriever.lib.rdatasets import create_rdataset, update_rdataset_catalog
from retriever.lib.repository import check_for_updates
from retriever.lib.scripts import SCRIPT_LIST, name_matches
from retriever.lib.socrata import find_socrata_dataset_by_id, create_socrata_dataset


def download(dataset, path='./', quiet=False, sub_dir='', debug=False, use_cache=True):
    """Download scripts for retriever."""
    args = {
        'dataset': dataset,
        'command': 'download',
        'path': path,
        'sub_dir': sub_dir,
        'quiet': quiet
    }
    engine = choose_engine(args)
    engine.use_cache = use_cache

    script_list = SCRIPT_LIST()
    if not script_list or not os.listdir(SCRIPT_WRITE_PATH):
        check_for_updates()
        script_list = SCRIPT_LIST()
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
    elif args['dataset'].startswith('socrata') and (scripts is None):
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
            print("=> Downloading", args['dataset'])
            name = f"socrata-{socrata_id}"
            create_socrata_dataset(engine, name, resource)
    elif (scripts is None) and (args['dataset'].startswith('rdataset')):
        print("=> Downloading", args['dataset'])
        rdataset = args['dataset'].split('-')
        update_rdataset_catalog()
        package, dataset_name = rdataset[1], rdataset[2]
        create_rdataset(engine, package, dataset_name)
    else:
        message = "Run retriever.datasets() to see the list of currently " \
                  "available datasets."
        raise ValueError(message)
    return engine
