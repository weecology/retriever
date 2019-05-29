"""Data Retriever Tools

This module contains miscellaneous classes and functions used in Retriever
scripts.

"""
from __future__ import print_function

from future import standard_library

standard_library.install_aliases()

import difflib
import json
import platform
import shutil
import subprocess
import warnings

from hashlib import md5
from io import StringIO as NewFile
from retriever.lib.defaults import HOME_DIR, ENCODING

from retriever.lib.models import *
import xml.etree.ElementTree as ET

warnings.filterwarnings("ignore")

TEST_ENGINES = dict()


def create_home_dir():
    """Create Directory for retriever."""
    current_platform = platform.system().lower()
    if current_platform != 'windows':
        import pwd

    # create the necessary directory structure for storing scripts/raw_data
    # in the ~/.retriever directory
    required_dirs = [os.path.join(HOME_DIR, dirs)
                     for dirs in ['', 'raw_data', 'scripts']]
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


def name_matches(scripts, arg):
    """Check for a match of the script in available scripts

    if all, return the entire script list
    if the exact script is available, return that script
    if no exact script name detected, match the argument with keywords
    title and name of all scripts and return the closest matches
    """
    arg = arg.strip().lower()
    matches = []

    if not arg:
        raise ValueError("No dataset name specified")

    if arg == 'all':
        return scripts

    for script in scripts:
        if arg == script.name.lower():
            return [script]

    for script in scripts:
        script_match_ratio = difflib.SequenceMatcher(None, script.name, arg).ratio()
        if script_match_ratio > .53:
            matches.append((script.name, script_match_ratio))

    matches.sort(key=lambda x: -x[1])

    print("\nThe dataset \"{}\" "
          "isn't currently available in the Retriever.".format(arg))
    if matches:
        print("Did you mean:"
              " \n\t{}".format("\n\t".join([i[0] for i in matches])))


def final_cleanup(engine):
    """Perform final cleanup operations after all scripts have run."""
    pass


def reset_retriever(scope="all", ask_permission=True):
    """Remove stored information on scripts and data."""
    warning_messages = {
        'all': "\nThis will remove existing scripts and cached data."
               "\nSpecifically it will remove the scripts and raw_data folders "
               "in {}\nDo you want to proceed? (y/N)\n",
        'scripts': "\nThis will remove existing scripts."
                   + "\nSpecifically it will remove the scripts folder in {}."
                   + "\nDo you want to proceed? (y/N)\n",
        'data': "\nThis will remove raw data cached by the Retriever."
                + "\nSpecifically it will remove the raw_data folder in {}."
                + "\nDo you want to proceed? (y/N)\n"
    }

    path = os.path.normpath(HOME_DIR)
    rw_dir = os.path.normpath(os.path.join(HOME_DIR, 'raw_data'))
    sc_dir = os.path.normpath(os.path.join(HOME_DIR, 'scripts'))
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
                if os.path.exists(sc_dir):
                    shutil.rmtree(sc_dir)
    else:
        dataset_path = os.path.normpath(os.path.join(rw_dir, scope))
        if os.path.exists(dataset_path):
            shutil.rmtree(dataset_path)
        script = scope.replace('-', '_')
        script_path_py = os.path.normpath(os.path.join(sc_dir, script + ".py"))
        script_path_json = os.path.normpath(os.path.join(sc_dir, script + ".json"))
        if os.path.exists(script_path_py):
            os.remove(script_path_py)
            print("successfully removed the script {scp}".format(scp=scope))
        elif os.path.exists(script_path_json):
            os.remove(script_path_json)
            print("successfully removed the script {scp}".format(scp=scope))
        else:
            print("can't find script {scp}".format(scp=scope))


def json2csv(input_file, output_file=None, header_values=None):
    """Convert Json file to CSV.

    Function is used for only testing and can handle the file of the size.
    """
    file_out = open_fr(input_file, encoding=ENCODING)
    # set output file name and write header
    if output_file is None:
        output_file = os.path.splitext(os.path.basename(input_file))[0] + ".csv"
    csv_out = open_fw(output_file, encoding=ENCODING)
    if os.name == 'nt':
        outfile = csv.DictWriter(csv_out, dialect='excel', escapechar="\\",
                                 lineterminator='\n',
                                 fieldnames=header_values)
    else:
        outfile = csv.DictWriter(csv_out, dialect='excel',
                                 escapechar="\\", fieldnames=header_values)
    raw_data = json.loads(file_out.read())
    outfile.writeheader()

    for item in raw_data:
        outfile.writerow(item)
    file_out.close()
    subprocess.call(['rm', '-r', input_file])
    return output_file


def xml2csv(input_file, outputfile=None, header_values=None, row_tag="row"):
    """Convert xml to csv.

    Function is used for only testing and can handle the file of the size.
    """
    file_output = open_fr(input_file, encoding=ENCODING)
    # set output file name and write header
    if outputfile is None:
        outputfile = os.path.splitext(os.path.basename(input_file))[0] + ".csv"
    csv_out = open_fw(outputfile)
    if os.name == 'nt':
        csv_writer = csv.writer(csv_out, dialect='excel',
                                escapechar='\\', lineterminator='\n')
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
    lines = [line.strip().replace('\x00', '') for line in input_file]
    input_file.close()
    outfile = open_fw(file_path, encoding)
    lines.sort()
    for line in lines:
        outfile.write(line + "\n")
    outfile.close()
    return file_path


def sort_csv(filename, encoding=None):
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


def to_str(object, object_encoding=sys.stdout, object_decoder=ENCODING):
    if os.name == "nt":
        enc = object_encoding.encoding
        return str(object).encode(enc, errors='backslashreplace').decode(object_decoder)
    return str(object)


def get_script_version():
    """This function gets the version number of the scripts and returns them in array form."""
    from retriever.lib.scripts import SCRIPT_LIST

    modules = SCRIPT_LIST()
    scripts = []
    for module in modules:
        if module.public:
            if os.path.isfile('.'.join(module._file.split('.')[:-1]) + '.json') and module.version:
                module_name = module._name + '.json'
                scripts.append(','.join([module_name, str(module.version)]))
            elif os.path.isfile('.'.join(module._file.split('.')[:-1]) + '.py') and \
                    not os.path.isfile('.'.join(module._file.split('.')[:-1]) + '.json'):
                module_name = module._name + '.py'
                scripts.append(','.join([module_name, str(module.version)]))

    scripts = sorted(scripts, key=str.lower)
    return scripts


def set_proxy():
    """Check for proxies and makes them available to urllib."""
    proxies = ["https_proxy", "http_proxy", "ftp_proxy",
               "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY"]
    for proxy in proxies:
        if os.getenv(proxy):
            if os.environ[proxy]:
                for i in proxies:
                    os.environ[i] = os.environ[proxy]
                break
