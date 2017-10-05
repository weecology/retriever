import csv
import imp
import io
import os
import sys
from os.path import join, isfile, getmtime, exists

from pkg_resources import parse_version

from retriever.lib.defaults import SCRIPT_SEARCH_PATHS, VERSION, ENCODING


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
    else:
        return object

def sort_csv(filename):
    """Sort CSV rows minus the header and return the file.

    Function is used for only testing and can handle the file of the size.
    """
    filename = os.path.normpath(filename)
    input_file = open_fr(filename)
    csv_reader_infile = csv.reader(input_file, escapechar="\\")
    #  write the data to a temporary file and sort it
    temp_path = os.path.normpath("tempfile")
    temp_file = open_fw(temp_path)

    csv_writer = open_csvw(temp_file)
    i = 0
    for row in csv_reader_infile:
        if i == 0:
            # The first entry is the header line
            infields = row
            i += 1
        else:
            csv_writer.writerow(row)
    input_file.close()
    temp_file.close()

    # sort the temp file
    sorted_txt = sort_file(temp_path)
    tmp = open_fr(sorted_txt)
    in_txt = csv.reader(tmp, delimiter=',', escapechar="\\")
    csv_file = open_fw(filename)
    csv_writer = open_csvw(csv_file)
    csv_writer.writerow(infields)
    csv_writer.writerows(in_txt)
    tmp.close()
    csv_file.close()
    os.remove(os.path.normpath(temp_path))
    return filename

def json2csv(input_file, output_file=None, header_values=None):
    """Convert Json file to CSV.

    Function is used for only testing and can handle the file of the size.
    """
    file_out = open_fr(input_file, encode=False)
    # set output file name and write header
    if output_file is None:
        output_file = os.path.splitext(os.path.basename(input_file))[0] + ".csv"
    csv_out = open_fw(output_file, encode=False)
    if os.name == 'nt':
        outfile = csv.DictWriter(csv_out, dialect='excel', escapechar="\\", lineterminator='\n',
                                 fieldnames=header_values)
    else:
        outfile = csv.DictWriter(csv_out, dialect='excel', escapechar="\\", fieldnames=header_values)
    raw_data = json.loads(file_out.read())
    outfile.writeheader()

    for item in raw_data:
        outfile.writerow(item)
    file_out.close()
    os.system("rm -r {}".format(input_file))
    return output_file


def xml2csv(input_file, outputfile=None, header_values=None, row_tag="row"):
    """Convert xml to csv.

    Function is used for only testing and can handle the file of the size.
    """
    file_output = open_fr(input_file, encode=False)
    # set output file name and write header
    if outputfile is None:
        outputfile = os.path.splitext(os.path.basename(input_file))[0] + ".csv"
    csv_out = open_fw(outputfile)
    if os.name == 'nt':
        csv_writer = csv.writer(csv_out, dialect='excel', escapechar='\\', lineterminator='\n')
    else:
        csv_writer = csv.writer(csv_out, dialect='excel', escapechar='\\')

    v = file_output.read()
    csv_writer.writerow(header_values)
    tree = ET.parse(newfile(v))
    root = tree.getroot()
    for rows in root.findall(row_tag):
        x = [name.text for name in header_values for name in rows.findall(name)]
        csv_writer.writerow(x)
    file_output.close()
    os.system("rm -r {}".format(input_file))
    return outputfile