"""EcoData Retriever Wizard

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""

import os
import sys
from retriever import VERSION, SCRIPT_LIST, ENGINE_LIST
from retriever.lib.repository import check_for_updates
from retriever.lib.lists import Category, get_lists
from retriever.lib.tools import choose_engine, get_opts
from retriever.app.main import launch_app


def main():
    """This function launches the EcoData Retriever."""
    if VERSION != "master":
        check_for_updates()
        lists = get_lists()
        launch_app(lists)
    else:
        script_list = SCRIPT_LIST()
        opts = get_opts(script_list)
        try:
            script = opts["script"]
        except KeyError:
            print "EcoData Retriever, version", VERSION
            print "Usage: retriever [install script]"
            print "                 [-e engine]"
            print "                 [-u username]"
            print "                 [-p password]"
            print "                 [-h host]"
            print "                 [-o port]"
            print "                 [-f filename (sqlite/ms access)]"
            print "                 [-d database (postgresql)]"
            print "Available engines:"
            for engine in ENGINE_LIST():
                if engine.abbreviation:
                    abbreviation = "(" + engine.abbreviation + ") "
                else:
                    abbreviation = ""
                print "\t", abbreviation, engine.name
            all_scripts = set([script.shortname for script in script_list])
            all_tags = set(["ALL"] + 
                            [tag.strip().upper() for script in script_list for tagset in script.tags for tag in tagset.split('>')])
            print "Available datasets (%s):" % len(all_scripts)
            print '\t', '\t'.join(sorted(list(all_scripts)))
            print '\t', '\t'.join(sorted(list(all_tags)))
            sys.exit()
        
        engine = choose_engine(opts)
        if isinstance(script, list):
            for dataset in script:
                print "=> Installing", dataset.name
                try:
                    dataset.download(engine)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print e

        else:
            script.download(engine)
        print "Done!"
                                                            

if __name__ == "__main__":
    main()
