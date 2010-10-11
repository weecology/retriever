import os
from dbtk import DBTK_LIST

DBTK_LIST = DBTK_LIST()


class DbTkList:
    """A categorical list of scripts."""
    def __init__(self, name, scripts):
        self.name = name
        self.scripts = scripts


def get_lists():
    
    lists = []
    lists.append(DbTkList("All Datasets", DBTK_LIST))
    
    # Check for .cat files
    files = os.listdir(os.getcwd())
    cat_files = [file for file in files if file[-4:] == ".cat"]
    for file in cat_files:
        cat = open(file, 'rb')
        scriptname = cat.readline().replace("\n", "")
        scripts = []
        for line in [line.replace("\n", "") for line in cat]:
            new_scripts = [script for script in DBTK_LIST
                           if script.shortname == line]
            for script in new_scripts:
                scripts.append(script)
        lists.append(DbTkList(scriptname, scripts))


    # Get list of additional datasets from dbtk.config file
    if os.path.isfile("scripts.config"):
        other_dbtks = []
        config = open("scripts.config", 'rb')
        for line in config:
            if line:
                line = line.strip('\n').strip('\r')
                values = line.split(', ')
                try:
                    dbname, tablename, url = (values[0], values[1], values[2])
                    other_dbtks.append(AutoDbTk(
                                                dbname + "." + tablename, 
                                                dbname, 
                                                tablename, 
                                                url))
                except:
                    pass

        if len(other_dbtks) > 0:
            lists.append(DbTkList("Custom", other_dbtks))
            for script in other_dbtks:
                lists[0].scripts.append(script)
                
    return lists
