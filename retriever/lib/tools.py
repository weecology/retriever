import csv
import os
import sys

from retriever.lib.defaults import ENCODING


def open_fr(file_name, encoding=ENCODING):
    """Open file for reading respecting use newline"""
    file_obj = open(file_name, 'r', newline='', encoding=encoding)
    return file_obj


def open_fw(file_name, encoding=ENCODING):
    """Open file for writing respecting use newline"""
    file_obj = open(file_name, 'w', newline='', encoding=encoding)
    return file_obj


def open_csvw(csv_file):
    """Open a csv writer forcing the use of Linux line endings on Windows.

    Also sets dialect to 'excel' and escape characters to '\\'
    """
    if os.name == 'nt':
        csv_writer = csv.writer(csv_file, dialect='excel',
                                escapechar='\\', lineterminator='\n')
    else:
        csv_writer = csv.writer(csv_file, dialect='excel', escapechar='\\')
    return csv_writer


def to_str(object, object_encoding=sys.stdout, object_decoder=ENCODING):
    if os.name == "nt":
        enc = object_encoding.encoding
        return str(object).encode(enc, errors='backslashreplace').decode(object_decoder)
    return str(object)


def walk_relative_path(dir_name):
    """Return relative paths of files in the directory"""
    return [os.path.join(os.path.relpath(dir_, dir_name), file_name)
            for dir_, _, files in os.walk(dir_name, topdown=False)
            for file_name in files]
