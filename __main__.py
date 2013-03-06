"""EcoData Retriever Wizard

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""

import argparse
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
from retriever import VERSION, MASTER, SCRIPT_LIST, sample_script
from retriever.engines import engine_list
from retriever.lib.repository import check_for_updates
from retriever.lib.lists import Category, get_lists
from retriever.lib.tools import choose_engine, get_opts, name_matches


def main():
    """This function launches the EcoData Retriever."""
    if len(sys.argv) == 1:
        # if no command line args are passed, launch GUI

        if not MASTER:
            check_for_updates(graphical=False if 'darwin' in platform.platform().lower() else True)
        lists = get_lists()
        
        from retriever.app.main import launch_app
        launch_app(lists)

    else:
        # otherwise, parse them

        script_list = SCRIPT_LIST()
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version=VERSION)
        
        subparsers = parser.add_subparsers(help='sub-command help', dest='command')
        
        install_parser = subparsers.add_parser('install', help='download and install dataset')
        install_parser.add_argument('dataset', help='dataset name', nargs='?', default=None)
        install_parser.add_argument('-e', '--engine', help='engine (%s)' % ', '.join('%s=%s' % (engine.abbreviation, engine.name) for engine in engine_list))
        install_parser.add_argument('-u', '--user', help='username for database connection, if applicable', nargs='?')
        install_parser.add_argument('-p', '--password', help='password for database connection, if applicable', nargs='?')
        install_parser.add_argument('--host', help='host for engine, if applicable', nargs='?')
        install_parser.add_argument('-o', '--port', help='port for engine, if applicable', nargs='?')
        install_parser.add_argument('-d', '--db', help='database for engine, if applicable', nargs='?')
        install_parser.add_argument('-f', '--file', help='file for engine, if applicable', nargs='?')
        install_parser.add_argument('--compile', help='force re-compile of script before downloading', action='store_true')
        install_parser.add_argument('--debug', help='run in debug mode', action='store_true')
        
        update_parser = subparsers.add_parser('update', help='download updated versions of scripts')
        
        gui_parser = subparsers.add_parser('gui', help='launch retriever in graphical mode')
        
        new_parser = subparsers.add_parser('new', help='create a new sample retriever script')
        new_parser.add_argument('filename', help='new script filename')

        help_parser = subparsers.add_parser('help', help='')
        
        args = parser.parse_args()

        if args.command == 'help':
            parser.parse_args(['-h'])
        
        
        if hasattr(args, 'compile') and args.compile:
            script_list = SCRIPT_LIST(force_compile=True)
        
        if args.command == 'update':
            check_for_updates(graphical=False)
            script_list = SCRIPT_LIST()
            return
            
        elif args.command == 'gui':
            lists = get_lists()

            from retriever.app.main import launch_app
            launch_app(lists)
            return

        elif args.command == 'new':
            f = open(args.filename, 'w')
            f.write(sample_script)
            f.close()
            
            return
        
        if args.dataset is None:
            all_scripts = set([script.shortname for script in script_list])
            all_tags = set(["ALL"] + 
                            [tag.strip().upper() for script in script_list for tagset in script.tags for tag in tagset.split('>')])
            print "Available datasets (%s):" % len(all_scripts)
            print '\t', '\t'.join(sorted(list(all_scripts), key=lambda s: s.lower()))
            print "Groups:"
            print '\t', '\t'.join(sorted(list(all_tags)))
            if len(all_scripts) == 0:
                print "Run 'retriever update' to download the latest scripts from the repository."
            return
        
        engine = choose_engine(get_opts(script_list, sys.argv[1:])) # TODO: update this
        
        if hasattr(args, 'debug') and args.debug: debug = True
        else: debug = False
        
        scripts = name_matches(script_list, args.dataset)
        
        for dataset in scripts:
            print "=> Installing", dataset.name
            try:
                dataset.download(engine, debug=debug)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print e

        print "Done!"
                                                            

if __name__ == "__main__":
    main()
