"""EcoData Retriever Tools

This module contains miscellaneous classes and functions used in Retriever
scripts.

"""

import difflib
import os
import sys
import warnings
import unittest
import shutil
import os
from decimal import Decimal
from hashlib import md5

from retriever import HOME_DIR
from retriever.lib.models import *

warnings.filterwarnings("ignore")

TEST_ENGINES = dict()

def name_matches(scripts, arg):
    matches = []
    for script in scripts:
        if arg.lower() == script.shortname.lower(): return [script]
        max_ratio = max([difflib.SequenceMatcher(None, arg.lower(), factor).ratio() for factor in (script.shortname.lower(), script.name.lower(), script.filename.lower())] +
                        [difflib.SequenceMatcher(None, arg.lower(), factor).ratio() for factor in [tag.strip().lower() for tagset in script.tags for tag in tagset]]
                        )
        if arg.lower() == 'all':
            max_ratio = 1.0
        matches.append((script, max_ratio))
    matches = [m for m in sorted(matches, key=lambda m: m[1], reverse=True) if m[1] > 0.6]
    return [match[0] for match in matches]


def getmd5(lines):
    """Get MD5 value of a set of lines."""
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()

def final_cleanup(engine):
    """Perform final cleanup operations after all scripts have run."""
    pass


config_path = os.path.join(HOME_DIR, 'connections.config')


def get_saved_connection(engine_name):
    """Given the name of an engine, returns the stored connection for that engine
    from connections.config."""
    parameters = {}
    if os.path.isfile(config_path):
        config = open(config_path, "rb")
        for line in config:
            values = line.rstrip('\n').split(',')
            if values[0] == engine_name:
                try:
                    parameters = eval(','.join(values[1:]))
                except:
                    pass
    return parameters


def save_connection(engine_name, values_dict):
    """Saves connection information for an engine in connections.config."""
    lines = []
    if os.path.isfile(config_path):
        config = open(config_path, "rb")
        for line in config:
            if line.split(',')[0] != engine_name:
                lines.append('\n' + line.rstrip('\n'))
        config.close()
        os.remove(config_path)
        config = open(config_path, "wb")
    else:
        config = open(config_path, "wb")
    if "file" in values_dict:
        values_dict["file"] = os.path.abspath(values_dict["file"])
    config.write(engine_name + "," + str(values_dict))
    for line in lines:
        config.write(line)
    config.close()


def get_default_connection():
    """Gets the first (most recently used) stored connection from
    connections.config."""
    if os.path.isfile(config_path):
        config = open(config_path, "rb")
        default_connection = config.readline().split(",")[0]
        config.close()
        return default_connection
    else:
        return None


def choose_engine(opts, choice=True):
    """Prompts the user to select a database engine"""
    from retriever.engines import engine_list

    if "engine" in opts.keys():
        enginename = opts["engine"]
    elif opts["command"] == "download":
        enginename = "download"
    else:
        if not choice:
            return None
        print "Choose a database engine:"
        for engine in engine_list:
            if engine.abbreviation:
                abbreviation = "(" + engine.abbreviation + ") "
            else:
                abbreviation = ""
            print "    " + abbreviation + engine.name
        enginename = raw_input(": ")
    enginename = enginename.lower()

    engine = Engine()
    if not enginename:
        engine = engine_list[0]
    else:
        for thisengine in engine_list:
            if (enginename == thisengine.name.lower() or
                    thisengine.abbreviation and
                    enginename == thisengine.abbreviation):
                engine = thisengine

    engine.opts = opts
    return engine


def reset_retriever(scope):
    """Remove stored information on scripts, data, and connections"""

    warning_messages = {
        'all': "This will remove existing scripts, cached data, and information on database connections. Specifically it will remove the scripts and raw_data folders and the connections.config file in {}. Do you want to proceed? (y/N)\n",
        'scripts': "This will remove existing scripts. Specifically it will remove the scripts folder in {}. Do you want to proceed? (y/N)\n",
        'data': "This will remove raw data cached by the Retriever. Specifically it will remove the raw_data folder in {}. Do you want to proceed? (y/N)\n",
        'connections': "This will remove stored information on database connections. Specifically it will remove the connections.config file in {}. Do you want to proceed? (y/N)\n"
    }

    warn_msg = warning_messages[scope].format(HOME_DIR)
    confirm = raw_input(warn_msg)
    while not (confirm.lower() in ['y', 'n', '']):
        print("Please enter either y or n.")
        confirm = raw_input()
    if confirm.lower() == 'y':
        if scope in ['data', 'all']:
            shutil.rmtree(os.path.join(HOME_DIR, 'raw_data'))
        if scope in ['scripts', 'all']:
            shutil.rmtree(os.path.join(HOME_DIR, 'scripts'))
        if scope in ['connections', 'all']:
            try:
                os.remove(os.path.join(HOME_DIR, 'connections.config'))
            except:
                pass
