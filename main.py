"""EcoData Retriever Wizard

This module contains a list of all current Retriever scripts.

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""

import os
import sys
from retriever.lib.repository import check_for_updates
from retriever.lib.lists import Category, get_lists
from retriever.app.main import launch_app


def main():    
    check_for_updates()
    launch_app(get_lists())

if __name__ == "__main__":
    main()
