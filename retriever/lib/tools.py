import csv
import imp
import io
import os
import sys
import struct

from gzip import FEXTRA, FNAME
from retriever.lib.defaults import  ENCODING


def get_gzip_filename(gzip_file):
    gf = gzip_file.fileobj
    pos = gf.tell()
    # Read archive size
    gf.seek(-4, 2)
    size = struct.unpack('<I', gf.read())[0]
    gf.seek(0)
    magic = gf.read(2)
    if magic != '\037\213':
        raise IOError('This is not a gzipped file')
    method, flag, mtime = struct.unpack("<BBIxx", gf.read(8))
    if not flag & FNAME:
        # If FNAME is set,
        # an original file name is present, terminated by a zero byte.
        # The name must consist of ISO 8859-1 (LATIN-1)
        # Not stored in the header, use the filename sans .gz
        gf.seek(pos)
        fname = gzip_file.name
        if fname.endswith('.gz'):
            fname = fname[:-3]
        return fname, size

    if flag & FEXTRA:
        # Read & discard the extra field, if present
        gf.read(struct.unpack("<H", gf.read(2)))

    # Read a null-terminated string containing the filename
    f_name = []
    while True:
        null__string = gf.read(1)
        if not null__string or null__string == '\000':
            break
        f_name.append(null__string)

    gf.seek(pos)
    return ''.join(f_name), size


def open_fr(file_name, encoding=ENCODING, encode=True):
    """Open file for reading respecting Python version and OS differences.

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
    """Open file for writing respecting Python version and OS differences.

    Sets newline to Linux line endings on Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if encode:
            file_obj = io.open(file_name, 'w', newline='', encoding=encoding)
        else:
            file_obj = io.open(file_name, 'w', newline='')
    else:
        file_obj = io.open(file_name, 'wb')
    return file_obj


def open_csvw(csv_file, encode=True):
    """Open a csv writer forcing the use of Linux line endings on Windows.

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
    return object   