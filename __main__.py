"""Data Retriever Wizard

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import input
from imp import reload
import os
import platform
import sys
# sys removes the setdefaultencoding method at startup; reload to get it back
reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    # set default encoding to latin-1 to decode source text
    sys.setdefaultencoding('latin-1')

from retriever import VERSION, SCRIPT_LIST, HOME_DIR, sample_script, CITATION
from retriever.engines import engine_list
from retriever.lib.repository import check_for_updates
from retriever.lib.tools import choose_engine, name_matches, reset_retriever
from retriever.lib.get_opts import parser
from retriever.lib.datapackage import create_json, edit_json


def main():
    """This function launches the Data Retriever."""
    if len(sys.argv) == 1:
        # if no command line args are passed, show the help options
        parser.parse_args(['-h'])

    else:
        # otherwise, parse them

        script_list = SCRIPT_LIST()

        args = parser.parse_args()

        if args.command == "install" and not args.engine:
            parser.parse_args(['install','-h'])

        if args.quiet:
            sys.stdout = open(os.devnull, 'w')

        if args.command == 'help':
            parser.parse_args(['-h'])

        if hasattr(args, 'compile') and args.compile:
            script_list = SCRIPT_LIST(force_compile=True)

        if args.command == 'defaults':
            for engine_item in engine_list:
                print("Default options for engine ", engine_item.name)
                for default_opts in engine_item.required_opts:
                    print(default_opts[0], " ", default_opts[2])
                print()
            return

        if args.command == 'update':
            check_for_updates()
            script_list = SCRIPT_LIST()
            return

        elif args.command == 'citation':
            if args.dataset is None:
                print("\nCitation for retriever:\n")
                print(CITATION)
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

        elif args.command == 'new_json':
            # create new JSON script
            create_json()
            return

        elif args.command == 'edit_json':
            # edit existing JSON script
            for json_file in [filename for filename in
                              os.listdir(os.path.join(HOME_DIR, 'scripts')) if filename[-5:] == '.json']:
                if json_file.lower().find(args.filename.lower()) != -1:
                    edit_json(json_file)
                    return
            raise Exception("File not found")

        elif args.command == 'delete_json':
            # delete existing JSON script
            for json_file in [filename for filename in
                              os.listdir(os.path.join(HOME_DIR, 'scripts')) if filename[-5:] == '.json']:
                if json_file.lower().find(args.dataset.lower()) != -1:
                    confirm = input("Really remove " + json_file +
                                    " and all its contents? (y/N): ")
                    if confirm.lower().strip() in ['y', 'yes']:
                        # raise Exception(json_file)
                        os.remove(os.path.join(HOME_DIR, 'scripts', json_file))
                        try:
                            os.remove(os.path.join(
                                HOME_DIR, 'scripts', json_file[:-4] + 'py'))
                        except:
                            # Not compiled yet
                            pass
                    return
            raise Exception("File not found")

        if args.command == 'ls':
            # If scripts have never been downloaded there is nothing to list
            if not script_list:
                print("No scripts are currently available. Updating scripts now...")
                check_for_updates()
                print("\n\nScripts downloaded.\n")
                script_list = SCRIPT_LIST()

            all_scripts = []

            for script in script_list:
                if script.shortname:
                    if args.l is not None:
                        script_name = script.name + "\nShortname: " + script.shortname + "\n"
                        if script.tags:
                            script_name += "Tags: " + \
                                str([tag for tag in script.tags]) + "\n"
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

            if args.l is None:
                from retriever import lscolumns
                lscolumns.printls(sorted(all_scripts, key=lambda s: s.lower()))
            else:
                count = 1
                for script in all_scripts:
                    print("%d. %s" % (count, script))
                    count += 1
            return

        engine = choose_engine(args.__dict__)

        if hasattr(args, 'debug') and args.debug:
            debug = True
        else:
            debug = False
            sys.tracebacklimit = 0

        if args.dataset is not None:
            scripts = name_matches(script_list, args.dataset)
        else:
            raise Exception("no dataset specified.")
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
                    if debug:
                        raise
            print("Done!")
        else:
            print("The dataset {} isn't currently available in the Retriever".format(
                args.dataset))
            print("Run 'retriever ls to see a list of currently available datasets")

if __name__ == "__main__":
    main()
