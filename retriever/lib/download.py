from __future__ import absolute_import
from __future__ import print_function

import os

from retriever.engines import choose_engine
from retriever.lib.defaults import SCRIPT_WRITE_PATH
from retriever.lib.engine_tools import name_matches
from retriever.lib.repository import check_for_updates
from retriever.lib.scripts import SCRIPT_LIST


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
    else:
        message = "Run retriever.datasets() to see the list of currently " \
                  "available datasets."
        raise ValueError(message)
    return engine
