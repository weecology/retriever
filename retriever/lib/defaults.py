import os
from retriever._version import __version__

VERSION = __version__
COPYRIGHT = "Copyright (C) 2011-2016 Weecology University of Florida"
REPO_URL = "https://raw.github.com/weecology/retriever/"
MASTER_BRANCH = REPO_URL + "master/"
REPOSITORY = MASTER_BRANCH
ENCODING = 'ISO-8859-1'

HOME_DIR = os.path.expanduser('~/.retriever/')
SCRIPT_SEARCH_PATHS = [
    "./",
    'scripts',
    os.path.join(HOME_DIR, 'scripts/')
]
SCRIPT_WRITE_PATH = SCRIPT_SEARCH_PATHS[-1]
DATA_SEARCH_PATHS = [
    "./",
    "{dataset}",
    "raw_data/{dataset}",
    os.path.join(HOME_DIR, 'raw_data/{dataset}'),
]
DATA_WRITE_PATH = DATA_SEARCH_PATHS[-1]

# Create default data directory
DATA_DIR = '.'
