"""Data Retriever Tools

This module contains miscellaneous classes and functions used in Retriever
scripts.

"""
import csv
import itertools
import json
import os
import platform
import shutil
import sqlite3 as sql
import subprocess
import warnings
from string import ascii_lowercase

try:
    # Geopanda installation is not smooth on the CI tests platforms
    import geopandas
except ModuleNotFoundError:
    pass
from pandas import json_normalize
from collections import OrderedDict
import xml.etree.ElementTree as ET
from hashlib import md5
from io import StringIO as NewFile
import h5py
import numpy as np
import pandas as pd
from PIL import Image

from retriever.lib.defaults import HOME_DIR, ENCODING
from retriever.lib.tools import open_fr, open_csvw, open_fw

warnings.filterwarnings("ignore")

TEST_ENGINES = dict()


def create_home_dir():
    """Create Directory for retriever."""
    current_platform = platform.system().lower()
    if current_platform != 'windows':
        import pwd  # pylint: disable=E0401

    # create the necessary directory structure for storing scripts/raw_data
    # in the ~/.retriever directory
    required_dirs = [
        os.path.join(HOME_DIR, dirs)
        for dirs in ['', 'raw_data', 'scripts', 'socrata-scripts', 'rdataset-scripts']
    ]
    for dir in required_dirs:
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
                if (current_platform != 'windows') and os.getenv("SUDO_USER"):
                    # owner of .retriever should be user even when installing
                    # w/sudo
                    pw = pwd.getpwnam(os.getenv("SUDO_USER"))
                    os.chown(dir, pw.pw_uid, pw.pw_gid)
            except OSError:
                print("The Retriever lacks permission to "
                      "access the ~/.retriever/ directory.")
                raise


def reset_retriever(scope="all", ask_permission=True):
    """Remove stored information on scripts and data."""
    warning_messages = {
        'all':
            "\nThis will remove existing scripts and cached data."
            "\nSpecifically it will remove the scripts, socrata-scripts," +
            " rdataset-scripts and raw_data folders in {}" +
            "\nDo you want to proceed? (y/N)\n",
        'scripts':
            "\nThis will remove existing scripts." +
            "\nSpecifically it will remove the scripts, socrata-scripts" +
            " and rdataset-scripts folders in {}." + "\nDo you want to proceed? (y/N)\n",
        'data':
            "\nThis will remove raw data cached by the Retriever." +
            "\nSpecifically it will remove the raw_data folder in {}." +
            "\nDo you want to proceed? (y/N)\n"
    }

    path = os.path.normpath(HOME_DIR)
    rw_dir = os.path.normpath(os.path.join(HOME_DIR, 'raw_data'))
    sc_dir = os.path.normpath(os.path.join(HOME_DIR, 'scripts'))
    soc_dir = os.path.normpath(os.path.join(HOME_DIR, 'socrata-scripts'))
    rd_dir = os.path.normpath(os.path.join(HOME_DIR, 'rdataset-scripts'))
    dirs = [sc_dir, soc_dir, rd_dir]

    if scope in ['all', 'scripts', 'data']:
        warn_msg = warning_messages[scope].format(path)
        if ask_permission:
            confirm = input(warn_msg)
            while not (confirm.lower() in ['y', 'n', '']):
                print("Please enter either y or n.")
                confirm = input()
        else:
            confirm = 'y'
        if confirm.lower() == 'y':
            if scope in ['data', 'all']:
                if os.path.exists(rw_dir):
                    shutil.rmtree(rw_dir)
            if scope in ['scripts', 'all']:
                for dir in dirs:
                    if os.path.exists(dir):
                        shutil.rmtree(dir)
    else:
        dataset_path = os.path.normpath(os.path.join(rw_dir, scope))
        if os.path.exists(dataset_path):
            shutil.rmtree(dataset_path)
        script = scope.replace('-', '_')
        script_path_py = os.path.normpath(os.path.join(sc_dir, script + ".py"))
        script_path_json = os.path.normpath(os.path.join(sc_dir, script + ".json"))
        socrata_script_path_json = os.path.normpath(
            os.path.join(soc_dir, script + ".json"))
        rdataset_script_path_json = os.path.normpath(
            os.path.join(rd_dir, script + ".json"))
        script_paths = [
            script_path_py, script_path_json, socrata_script_path_json,
            rdataset_script_path_json
        ]

        for script_path in script_paths:
            if os.path.exists(script_path):
                os.remove(script_path)
                print("successfully removed the script {scp}".format(scp=scope))
                return
        print("can't find script {scp}".format(scp=scope))


