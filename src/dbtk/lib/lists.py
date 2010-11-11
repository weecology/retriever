"""Contains code for getting dataset lists from available datasets/categories."""

import os
from operator import attrgetter
from dbtk.lib.models import *
from dbtk.lib.templates import *


class DbTkList:
    """A categorical list of scripts."""
    def __init__(self, name, scripts):
        self.name = name
        self.scripts = scripts


def get_lists():
    from dbtk import DBTK_LIST
    DBTK_LIST = DBTK_LIST()
    DBTK_LIST.sort(key=attrgetter('name'))

    lists = []
    lists.append(DbTkList("All Datasets", DBTK_LIST))
    
    # Check for .cat files
    files = os.listdir('categories')
    cat_files = [file for file in files if file[-4:] == ".cat"]
    for file in cat_files:
        cat = open(os.path.join('categories', file), 'rb')
        scriptname = cat.readline().replace('\n', '')
        scripts = []
        for line in [line.replace('\n', '') for line in cat]:
            new_scripts = [script for script in DBTK_LIST
                           if script.shortname == line]
            for script in new_scripts:
                scripts.append(script)
        scripts.sort(key=attrgetter('name'))
        lists.append(DbTkList(scriptname, scripts))


    # Get list of additional datasets from dbtk.config file
    if os.path.isfile("scripts.config"):
        other_dbtks = []
        config = open("scripts.config", 'rb')
        for line in config:
            if line:
                try:
                    new_dataset = eval(line)
                    other_dbtks.append(new_dataset)
                except:
                    pass
        
        other_dbtks.sort(key=attrgetter('name'))
        if len(other_dbtks) > 0:
            lists.append(DbTkList("Custom", other_dbtks))
            for script in other_dbtks:
                lists[0].scripts.append(script)
    
    return lists
