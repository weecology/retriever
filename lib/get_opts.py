import argparse
from retriever import VERSION, MASTER, SCRIPT_LIST, sample_script
from retriever.engines import engine_list


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=VERSION)

subparsers = parser.add_subparsers(help='sub-command help', dest='command')

install_parser = subparsers.add_parser('install', help='download and install dataset')
install_subparsers = install_parser.add_subparsers(help='engine-specific help', dest='engine')

install_parser.add_argument('--compile', help='force re-compile of script before downloading', action='store_true')
install_parser.add_argument('--debug', help='run in debug mode', action='store_true')

for engine in engine_list:
    engine_parser = install_subparsers.add_parser(engine.abbreviation, help=engine.name)
    engine_parser.add_argument('dataset', help='dataset name', nargs='?', default=None)
    for arg in engine.required_opts:
        name, help, default = arg[:3]
        engine_parser.add_argument('--%s' % name, help=help, nargs=1, default=default)            

update_parser = subparsers.add_parser('update', help='download updated versions of scripts')

gui_parser = subparsers.add_parser('gui', help='launch retriever in graphical mode')

new_parser = subparsers.add_parser('new', help='create a new sample retriever script')
new_parser.add_argument('filename', help='new script filename')

ls_parser = subparsers.add_parser('ls', help='display a list all available dataset scripts')

help_parser = subparsers.add_parser('help', help='')
