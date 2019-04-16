import os

from retriever._version import __version__

VERSION = __version__
COPYRIGHT = "Copyright (C) 2011-2016 Weecology University of Florida"
LICENSE = "MIT"
REPO_URL = "https://raw.githubusercontent.com/weecology/retriever/"
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
sample_script = """
{
    "description": "S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.",
    "homepage": "http://esapubs.org/archive/ecol/E084/093/default.htm",
    "name": "MammalLH",
    "resources": [
        {
            "dialect": {},
            "mediatype": "text/csv",
            "name": "species",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"
        }
    ],
    "title": "Mammal Life History Database - Ernest, et al., 2003"
}
"""
CITATION = """Morris, B.D. and E.P. White. 2013. The EcoData Retriever: improving access to
existing ecological data. PLOS ONE 8:e65848.
http://doi.org/doi:10.1371/journal.pone.0065848

@article{morris2013ecodata,
  title={The EcoData Retriever: Improving Access to Existing Ecological Data},
  author={Morris, Benjamin D and White, Ethan P},
  journal={PLOS One},
  volume={8},
  number={6},
  pages={e65848},
  year={2013},
  publisher={Public Library of Science}
  doi={10.1371/journal.pone.0065848}
}
"""