def json2csv(input_file,
             output_file=None,
             header_values=None,
             encoding=ENCODING,
             row_key=None):
    """Convert Json file to CSV."""
    file_out = open_fr(input_file, encoding=encoding)
    # set output file name and write header
    if output_file is None:
        output_file = os.path.splitext(os.path.basename(input_file))[0] + ".csv"
    csv_out = open_fw(output_file, encoding=encoding)
    if os.name == 'nt':
        outfile = csv.writer(csv_out,
                             dialect='excel',
                             escapechar="\\",
                             lineterminator='\n')
    else:
        outfile = csv.writer(csv_out, dialect='excel', escapechar="\\")

    raw_data = json.loads(file_out.read(), object_pairs_hook=OrderedDict)

    raw_data, header_values = walker(raw_data,
                                     row_key=row_key,
                                     header_values=header_values,
                                     rows=[],
                                     normalize=False)

    if isinstance(raw_data[0], dict):
        # row values are in a list of dictionaries
        raw_data = [list(row.values()) for row in raw_data]
    else:
        raw_data = [row.tolist() for row in raw_data]
    if header_values:
        outfile.writerow(header_values)
    outfile.writerows(raw_data)
    file_out.close()
    subprocess.call(['rm', '-r', input_file])
    return output_file


def walker(raw_data, row_key=None, header_values=None, rows=[], normalize=False):
    """
    Extract rows of data from json datasets
    """
    #  Handles the simple case, where row_key and column_key are not required
    if not (row_key or header_values):
        if isinstance(raw_data, dict):
            rows = pd.DataFrame([raw_data]).values
            header_values = raw_data.keys()
            return rows, header_values
        elif isinstance(raw_data, list):
            rows = pd.DataFrame(raw_data, columns=header_values).values
            # Create headers with values as alphabets like [a , b, c, d]
            num_columns = len(rows[0])
            header_values = list(
                itertools.chain(ascii_lowercase, (
                    ''.join(pair) for pair in itertools.product(ascii_lowercase, repeat=2)
                )))[:num_columns]
            return rows, header_values

    if isinstance(raw_data, dict):
        header_values = [i.lower() for i in header_values]
        # dict_keys = [i.lower() for i in dictionary.keys()]
        raw_data = {k.lower(): v for k, v in raw_data.items()}
        if header_values and (set(header_values).issubset(raw_data.keys())):
            if normalize:
                rows.extend(
                    json_normalize(
                        dict(
                            i for i in raw_data.items() if i[0] in header_values)).values)
            else:
                rows.extend([dict(i for i in raw_data.items() if i[0] in header_values)])

        elif raw_data.get(row_key):
            if normalize:
                rows.extend(json_normalize(raw_data[row_key]).values)
            else:
                rows, header_field = walker(raw_data[row_key],
                                            row_key,
                                            header_values,
                                            rows,
                                            normalize=True)
                return rows, header_values

        else:
            for item in raw_data.values():
                if isinstance(item, list):
                    for ls in item:
                        rows, header_field = walker(ls, row_key, header_values, rows)

    if isinstance(raw_data, list):
        for item in raw_data:
            rows, header_field = walker(item,
                                        row_key,
                                        header_values,
                                        rows,
                                        normalize=True)

    return rows, header_values


def sqlite2csv(input_file, output_file, table_name=None, encoding=ENCODING):
    """Convert sqlite database file to CSV."""
    conn = sql.connect(input_file)
    cursor = conn.cursor()
    table = pd.read_sql_query("SELECT * from %s" % table_name, conn)
    table.to_csv(output_file, index=False)
    cursor.close()
    conn.close()
    return output_file


def xml2csv_test(input_file, outputfile=None, header_values=None, row_tag="row"):
    """Convert xml to csv.

    Function is used for only testing and can handle the file of the size.
    """
    file_output = open_fr(input_file, encoding=ENCODING)
    # set output file name and write header
    if outputfile is None:
        outputfile = os.path.splitext(os.path.basename(input_file))[0] + ".csv"
    csv_out = open_fw(outputfile)
    if os.name == 'nt':
        csv_writer = csv.writer(csv_out,
                                dialect='excel',
                                escapechar='\\',
                                lineterminator='\n')
    else:
        csv_writer = csv.writer(csv_out, dialect='excel', escapechar='\\')

    v = file_output.read()
    csv_writer.writerow(header_values)
    tree = ET.parse(NewFile(v))
    root = tree.getroot()
    for rows in root.findall(row_tag):
        x = [name.text for name in header_values for name in rows.findall(name)]
        csv_writer.writerow(x)
    file_output.close()
    subprocess.call(['rm', '-r', input_file])
    return outputfile


def geojson2csv(input_file, output_file, encoding):
    """Convert Geojson file to csv.

    Function is used for testing only.
    """
    file = open(input_file)
    df = geopandas.read_file(file)
    df.to_csv(output_file, index=False)
    return output_file


