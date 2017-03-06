import argparse
from retriever import VERSION
from retriever.engines import engine_list


parser = argparse.ArgumentParser(prog="retriever")
parser.add_argument('-v', '--version', action='version', version=VERSION)
parser.add_argument('-q', '--quiet', help='suppress command-line output', action='store_true')

# ..............................................................
# subparsers
# ..............................................................

# retriever HELP
subparsers = parser.add_subparsers(help='sub-command help', dest='command')

# retriever download/install/update/new help
download_parser = subparsers.add_parser('download', help='download raw data files for a dataset')
install_parser = subparsers.add_parser('install', help='download and install dataset')
default_parser = subparsers.add_parser('defaults', help='displays default options')
update_parser = subparsers.add_parser('update', help='download updated versions of scripts')
new_parser = subparsers.add_parser('new', help='create a new sample retriever script')
new_json_parser = subparsers.add_parser('new_json', help='CLI to create retriever datapackage.json script')
edit_json_parser = subparsers.add_parser('edit_json', help='CLI to edit retriever datapackage.json script')
delete_json_parser = subparsers.add_parser('delete_json', help='CLI to remove retriever datapackage.json script')
ls_parser = subparsers.add_parser('ls', help='display a list all available dataset scripts')
citation_parser = subparsers.add_parser('citation', help='view citation')
reset_parser = subparsers.add_parser('reset', help='reset retriever: removes configation settings, scripts, and cached data')
help_parser = subparsers.add_parser('help', help='')

# ..............................................................
# subparsers with Arguments
# ..............................................................

citation_parser.add_argument('dataset', help='dataset name', nargs='?', default=None)
new_parser.add_argument('filename', help='new script filename')
edit_json_parser.add_argument('filename', help='script filename')
reset_parser.add_argument('scope', help='things to reset: all, scripts, data, or connections', choices=['all', 'scripts', 'data', 'connections'])
install_parser.add_argument('--compile', help='force re-compile of script before downloading', action='store_true')
install_parser.add_argument('--debug', help='run in debug mode', action='store_true')
download_parser.add_argument('dataset', help='dataset name')
ls_parser.add_argument('-l', help='verbose list of datasets containing following keywords (lists all when no keywords are specified)', nargs='*')
delete_json_parser.add_argument('dataset', help='dataset name')
# retriever Install {Engine} ..
# retriever download [options]
install_subparsers = install_parser.add_subparsers(help='engine-specific help', dest='engine')

for engine in engine_list:
    if engine.name == "Download Only":   # skip the Download engine and just add attributes
        pass
    else:
        engine_parser = install_subparsers.add_parser(engine.abbreviation, help=engine.name)
        engine_parser.add_argument('dataset', help='dataset name')

    abbreviations = set('h')

    for arg in engine.required_opts:
        arg_name, help_msg, default = arg[:3]
        potential_abbreviations = [char for char in arg_name if not char in abbreviations]
        if potential_abbreviations:
            abbreviation = potential_abbreviations[0]
            abbreviations.add(abbreviation)
        else:
            abbreviation = '-%s' % arg_name

        if engine.name == "Download Only" or abbreviation == "download":
            # add attributes to Download::  (download [-h] [--path [PATH]]
            # [--subdir [SUBDIR]]

            # subdir doesn't take any arguments, if included takes True if excluded takes False
            if arg_name.lower()== "subdir":
                download_parser.add_argument('--%s' % arg_name, '-%s' % abbreviation, help=help_msg, default=default, action='store_true')
                # parser.add_argument('--foo', action='store_const', const = False)
            else:
                # path must take arguments else it takes default "./"
                download_parser.add_argument('--%s' % arg_name, '-%s' % abbreviation, help=help_msg, nargs='?',
                                             default=default)
        else:
            engine_parser.add_argument('--%s' % arg_name, '-%s' % abbreviation, help=help_msg, nargs='?',
                                       default=default)
