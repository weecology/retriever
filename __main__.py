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
from retriever import VERSION, MASTER, SCRIPT_LIST, sample_script, current_platform
from retriever.engines import engine_list
from retriever.lib.repository import check_for_updates
from retriever.lib.lists import Category, get_lists
from retriever.lib.tools import choose_engine, name_matches, reset_retriever
from retriever.lib.get_opts import parser


def main():
    """This function launches the EcoData Retriever."""
    if len(sys.argv) == 1:
        print "arguments required, use retriever -h for help"
        sys.exit(1)
 
    if len(sys.argv) > 1 and sys.argv[1] == 'gui':
        check_for_updates(graphical=False if current_platform == 'darwin' else True)
        lists = get_lists()

        from retriever.app.main import launch_app
        launch_app(lists)

    else:
        # otherwise, parse them

        script_list = SCRIPT_LIST()

        args = parser.parse_args()

        if args.quiet:
            sys.stdout = open(os.devnull, 'w')

        if args.command == 'help':
            parser.parse_args(['-h'])

        if hasattr(args, 'compile') and args.compile:
            script_list = SCRIPT_LIST(force_compile=True)

        if args.command == 'update':
            check_for_updates(graphical=False)
            script_list = SCRIPT_LIST()
            return

        elif args.command == 'citation':
            if args.dataset is None:
                citation_path = os.path.join(os.path.split(__file__)[0], '../CITATION')
                print "\nCitation for retriever:\n"
                with open(citation_path) as citation_file:
                    print citation_file.read()
            else:
                scripts = name_matches(script_list, args.dataset)
                for dataset in scripts:

                    print ("\nCitation:   {}".format(dataset.citation))
                    print ("Description:   {}\n".format(dataset.description))

            return

        elif args.command == 'gui':
            check_for_updates(graphical=False if current_platform == 'darwin' else True)
            lists = get_lists() 
            from retriever.app.main import launch_app
            launch_app(lists)            

            lists = get_lists()

            from retriever.app.main import launch_app
            launch_app(lists)
            return

        elif args.command == 'new':
            f = open(args.filename, 'w')
            f.write(sample_script)
            f.close()

            return

        elif args.command == 'reset':
            reset_retriever(args.scope)
            return

        if args.command == 'ls' or args.dataset is None:
            import lscolumns

            #If scripts have never been downloaded there is nothing to list
            if not script_list:
                print "No scripts are currently available. Updating scripts now..."
                check_for_updates(graphical=False)
                print "\n\nScripts downloaded.\n"
                script_list = SCRIPT_LIST()

            all_scripts = set([script.shortname for script in script_list])
            all_tags = set(["ALL"] +
                            [tag.strip().upper() for script in script_list for tagset in script.tags for tag in tagset.split('>')])

            print "Available datasets : {}".format(len(all_scripts))
            lscolumns.printls(sorted(list(all_scripts), key=lambda s: s.lower()))
            print "Groups:"
            lscolumns.printls(sorted(list(all_tags)))
            return

        engine = choose_engine(args.__dict__)

        if hasattr(args, 'debug') and args.debug: debug = True
        else: debug = False

        scripts = name_matches(script_list, args.dataset)
        if scripts:
            for dataset in scripts:
                print "=> Installing", dataset.name
                try:
                    dataset.download(engine, debug=debug)
                    dataset.engine.final_cleanup()
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print e
                    if debug: raise
            print "Done!"
        else:
            print "The dataset {} isn't currently available in the Retriever".format(args.dataset)
            print "Run 'retriever -ls to see a list of currently available datasets"

if __name__ == "__main__":
    main()
