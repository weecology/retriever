import os.path
import yaml
import json
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse, urlunparse, ParseResult

from retriever import HOME_DIR, SCRIPT_SEARCH_PATHS

def get_dps():
    """Load the list of data packages from datapackages.yml

    Checks all of the search paths for a datapackages.yml file and loads it into
    a dictionary.

    """
    for path in SCRIPT_SEARCH_PATHS:
        try:
            with open(os.path.join(path, "datapackages.yml"), 'r') as dp_file:
                dp_dict = yaml.safe_load(dp_file)
        except:
            pass
    return dp_dict

def load_dp_json(url):
    """Load a remote data package json file"""
    with urlopen(url) as url:
        dp = json.loads(url.read().decode())
    return dp

def replace_path(dp, url):
    """Replace relative data locations with absolute urls

    Data packages can either use relative paths or absolute urls to identify the
    locations of data: http://frictionlessdata.io/guides/data-package/#resources
    Convert all of the relative paths into absolute urls for consistent
    processing

    """
    for resource in dp['resources']:
        if 'path' in resource:
            resource['url'] = urljoin(url, resource['path'])
            del resource['path']
    return dp

def add_retriever_metadata(dp):
    """Add retriever specific metadata to a data package json file"""
    dp["retriever"] = "True"
    dp["retriever_minimum_version"] = "2.0.0"
    return dp

def replace_name(dp, dp_name):
    """Replace the original dp name with the name chosen for the retriever

    There is no system for ensuring that data package names are unique and
    descriptive, so we replace the name in the original dp with the name
    specified in datapackage.yml
    """
    dp["name"] = dp_name
    return dp

def match_types(dp):
    """Match the datapackage types to the retriever types

    The retriever still describes types using its old system instead of the
    official frictionless data spec. This converts frictionless data types to
    retriever types.

    """

    types = {'string': 'char',
             'number': 'double',
             'integer': 'int',
             'date': 'char'
    }

    for resource in dp['resources']:
        for field in resource['schema']['fields']:
            field['type'] = types.get(field['type'], field['type'])
    return dp

def download_dps_json(dps):
    """Download json files for each external data package"""
    scripts_dir = os.path.join(HOME_DIR, 'scripts')
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    for dp_name in dps:
        url = dps[dp_name]
        dp = load_dp_json(url)
        dp = replace_path(dp, url)
        dp = replace_name(dp, dp_name)
        dp = match_types(dp)
        dp = add_retriever_metadata(dp)
        write_path = os.path.join(scripts_dir,
                                  dp_name.replace('-', '_') + ".json")
        with open(write_path, 'w') as fp:
            json.dump(dp, fp, sort_keys=True, indent=4, separators=(',', ':'))
