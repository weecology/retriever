import os

try:
    from inquirer.themes import load_theme_from_dict
    INQUIRER_THEME = load_theme_from_dict(
        {"List": {
            "selection_color": "black_on_bright_green"
        }})
except ModuleNotFoundError:
    pass
from retriever._version import __version__

VERSION = __version__
COPYRIGHT = "Copyright (C) 2011-2016 Weecology University of Florida"
LICENSE = "MIT"
REPO_URL = "https://raw.githubusercontent.com/weecology/retriever-recipes/"
RETRIEVER_REPO_URL = "https://raw.githubusercontent.com/weecology/retriever/"
MAIN_BRANCH = REPO_URL + "main/"
RETRIEVER_MAIN_BRANCH = RETRIEVER_REPO_URL + "main/"
REPOSITORY = MAIN_BRANCH
RETRIEVER_REPOSITORY = RETRIEVER_MAIN_BRANCH
RDATASETS_URL = "https://github.com/vincentarelbundock/Rdatasets/raw/master/datasets.csv"
ENCODING = 'utf-8'
HOME_DIR = os.path.expanduser('~/.retriever/')
KAGGLE_TOKEN_PATH = os.path.expanduser('~/.kaggle/kaggle.json')
SOCRATA_BASE_URL = "http://api.us.socrata.com/api/catalog/v1"
RETRIEVER_DIR = 'retriever'
if os.path.exists(os.path.join(HOME_DIR, 'retriever_path.txt')):
    with open(os.path.join(HOME_DIR, 'retriever_path.txt'), 'r') as f:
        RETRIEVER_DIR = f.read()
RETRIEVER_RECIPES_DIR = 'retriever-recipes'
if os.path.exists(os.path.join(HOME_DIR, 'retriever_recipes_path.txt')):
    with open(os.path.join(HOME_DIR, 'retriever_recipes_path.txt'), 'r') as f:
        RETRIEVER_RECIPES_DIR = f.read()
SCRIPT_SEARCH_PATHS = [
    "./", 'scripts',
    os.path.join(RETRIEVER_DIR, 'scripts/'),
    os.path.join(HOME_DIR, 'socrata-scripts/'),
    os.path.join(HOME_DIR, 'rdataset-scripts/'),
    os.path.join(RETRIEVER_RECIPES_DIR, 'scripts/'),
    os.path.join(HOME_DIR, 'scripts/')
]
SCRIPT_WRITE_PATH = SCRIPT_SEARCH_PATHS[-1]
SOCRATA_SCRIPT_WRITE_PATH = SCRIPT_SEARCH_PATHS[3]
RDATASET_SCRIPT_WRITE_PATH = SCRIPT_SEARCH_PATHS[4]
RDATASET_PATH = os.path.normpath(
    os.path.join(RDATASET_SCRIPT_WRITE_PATH, 'datasets_url.json'))
DATA_SEARCH_PATHS = [
    "./",
    "{dataset}",
    "raw_data/{dataset}",
    os.path.join(HOME_DIR, 'raw_data/{dataset}'),
]
DATA_WRITE_PATH = DATA_SEARCH_PATHS[-1]
RETRIEVER_SCRIPTS = [
    "acton_lake.json", "amniote_life_hist.py", "bioclim.json", "iris.json", "predicts.py"
]
RETRIEVER_DATASETS = ["acton-lake", "amniote-life-hist", "bioclim", "iris", "predicts"]

# Provenance directory(to store committed datasets)
DEFAULT_PROVENANCE_DIR = os.path.expanduser('~/.retriever_provenance/')
PROVENANCE_DIR = os.environ.get('PROVENANCE_DIR', DEFAULT_PROVENANCE_DIR)

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
