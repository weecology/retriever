import argparse
from retriever import VERSION, MASTER, SCRIPT_LIST, sample_script
from retriever.engines import engine_list


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=VERSION)
parser.add_argument('-q', '--quiet', help='suppress command-line output', action='store_true')

subparsers = parser.add_subparsers(help='sub-command help', dest='command')

install_parser = subparsers.add_parser('install', help='download and install dataset')
install_subparsers = install_parser.add_subparsers(help='engine-specific help', dest='engine')

install_parser.add_argument('--compile', help='force re-compile of script before downloading', action='store_true')
install_parser.add_argument('--debug', help='run in debug mode', action='store_true')

engine_parsers = {}
for engine in engine_list:
    engine_parser = install_subparsers.add_parser(engine.abbreviation, help=engine.name)
    engine_parser.add_argument('dataset', help='dataset name', nargs='?', default=None)
    abbreviations = set('h')

    for arg in engine.required_opts:
        arg_name, help_msg, default = arg[:3]
        potential_abbreviations = [char for char in arg_name if not char in abbreviations]
        if potential_abbreviations:
            abbreviation = potential_abbreviations[0]
            abbreviations.add(abbreviation)
        else: abbreviation = '-%s' % arg_name
        
        engine_parser.add_argument('--%s' % arg_name, '-%s' % abbreviation, help=help_msg, nargs='?', default=default)

    engine_parsers[engine.abbreviation] = engine_parser

download_parser = subparsers.add_parser(
                      'download',
                      help='download raw data files for a dataset',
                      parents=(engine_parsers['download'],),
                      conflict_handler='resolve')

update_parser = subparsers.add_parser('update', help='download updated versions of scripts')

gui_parser = subparsers.add_parser('gui', help='launch retriever in graphical mode')

new_parser = subparsers.add_parser('new', help='create a new sample retriever script')
new_parser.add_argument('filename', help='new script filename')

ls_parser = subparsers.add_parser('ls', help='display a list all available dataset scripts')

citation_parser = subparsers.add_parser('citation', help='view citation')
citation_parser.add_argument('dataset', help='dataset name', nargs='?', default=None)

reset_parser = subparsers.add_parser('reset', help='reset retriever: removes configation settings, scripts, and cached data')
reset_parser.add_argument('scope', help='things to reset: all, scripts, data, or connections',
                          choices=['all', 'scripts', 'data', 'connections'])

help_parser = subparsers.add_parser('help', help='')
