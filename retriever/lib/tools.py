import csv
import io
import os
import sys

import xlrd
import pandas as pd

from retriever.lib.defaults import ENCODING


def excel_csv(src_path, path_to_csv, excel_info=None, encoding=ENCODING):
    """Convert an excel sheet to csv

    Read src_path excel file and write the excel sheet to path_to_csv
    excel_info contains the index of the sheet and the excel file name
    """
    if not excel_info:
        excel_info = [0]
    df = pd.read_excel(src_path, sheet_name=excel_info[0])
    df.to_csv(path_to_csv, sep=',', encoding=encoding, index=False, header=True)


def open_fr(file_name, encoding=ENCODING, encode=True):
    """Open file for reading respecting Python version and OS differences.

    Sets newline to Linux line endings on Windows and Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if os.name == 'nt':
        file_obj = io.open(file_name, 'r', newline='', encoding=encoding)
    else:
        if encode:
            file_obj = io.open(file_name, "r", encoding=encoding)
        else:
            file_obj = io.open(file_name, "r")
    return file_obj


def open_fw(file_name, encoding=ENCODING, encode=True):
    """Open file for writing respecting Python version and OS differences.

    Sets newline to Linux line endings on Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if encode:
        file_obj = io.open(file_name, 'w', newline='', encoding=encoding)
    else:
        file_obj = io.open(file_name, 'w', newline='')
    return file_obj


def open_csvw(csv_file):
    """Open a csv writer forcing the use of Linux line endings on Windows.

    Also sets dialect to 'excel' and escape characters to '\\'
    """
    if os.name == 'nt':
        csv_writer = csv.writer(csv_file,
                                dialect='excel',
                                escapechar='\\',
                                lineterminator='\n')
    else:
        csv_writer = csv.writer(csv_file, dialect='excel', escapechar='\\')
    return csv_writer


def to_str(object, object_encoding=sys.stdout, object_decoder=ENCODING):
    """Convert encoded values to string"""
    enc = object_encoding.encoding
    return str(object).encode(enc, errors='backslashreplace').decode(object_decoder)


def walk_relative_path(dir_name):
    """Return relative paths of files in the directory"""
    return [
        os.path.join(os.path.relpath(dir_, dir_name), file_name)
        for dir_, _, files in os.walk(dir_name, topdown=False)
        for file_name in files
    ]
