"""EcoData Retriever Wizard

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""

import os
import platform
import sys
# sys removes the setdefaultencoding method at startup; reload to get it back
reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    # set default encoding to latin-1 to avoid ascii encoding issues
    sys.setdefaultencoding('latin-1')
else:
    pass
from retriever import VERSION, MASTER, SCRIPT_LIST, ENGINE_LIST
from retriever.lib.repository import check_for_updates
from retriever.lib.lists import Category, get_lists
from retriever.lib.tools import choose_engine, get_opts


def main():
    """This function launches the EcoData Retriever."""
    if len(sys.argv) == 1:
        if not MASTER:
            check_for_updates(graphical=False if 'darwin' in platform.platform().lower() else True)
        lists = get_lists()
        
        from retriever.app.main import launch_app
        launch_app(lists)
    else:
        script_list = SCRIPT_LIST()
        opts = get_opts(script_list)
        
        if "update" in opts.keys() and opts["update"]:
            check_for_updates(graphical=False)
            script_list = SCRIPT_LIST()
            opts = get_opts(script_list)
            
        if "force" in opts.keys() and opts["force"]:
            script_list = SCRIPT_LIST(force_compile=True)
            
        if "gui" in opts.keys():
            lists = get_lists()

            from retriever.app.main import launch_app
            launch_app(lists)
            return            
            
        try:
            script = opts["script"]
        except KeyError:
            print "EcoData Retriever, version", VERSION
            print "Usage: retriever [install script_name]"
            print "                 [-e engine] [-h host] [-o port] [-u username] [-p password]"
            print "                 [-f filename (sqlite/ms access)] [-d database (postgresql)]"
            print "                 [--update] [--debug] [--compile]"
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
            print '\t', '\t'.join(sorted(list(all_scripts), key=lambda s: s.lower()))
            print "Groups:"
            print '\t', '\t'.join(sorted(list(all_tags)))
            if len(all_scripts) == 0:
                print "Run 'retriever update' to download the latest scripts from the repository."
            sys.exit()
        
        engine = choose_engine(opts)
        debug = False
        if "debug" in opts.keys() and opts["debug"]: debug = True
        if isinstance(script, list):
            for dataset in script:
                print "=> Installing", dataset.name
                try:
                    dataset.download(engine, debug=debug)
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print e

        else:
            script.download(engine)
        print "Done!"
                                                            

if __name__ == "__main__":
    main()
