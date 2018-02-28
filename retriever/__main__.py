"""Data Retriever Wizard

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from builtins import input
from imp import reload

from retriever.engines import engine_list, choose_engine
from retriever.lib.datapackage import create_json, edit_json, delete_json, get_script_filename
from retriever.lib.datasets import datasets, dataset_names, license
from retriever.lib.defaults import sample_script, CITATION, ENCODING, SCRIPT_SEARCH_PATHS
from retriever.lib.get_opts import parser
from retriever.lib.repository import check_for_updates
from retriever.lib.scripts import SCRIPT_LIST, get_script
from retriever.lib.engine_tools import name_matches, reset_retriever

encoding = ENCODING.lower()
# sys removes the setdefaultencoding method at startup; reload to get it back
reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding(encoding)


def main():
    """This function launches the Data Retriever."""
    if len(sys.argv) == 1:
        # if no command line args are passed, show the help options
        parser.parse_args(['-h'])

    else:
        # otherwise, parse them

        if not os.path.isdir(SCRIPT_SEARCH_PATHS[1]) and not \
                [f for f in os.listdir(SCRIPT_SEARCH_PATHS[-1])
                 if os.path.exists(SCRIPT_SEARCH_PATHS[-1])]:
            check_for_updates()
        script_list = SCRIPT_LIST()

        args = parser.parse_args()

        if args.command == "install" and not args.engine:
            parser.parse_args(['install', '-h'])

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
            check_for_updates(False)
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

        elif args.command == 'license':
            dataset_license = license(args.dataset)
            if dataset_license:
                print(dataset_license)
            else:
                print("There is no license information for {}".format(args.dataset))
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
            json_file = get_script_filename(args.dataset.lower())
            edit_json(json_file)
            return

        elif args.command == 'delete_json':
            # delete existing JSON script from home directory and or script directory if exists in current dir
            confirm = input("Really remove " + args.dataset.lower() +
                            " and all its contents? (y/N): ")
            if confirm.lower().strip() in ['y', 'yes']:
                json_file = get_script_filename(args.dataset.lower())
                delete_json(json_file)
            return

        if args.command == 'ls':
            # If scripts have never been downloaded there is nothing to list
            if not script_list:
                print("No scripts are currently available. Updating scripts now...")
                check_for_updates(False)
                print("\n\nScripts downloaded.\n")
            if not (args.l or args.k or (type(args.v) is list)):
                all_scripts = dataset_names()
                print("Available datasets : {}\n".format(len(all_scripts)))
                from retriever import lscolumns
                lscolumns.printls(all_scripts)
            
            elif type(args.v) is list:
                if args.v:
                    try:
                        all_scripts = [get_script(dataset) for dataset in args.v]
                    except KeyError:
                        all_scripts = []
                        print("Dataset(s) is not found.")
                else:
                    all_scripts = datasets()
                count = 1
                for script in all_scripts:
                    print("{}. {}\n{}\n{}\n{}\n".format(
                        count, script.title,
                        script.name,
                        script.keywords,
                        script.description,
                        str(script.licenses[0]['name']),
                        script.citation
                    ))
                    count += 1
 
            else:
                param_licenses = args.l if args.l else None
                keywords = args.k if args.k else None

                # search
                searched_scripts = datasets(keywords, param_licenses)
                if not searched_scripts:
                    print("No available datasets found")
                else:
                    print("Available datasets : {}\n".format(len(searched_scripts)))
                    count = 1
                    for script in searched_scripts:
                        print("{}. {}\n{}\n{}\n{}\n".format(
                                count, script.title,
                                script.name,
                                script.keywords,
                                str(script.licenses[0]['name'])
                        ))
                        count += 1
            return

        engine = choose_engine(args.__dict__)

        if hasattr(args, 'debug') and args.debug:
            debug = True
        else:
            debug = False
            sys.tracebacklimit = 0

        if hasattr(args, 'debug') and args.not_cached:
            engine.use_cache = False
        else:
            engine.use_cache = True

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
            print("Run 'retriever ls' to see a list of currently available datasets.")


if __name__ == "__main__":
    main()
