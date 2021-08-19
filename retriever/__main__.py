"""Data Retriever

This module handles the CLI for the Data retriever.
"""
import os
import sys

try:
    import inquirer
    from retriever.lib.defaults import INQUIRER_THEME
except ModuleNotFoundError:
    pass

from retriever.engines import engine_list, choose_engine
from retriever.lib.datasets import datasets, dataset_names, license, dataset_verbose_list
from retriever.lib.defaults import sample_script, CITATION, SCRIPT_SEARCH_PATHS, LICENSE
from retriever.lib.engine_tools import reset_retriever
from retriever.lib.get_opts import parser
from retriever.lib.install import _install
from retriever.lib.repository import check_for_updates
from retriever.lib.scripts import SCRIPT_LIST, reload_scripts, name_matches, get_script_citation
from retriever.lib.create_scripts import create_package
from retriever.lib.provenance import commit, commit_log
from retriever.lib.socrata import socrata_autocomplete_search, socrata_dataset_info
from retriever.lib.rdatasets import display_all_rdataset_names


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
            if args.c:
                url = args.path
                script_list = SCRIPT_LIST()
                flag = 0

                for script in script_list:
                    for dataset in script.tables:
                        if script.tables[dataset].url == url:
                            flag = 1
                            break

                if flag == 1:
                    print("File already exist in dataset " + str(script.name))
                else:
                    print("Dataset is not avaliable, Please download")
                return
            if sum([args.f, args.d]) == 1:
                file_flag = bool(args.f)
                create_package(args.path, args.dt, file_flag, args.o, args.skip_lines,
                               args.e)
            else:
                print('Please use one and only one of the flags -f -d')
            return

        if args.command == 'ls':
            # scripts should never be empty because check_for_updates is run on SCRIPT_LIST init
            if not any([args.l, args.k, args.v, args.s, args.rdataset]):
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

            elif isinstance(args.s, list):
                try:
                    theme = INQUIRER_THEME
                except NameError:
                    print("To use retriever ls -s, install inquirer")
                    exit()

                name_list = socrata_autocomplete_search(args.s)
                print("Autocomplete suggestions : Total {} results\n".format(
                    len(name_list)))
                if len(name_list):
                    question = [
                        inquirer.List('dataset name',
                                      message='Select the dataset name',
                                      choices=name_list)
                    ]
                    answer = inquirer.prompt(question,
                                             theme=INQUIRER_THEME,
                                             raise_keyboard_interrupt=True)
                    dataset_name = answer['dataset name']
                    metadata = socrata_dataset_info(dataset_name)

                    print("Dataset Information of {}: Total {} results\n".format(
                        dataset_name, len(metadata)))

                    for i in range(len(metadata)):
                        print("{}. {}\n \tID : {}\n"
                              "\tType : {}\n"
                              "\tDescription : {}\n"
                              "\tDomain : {}\n \tLink : {}\n".format(
                                  i + 1, metadata[i]["name"], metadata[i]["id"],
                                  metadata[i]["type"],
                                  metadata[i]["description"][:50] + "...",
                                  metadata[i]["domain"], metadata[i]["link"]))

            elif args.rdataset:
                if not isinstance(args.p, list) and not args.all:
                    display_all_rdataset_names()
                elif not isinstance(args.p, list) and args.all:
                    display_all_rdataset_names(package_name='all')
                else:
                    display_all_rdataset_names(package_name=args.p)

            elif isinstance(args.v, list):
                dataset_verbose_list(args.v)

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
                        print(
                            "{count}. {title}\n{name}\n"
                            "{keywords}\n{licenses}\n".format(
                                count=count,
                                title=script.title,
                                name=script.name,
                                keywords=script.keywords,
                                licenses=str(script.licenses[0]['name']) if
                                script.licenses and len(script.licenses) else str('N/A'),
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
            if args.dataset.startswith(('socrata', 'rdataset')):
                scripts = True
            else:
                scripts = name_matches(script_list, args.dataset)
        else:
            raise Exception("no dataset specified.")
        if scripts:
            _install(vars(args), debug=debug, use_cache=use_cache)
            print("Done!")
        else:
            print("Run 'retriever ls' to see a list of currently available datasets.")


if __name__ == "__main__":
    main()
