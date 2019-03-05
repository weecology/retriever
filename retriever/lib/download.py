from __future__ import absolute_import
from __future__ import print_function

import os

from retriever.engines import choose_engine
from retriever.lib.defaults import SCRIPT_WRITE_PATH
from retriever.lib.scripts import SCRIPT_LIST
from retriever.lib.engine_tools import name_matches
from retriever.lib.repository import check_for_updates

from retriever.logger import getFileLogger
logger = getFileLogger(os.path.join(os.pardir, os.pardir, "logs"), "download.log")

def download(dataset, path='./', quiet=False, subdir=False, debug=False):
    """Download scripts for retriever."""
    args = {
        'dataset': dataset,
        'command': 'download',
        'path': path,
        'subdir': subdir,
        'quiet': quiet
    }
    engine = choose_engine(args)
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
                logger.error(str(e))
                print(e)
                if debug:
                    raise
    else:
        message = "Run retriever.datasets() to see a list of currently " \
                  "available datasets."
        raise ValueError(message)
