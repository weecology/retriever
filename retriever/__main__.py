"""Data Retriever

This module handles the CLI for the Data retriever.
"""
import os
import sys

from retriever.engines import engine_list, choose_engine
from retriever.lib.datasets import datasets, dataset_names, license
from retriever.lib.defaults import sample_script, CITATION, SCRIPT_SEARCH_PATHS, LICENSE
from retriever.lib.engine_tools import reset_retriever
from retriever.lib.get_opts import parser
from retriever.lib.install import _install
from retriever.lib.repository import check_for_updates
from retriever.lib.scripts import SCRIPT_LIST, reload_scripts, get_script, name_matches, get_script_citation
from retriever.lib.create_scripts import create_package
from retriever.lib.provenance import commit, commit_log


def main():
    """This function launches the Data Retriever."""
    if len(sys.argv) == 1:
        # if no command line args are passed, show the help options
        parser.parse_args(['-h'])

    else:
        # otherwise, parse them
        args = parser.parse_args()

        reset_or_update = args.command in ["reset", "update"]
        if (not reset_or_update and not os.path.isdir(SCRIPT_SEARCH_PATHS[1]) and not [
                f for f in os.listdir(SCRIPT_SEARCH_PATHS[-1])
                if os.path.exists(SCRIPT_SEARCH_PATHS[-1])
        ]):
            check_for_updates()
            reload_scripts()
        script_list = SCRIPT_LIST()

        if args.command == "install" and not args.engine:
            parser.parse_args(["install", "-h"])

        if args.quiet:
            sys.stdout = open(os.devnull, "w")

        if args.command == "help":
            parser.parse_args(["-h"])

        if hasattr(args, "compile") and args.compile:
            script_list = reload_scripts()

        if args.command == "defaults":
            for engine_item in engine_list:
                print("Default options for engine ", engine_item.name)
                for default_opts in engine_item.required_opts:
                    print(default_opts[0], " ", default_opts[2])
                print()
            return

        if args.command == "update":
            check_for_updates()
            reload_scripts()
            return

        if args.command == "citation":
            if args.dataset is None:
                print("\nCitation for retriever:\n")
                print(CITATION)
            else:
                citations = get_script_citation(args.dataset)
                for citation in citations:
                    print("Citation:   {}".format(citation))
            return

        if args.command == 'license':
            if args.dataset is None:
                print(LICENSE)
            else:
                dataset_license = license(args.dataset)
                if dataset_license:
                    print(dataset_license)
                else:
                    print("There is no license information for {}".format(args.dataset))
            return

        if args.command == 'new':
            f = open(args.filename, 'w')
            f.write(sample_script)
            f.close()

            return

        if args.command == 'reset':
            reset_retriever(args.scope)
            return

        if args.command == 'autocreate':
            if sum([args.f, args.d]) == 1:
                file_flag = bool(args.f)
                create_package(args.path, args.dt, file_flag, args.o, args.skip_lines,
                               args.e)
            else:
                print('Please use one and only one of the flags -f -d')
            return

        if args.command == 'ls':
            # scripts should never be empty because check_for_updates is run on SCRIPT_LIST init
            if not (args.l or args.k or isinstance(args.v, list)):
                all_scripts = dataset_names()
                from retriever import lscolumns

                all_scripts_combined = []
                for dataset in all_scripts['offline']:
                    all_scripts_combined.append((dataset, True))
                for dataset in all_scripts['online']:
                    if dataset in all_scripts['offline']:
                        continue
                    all_scripts_combined.append((dataset, False))
                all_scripts_combined = sorted(all_scripts_combined, key=lambda x: x[0])
                print("Available datasets : {}\n".format(len(all_scripts_combined)))
                lscolumns.printls(all_scripts_combined)
                print("\nThe symbol * denotes the online datasets.")
                print("To see the full list of available online datasets, visit\n"
                      "https://github.com/weecology/retriever-recipes.")

            elif isinstance(args.v, list):
                online_scripts = []
                if args.v:
                    try:
                        all_scripts = [get_script(dataset) for dataset in args.v]
                    except KeyError:
                        all_scripts = []
                        print("Dataset(s) is not found.")
                else:
                    scripts = datasets()
                    all_scripts = scripts['offline']
                    online_scripts = scripts['online']
                count = 1
                if not args.v:
                    print("Offline datasets : {}\n".format(len(all_scripts)))
                for script in all_scripts:
                    print("{count}. {title}\n {name}\n"
                          "{keywords}\n{description}\n"
                          "{licenses}\n{citation}\n"
                          "".format(
                              count=count,
                              title=script.title,
                              name=script.name,
                              keywords=script.keywords,
                              description=script.description,
                              licenses=str(script.licenses[0]['name']),
                              citation=script.citation,
                          ))
                    count += 1

                count = 1
                offline_scripts = [script.name for script in all_scripts]
                set_online_scripts = []
                for script in online_scripts:
                    if script in offline_scripts:
                        continue
                    set_online_scripts.append(script)
                if not args.v:
                    print("Online datasets : {}\n".format(len(set_online_scripts)))
                for script in set_online_scripts:
                    print("{count}. {name}".format(count=count, name=script))
                    count += 1
            else:
                param_licenses = args.l if args.l else None
                keywords = args.k if args.k else None

                # search
                searched_scripts = datasets(keywords, param_licenses)
                offline_mesg = "Available offline datasets : {}\n"
                online_mesg = "Available online datasets : {}\n"
                if not searched_scripts:
                    print("No available datasets found")
                else:
                    print(offline_mesg.format(len(searched_scripts['offline'])))
                    count = 1
                    for script in searched_scripts['offline']:
                        print("{count}. {title}\n{name}\n"
                              "{keywords}\n{licenses}\n".format(
                                  count=count,
                                  title=script.title,
                                  name=script.name,
                                  keywords=script.keywords,
                                  licenses=str(script.licenses[0]['name']),
                              ))
                        count += 1

                    count = 1
                    searched_scripts_offline = [
                        script.name for script in searched_scripts["offline"]
                    ]
                    searched_scripts_online = []
                    for script in searched_scripts['online']:
                        if script in searched_scripts_offline:
                            continue
                        searched_scripts_online.append(script)
                    print(online_mesg.format(len(searched_scripts_online)))
                    for script in searched_scripts_online:
                        print("{count}. {name}".format(count=count, name=script))
                        count += 1
            return
        if args.command == 'commit':
            commit(
                dataset=args.dataset,
                path=os.path.normpath(args.path) if args.path else None,
                commit_message=args.message,
            )
            return
        if args.command == 'log':
            commit_log(dataset=args.dataset)
            return

        engine = choose_engine(args.__dict__)

        if hasattr(args, 'debug') and args.debug:
            debug = True
        else:
            debug = False
            sys.tracebacklimit = 0

        if hasattr(args, 'debug') and args.not_cached:
            use_cache = False
        else:
            use_cache = True
        engine.use_cache = use_cache
        if args.dataset is not None:
            scripts = name_matches(script_list, args.dataset)
        else:
            raise Exception("no dataset specified.")
        if scripts:
            if args.dataset.endswith('.zip') or (hasattr(args, 'hash_value') and
                                                 args.hash_value):
                _install(vars(args), debug=debug, use_cache=use_cache)
                return
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
