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

    all_tags = set()
    for script in SCRIPT_LIST:
        all_tags.update(script.tags)
    all_tags = sorted(list(all_tags))

    lists = []
    lists.append(Category("All Datasets", SCRIPT_LIST))
    
    for tag in all_tags:
        lists.append(Category(tag, [script for script in SCRIPT_LIST
                                    if tag in script.tags]))

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
