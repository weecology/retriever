"""Database Toolkit auto-generator

Runs an automatic DbTk based on an input URL.
 
"""

from dbtk_ui import *

if __name__ == "__main__":
    name = raw_input("Name:")
    url = raw_input("URL:")
    me = AutoDbTk(name, url)
    if len(sys.argv) == 1:
        launch_wizard([me], ALL_ENGINES)
    else:
        final_cleanup(me.download())