"""Data Retriever

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""
from __future__ import print_function
from __future__ import absolute_import

import os
import platform

from .lib import *
from retriever.lib.defaults import HOME_DIR
from retriever.lib.tools import set_proxy

current_platform = platform.system().lower()
if current_platform != 'windows':
    import pwd

# create the necessary directory structure for storing scripts/raw_data
# in the ~/.retriever directory
for dir in (HOME_DIR, os.path.join(HOME_DIR, 'raw_data'), os.path.join(HOME_DIR, 'scripts')):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            if (current_platform != 'windows') and os.getenv("SUDO_USER"):
                # owner of .retriever should be user even when installing
                # w/sudo
                pw = pwd.getpwnam(os.getenv("SUDO_USER"))
                os.chown(dir, pw.pw_uid, pw.pw_gid)
        except OSError:
            print("The Retriever lacks permission to access the ~/.retriever/ directory.")
            raise

set_proxy()
