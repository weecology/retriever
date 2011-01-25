"""Contains code for getting dataset lists from available datasets/categories."""

import os
from operator import attrgetter
from retriever.lib.models import *
from retriever.lib.templates import *


class Category:
    """A categorical list of scripts."""
    def __init__(self, name, scripts):
        self.name = name
        self.scripts = scripts


def get_lists():
    from retriever import SCRIPT_LIST
    SCRIPT_LIST = SCRIPT_LIST()
    SCRIPT_LIST.sort(key=attrgetter('name'))

    lists = []
    lists.append(Category("All Datasets", SCRIPT_LIST))
    
    # Check for .cat files
    files = os.listdir('categories')
    cat_files = [file for file in files if file[-4:] == ".cat"]
    for file in cat_files:
        cat = open(os.path.join('categories', file), 'rb')
        scriptname = cat.readline().replace('\n', '')
        scripts = []
        for line in [line.replace('\n', '') for line in cat]:
            new_scripts = [script for script in SCRIPT_LIST
                           if script.shortname == line]
            for script in new_scripts:
                scripts.append(script)
        scripts.sort(key=attrgetter('name'))
        lists.append(Category(scriptname, scripts))


    # Get list of additional datasets from scripts.config file
    if os.path.isfile("scripts.config"):
        other_scripts = []
        config = open("scripts.config", 'rb')
        for line in config:
            if line:
                try:
                    new_dataset = eval(line)
                    other_scripts.append(new_dataset)
                except:
                    pass
        
        other_scripts.sort(key=attrgetter('name'))
        if len(other_scripts) > 0:
            lists.append(Category("Custom", other_scripts))
            for script in other_scripts:
                lists[0].scripts.append(script)
    
    return lists