def hdf2csv(file, output_file, data_name, data_type, encoding=ENCODING):
    if data_type == "csv":
        data = pd.read_hdf(file, data_name)
        data.to_csv(output_file, index=False)
    elif data_type == "image":
        file = h5py.File(file, 'r+')
        data = file.get(data_name)
        image = np.asarray(data)
        im = Image.fromarray(image)
        im.save(output_file)
        file.close()
    return output_file


def getmd5(data, data_type='lines', encoding='utf-8'):
    """Get MD5 of a data source."""
    checksum = md5()
    if data_type == 'lines':
        for line in data:
            checksum.update(line.encode(encoding))
        return checksum.hexdigest()
    files = []
    if data_type == 'file':
        files = [os.path.normpath(data)]
    if data_type == 'dir':
        directory_path = os.path.normpath(data)
        if not os.path.exists(directory_path):
            raise "Path not found, {path}".format(path=directory_path)
        for root, _, filenames in os.walk(os.path.normpath(directory_path)):
            for filename in sorted(filenames):
                files.append(os.path.normpath(os.path.join(root, filename)))
    for file_path in files:
        input_file = open(file_path, 'r', encoding=encoding)

        for line in input_file:
            checksum.update(str(line).encode(encoding))
    return checksum.hexdigest()


def sort_file(file_path, encoding=ENCODING):
    """Sort file by line and return the file.

    Function is used for only testing and can handle the file of the size.
    """
    file_path = os.path.normpath(file_path)
    input_file = open_fr(file_path, encoding)
    lines = [line.strip() for line in input_file]
    input_file.close()
    outfile = open_fw(file_path, encoding)
    lines.sort()
    for line in lines:
        outfile.write(line + "\n")
    outfile.close()
    return file_path


def sort_csv(filename, encoding=ENCODING):
    """Sort CSV rows minus the header and return the file.

    Function is used for only testing and can handle the file of the size.
    """
    filename = os.path.normpath(filename)
    input_file = open_fr(filename, encoding)
    csv_reader_infile = csv.reader(input_file, escapechar="\\")
    #  write the data to a temporary file and sort it
    temp_path = os.path.normpath("tempfile")
    temp_file = open_fw(temp_path, encoding)

    csv_writer = open_csvw(temp_file)
    i = 0
    infields = None
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
    sorted_txt = sort_file(temp_path, encoding)
    tmp = open_fr(sorted_txt, encoding)
    in_txt = csv.reader(tmp, delimiter=',', escapechar="\\")
    csv_file = open_fw(filename, encoding)
    csv_writer = open_csvw(csv_file)
    csv_writer.writerow(infields)
    csv_writer.writerows(in_txt)
    tmp.close()
    csv_file.close()
    os.remove(os.path.normpath(temp_path))
    return filename


def create_file(data, output='output_file'):
    """Write lines to file from a list."""
    output_file = os.path.normpath(output)
    with open(output_file, 'w') as testfile:
        for line in data:
            testfile.write(line)
            testfile.write("\n")
    return output_file


def file_2list(input_file):
    """Read in a csv file and return lines a list."""
    input_file = os.path.normpath(input_file)
    input_obj = open(input_file)
    abs_list = []
    for line in input_obj.readlines():
        abs_list.append(line.strip())
    return abs_list


def set_proxy():
    """Check for proxies and makes them available to urllib."""
    proxies = [
        "https_proxy", "http_proxy", "ftp_proxy", "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY"
    ]
    for proxy in proxies:
        if os.getenv(proxy):
            if os.environ[proxy]:
                for i in proxies:
                    os.environ[i] = os.environ[proxy]
                break


def xml2dict(data, node, level):
    """Convert xml to dict type.

    """
    vals = dict()
    for child in node:
        key = child.tag.strip()
        if key not in data:
            data[key] = []
        if child.attrib:
            if key not in vals:
                vals[key] = [child.attrib]
            else:
                vals[key].append(child.attrib)
        if child.text and child.text.strip():
            if key not in vals:
                vals[key] = [child.text]
            else:
                vals[key].append(child.text)
        if child:
            xml2dict(data, child, level + 1)

    for k in vals:
        if len(vals) == 1:
            for val in vals[k]:
                data[k].append(val)
        else:
            val = vals[k] if len(vals[k]) > 1 else vals[k][0]
            data[k].append(val)


def xml2csv(input_file, output_file, header_values=None, empty_rows=1, encoding=ENCODING):
    """Convert xml to csv."""

    tree = ET.parse(input_file)
    root = tree.getroot()
    dic = OrderedDict()
    xml2dict(dic, root, empty_rows)

    for empty_row in range(empty_rows):
        dic.pop("row")
    df = pd.DataFrame.from_dict(dic, orient='index')
    df = df.transpose()
    df.to_csv(output_file, index=False, encoding=encoding)
    return output_file
