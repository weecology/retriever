"""Contains code for getting dataset lists from available datasets/categories."""

import os
from operator import attrgetter
from retriever.lib.models import *
from retriever.lib.templates import *


class Category:
    """A categorical list of scripts."""
    def __init__(self, name, scripts, children=[]):
        self.name = name
        self.scripts = scripts
        self.children = children


def tag_tree(all_tags):
    return [tag.strip() for tag in all_tags.split('>')] 
            

def tag_tree_desc(l):
    return ' > '.join(l)
    
    
def children(node, scripts, tags, level):
    lists = []
    for tag in tags:
        if len(tag) > 0:
            valid_scripts = []
            for script in scripts:
                for this_tag in script.tags:
                    this_tag_tree = tag_tree(this_tag)
                    if len(this_tag_tree[level:]) > 0 and tag[0] == this_tag_tree[level:][0]:
                        valid_scripts.append(script)

            lists.append(Category(tag[0], valid_scripts,
                                  children=children(tag, valid_scripts, 
                                                    [tag[1:] for tag in tags], 
                                                     level + 1)))
    return lists


def get_lists():
    # get a list of category tags from all scripts
    from retriever import SCRIPT_LIST
    SCRIPT_LIST = SCRIPT_LIST()
    SCRIPT_LIST.sort(key=attrgetter('name'))
    
    full_tags = set()
    tag_heads = set()
    for script in SCRIPT_LIST:
        for tag in script.tags:
            full_tags.update([tag])
            if len(tag_tree(tag)) > 0:
                tag_heads.update([tag_tree(tag)[0]])
    full_tags = sorted(list(full_tags))
    tag_heads = sorted(list(tag_heads))

    lists = []    
    for head in tag_heads:
        valid_scripts = [script for script in SCRIPT_LIST 
                                if len([tag for tag in script.tags
                                            if len(tag_tree(tag)) > 0 and 
                                            tag_tree(tag)[0] == head]) > 0]
        lists.append(Category(head, valid_scripts,
                              children=children(head, valid_scripts, 
                                                [tag_tree(tag)[1:] 
                                                 for tag in full_tags
                                                 if tag_tree(tag)[0] == head],
                                                1))
                     )

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
                
    choice_tree = Category("All Datasets", SCRIPT_LIST,
                           children=lists)
    
    return choice_tree
