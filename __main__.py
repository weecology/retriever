"""EcoData Retriever Wizard

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from imp import reload
import os
import platform
import sys
# sys removes the setdefaultencoding method at startup; reload to get it back
reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    # set default encoding to utf-8 to decode source text
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
        # if no command line args are passed, show the help options
        parser.parse_args(['-h'])

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
            check_for_updates()
            script_list = SCRIPT_LIST()
            return

        elif args.command == 'citation':
            if args.dataset is None:
                citation_path = os.path.join(os.path.split(__file__)[0], '../CITATION')
                print("\nCitation for retriever:\n")
                with open(citation_path) as citation_file:
                    print(citation_file.read())
            else:
                scripts = name_matches(script_list, args.dataset)
                for dataset in scripts:
                    print("\nDataset:  {}".format(dataset.name))
                    print("Citation:   {}".format(dataset.citation))
                    print("Description:   {}\n".format(dataset.description))

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

            # If scripts have never been downloaded there is nothing to list
            if not script_list:
                print("No scripts are currently available. Updating scripts now...")
                check_for_updates()
                print("\n\nScripts downloaded.\n")
                script_list = SCRIPT_LIST()

            all_scripts = []

            for script in script_list:
                if script.name:
                    if args.l!=None:
                        script_name = script.name + "\nShortname: " + script.shortname+"\n"
                        if script.tags:
                            script_name += "Tags: "+str([tag for tag in script.tags])+"\n"
                        not_found = 0
                        for term in args.l:
                            if script_name.lower().find(term.lower()) == -1:
                                not_found = 1
                                break
                        if not_found == 0:
                            all_scripts.append(script_name)
                    else:
                        script_name = script.shortname
                        all_scripts.append(script_name)

            all_scripts = sorted(all_scripts, key=lambda s: s.lower())

            print("Available datasets : {}\n".format(len(all_scripts)))

            if args.l==None:
                from retriever import lscolumns
                lscolumns.printls(sorted(all_scripts, key=lambda s: s.lower()))
            else:
                count = 1
                for script in all_scripts:
                    print ("%d. %s"%(count, script))
                    count += 1
            return

        engine = choose_engine(args.__dict__)

        if hasattr(args, 'debug') and args.debug:
            debug = True
        else:
            debug = False

        scripts = name_matches(script_list, args.dataset)
        if scripts:
            for dataset in scripts:
                print("=> Installing", dataset.name)
                try:
                    dataset.download(engine, debug=debug)
                    dataset.engine.final_cleanup()
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    print(e)
                    if debug: raise
            print("Done!")
        else:
            print("The dataset {} isn't currently available in the Retriever".format(args.dataset))
            print("Run 'retriever ls to see a list of currently available datasets")

if __name__ == "__main__":
    main()
