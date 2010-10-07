"""Database Toolkit Wizard

This module contains a list of all current DBTK scripts.

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""

import os
from dbtk.scripts.all import MODULE_LIST
from dbtk.lib.tools import AutoDbTk, DbTkList
from dbtk.lib.engines import ALL_ENGINES
from dbtk.ui.wizard import launch_wizard


DBTK_LIST = [module.main() for module in MODULE_LIST]
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
            line = line.rstrip("\n")
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
                
def main():
    launch_wizard(lists)

if __name__ == "__main__":
    main()
