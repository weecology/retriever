from __future__ import absolute_import
from __future__ import print_function

from retriever.engines import choose_engine
from retriever.lib.scripts import SCRIPT_LIST
from retriever.lib.tools import name_matches

script_list = SCRIPT_LIST()


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

    # scripts = name_matches(script_list, args['dataset'])
    # if scripts:
    #     for script in scripts:
    #         print("=> Downloading", script.name)
    #         try:
    #             script.download(engine, debug=debug)
    #             script.engine.final_cleanup()
    #         except Exception as e:
    #             print(e)
    #             if debug:
    #                 raise
    # else:
    #     message = "The dataset \"{}\" isn't currently available in the Retriever. " \
    #               "Run retriever.datasets() to see a list of currently " \
    #               "available datasets".format(args['dataset'])
    #     raise ValueError(message)
