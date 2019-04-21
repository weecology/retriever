import argparse
import os

import argcomplete
from argcomplete.completers import ChoicesCompleter

from retriever.engines import engine_list
from retriever.lib.defaults import VERSION
from retriever.lib.scripts import SCRIPT_LIST

module_list = SCRIPT_LIST()
script_list = []
json_list = []
keywords_list = []
licenses_list = []

for module in module_list:
    script_list.append(module.name)
    if os.path.isfile('.'.join(module._file.split('.')[:-1]) + '.json'):
        json_list.append(module.name)

    if hasattr(module, "keywords"):
        # Add list of keywords to keywords_list
        if module.keywords:
            keywords_list += module.keywords

    if hasattr(module, "licenses"):
        # Append string to list of licenses_list
        if module.licenses:
            for dict_items in module.licenses:
                if dict_items['name']:
                    licenses_list.append(dict_items['name'])

# set of all possible licenses and keywords
licenses_options = set(licenses_list)
keywords_options = set(keywords_list)

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
autocreate_parser = subparsers.add_parser('autocreate', help='CLI to automatically create retriever scripts')
ls_parser = subparsers.add_parser('ls', help='display a list all available dataset scripts')
citation_parser = subparsers.add_parser('citation', help='view citation')
license_parser = subparsers.add_parser('license', help='view dataset license')
reset_parser = subparsers.add_parser('reset',
                                     help='reset retriever: removes configuration settings, scripts, and cached data')
help_parser = subparsers.add_parser('help', help='')

# ..............................................................
# subparsers with Arguments
# ..............................................................

citation_parser.add_argument('dataset', help='dataset name', nargs='?', default=None, choices=script_list + [None])
license_parser.add_argument('dataset', help='dataset name', nargs='?', default=None, choices=script_list + [None])
new_parser.add_argument('filename', help='new script filename')
edit_json_parser.add_argument('dataset', help='dataset name', choices=json_list)
reset_parser.add_argument('scope', help='things to reset: all, scripts or data').completer = \
    ChoicesCompleter(script_list + ['all', 'scripts', 'data'])
install_parser.add_argument('--compile', help='force re-compile of script before downloading', action='store_true')
install_parser.add_argument('--debug', help='run in debug mode', action='store_true')
install_parser.add_argument('--not-cached', help='overwrites local cache of raw data', action='store_true')
download_parser.add_argument('--debug', help='run in debug mode', action='store_true')
download_parser.add_argument('--not-cached', help='overwrites local cache of raw data', action='store_true')
download_parser.add_argument('-b', '--bbox', nargs=4,
                             help='Set bounding box xmin, ymin, xmax, ymax',
                             required=False)

ls_parser.add_argument('-l', help='search datasets with specific license(s)',
                       nargs='+').completer = ChoicesCompleter(list(licenses_options))
ls_parser.add_argument('-k', help='search datasets with keyword(s)',
                       nargs='+').completer = ChoicesCompleter(list(keywords_options))
ls_parser.add_argument('-v', help='verbose list of all datasets', nargs='*', default=False)

delete_json_parser.add_argument('dataset', help='dataset name', choices=json_list)
autocreate_parser.add_argument('path', help='path to the data file(s)')
autocreate_parser.add_argument('-dt', help='datatype for files', nargs='?', default='tabular', choices=['raster', 'vector', 'tabular'])
autocreate_parser.add_argument('-f', help='turn files into scripts', action='store_true')
autocreate_parser.add_argument('-d', help='turn a directory and subdirectories into scripts', action='store_true')
autocreate_parser.add_argument('-o', help='write scripts out to a designated directory', nargs='?', const='')
autocreate_parser.add_argument('--skip-lines', help='skip a set number of lines before processing data', nargs=1, type=int)
# retriever Install {Engine} ..
# retriever download [options]
install_subparsers = install_parser.add_subparsers(help='engine-specific help', dest='engine')

for engine in engine_list:
    if engine.name == "Download Only":
        # download engine follows, retriever download [dataset]
        download_parser.add_argument('dataset', help='dataset name').completer = ChoicesCompleter(script_list)
    else:
        engine_parser = install_subparsers.add_parser(engine.abbreviation, help=engine.name)
        engine_parser.add_argument('dataset', help='dataset name').completer = ChoicesCompleter(script_list)
        engine_parser.add_argument('-b', '--bbox', nargs=4,
                                   help='Set bounding box xmin, ymin, xmax, ymax',
                                   required=False)
        if engine.name == "JSON":
            engine_parser.add_argument('-p', '--pretty',
                                       help='Add indentation to json file', action='store_true',
                                       required=False)

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
            # add attributes to Download only engine
            download_parser.add_argument('--%s' % arg_name, '-%s' % abbreviation,
                                         help=help_msg, nargs='?', default=default)
        else:
            engine_parser.add_argument('--%s' % arg_name, '-%s' % abbreviation,
                                       help=help_msg, nargs='?', default=default)

argcomplete.autocomplete(parser)
