"""Database Toolkit Wizard

This module contains a list of all current DBTK scripts.

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""

import os
import sys
from dbtk.lib.repository import check_for_updates
from dbtk.lib.lists import DbTkList, get_lists
from dbtk.app.main import launch_app
from dbtk.wizard.main import launch_wizard


def main():    
    check_for_updates()
    launch_app(get_lists())
    
def wizard():
    check_for_updates()
    launch_wizard(get_lists())

if __name__ == "__main__":
    main()
