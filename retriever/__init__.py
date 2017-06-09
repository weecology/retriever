"""Data Retriever

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import str

import io
import os
import sys
import csv
import platform

from retriever.lib.defaults import HOME_DIR, ENCODING

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


def open_fr(file_name, encoding=ENCODING, encode=True):
    """Open file for reading respecting Python version and OS differences

    Sets newline to Linux line endings on Windows and Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if os.name == 'nt':
            file_obj = io.open(file_name, 'r', newline='', encoding=encoding)
        else:
            if encode:
                file_obj = io.open(file_name, "r", encoding=encoding)
            else:
                file_obj = io.open(file_name, "r")
    else:
        file_obj = io.open(file_name, "r", encoding=encoding)
    return file_obj


def open_fw(file_name, encoding=ENCODING, encode=True):
    """Open file for writing respecting Python version and OS differences

    Sets newline to Linux line endings on Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if encode:
            file_obj = io.open(file_name, 'w', newline='', encoding=encoding)
        else:
            file_obj = io.open(file_name, 'w', newline='')
    else:
        file_obj = io.open(file_name, 'wb',)
    return file_obj


def open_csvw(csv_file, encode=True):
    """Open a csv writer forcing the use of Linux line endings on Windows

    Also sets dialect to 'excel' and escape characters to '\\'

    """
    if os.name == 'nt':
        csv_writer = csv.writer(csv_file, dialect='excel', escapechar='\\', lineterminator='\n')
    else:
        csv_writer = csv.writer(csv_file, dialect='excel', escapechar='\\')
    return csv_writer


def to_str(object, object_encoding=sys.stdout):
    if sys.version_info >= (3, 0, 0):
        enc = object_encoding.encoding
        return str(object).encode(enc, errors='backslashreplace').decode("latin-1")
    else:
        return object


def set_proxy():
    """Check for proxies and makes them available to urllib"""
    proxies = ["https_proxy", "http_proxy", "ftp_proxy",
               "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY"]
    for proxy in proxies:
        if os.getenv(proxy):
            if len(os.environ[proxy]) != 0:
                for i in proxies:
                    os.environ[i] = os.environ[proxy]
                break

set_proxy()
