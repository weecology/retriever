"""EcoData Retriever Tools

This module contains miscellaneous classes and functions used in Retriever
scripts.

"""


import json
import shutil
import difflib
import warnings
import xml.etree.ElementTree as ET
from hashlib import md5

from retriever import HOME_DIR
from retriever.lib.models import *

warnings.filterwarnings("ignore")

TEST_ENGINES = dict()


def name_matches(scripts, arg):
    matches = []
    for script in scripts:
        if arg.lower() == script.shortname.lower():
            return [script]
        max_ratio = max([difflib.SequenceMatcher(None, arg.lower(), factor).ratio() for factor in (script.shortname.lower(), script.name.lower(), script.filename.lower())] +
                        [difflib.SequenceMatcher(None, arg.lower(), factor).ratio() for factor in [tag.strip().lower() for tagset in script.tags for tag in tagset]]
                        )
        if arg.lower() == 'all':
            max_ratio = 1.0
        matches.append((script, max_ratio))
    matches = [m for m in sorted(matches, key=lambda m: m[1], reverse=True) if m[1] > 0.6]
    return [match[0] for match in matches]


def getmd5(lines):
    """Get MD5 value of a set of lines."""
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()


def unix_file_format(inputfile):
    inputfile = os.path.normpath(inputfile)
    """Convert a file to the unix standard"""
    try:
        with open(inputfile, 'rU') as infile:
            content = infile.read()
        infile.close()
        with open(inputfile, 'wb') as output:
            for line in content.splitlines():
                output.write(line + '\n')
        output.close()
    except IOError as e:
        print "I/O error({0}): {1} ".format(e.errno, e.strerror)
    return inputfile

def getmd5_u(file_path):
    """Get MD5 based on "rU"""
    files = []
    if os.path.isfile(file_path):
        files.append(file_path)
    elif os.path.isdir(file_path):
        for root, directories, filenames in os.walk(file_path):
            for filename in sorted(filenames):
                files.append(os.path.normpath(os.path.join(root, filename)))
    sum = md5()
    for file_path in files:
        lines = open(file_path, 'rU')
        sum = md5()
        for line in lines:
            sum.update(line)
    return sum.hexdigest()

def get_path_md5(file_path):
    """Get MD5 of a file, files in a directory or for specific files

    use 'rb' not 'rU'
    """
    files = []
    if os.path.isfile(file_path):
        files.append(file_path)
    elif os.path.isdir(file_path):
        for root, directories, filenames in os.walk(file_path):
            for filename in sorted(filenames):
                files.append(os.path.normpath(os.path.join(root, filename)))

    sum = md5()
    for file_path in files:
        lines = open(file_path, 'rb')
        sum = md5()
        for line in lines:
            sum.update(line)
    return sum.hexdigest()


def sort_file(file_path):
    """Sort file by line and return the file"""
    file_path = os.path.normpath(file_path)
    infile = open(file_path, 'rU')
    lines = [line for line in infile if line.strip()]
    infile.close()
    outfile = open(file_path, 'wb')
    lines.sort()
    for line in lines:
        outfile.write(line)
    outfile.close()
    return file_path


def sortcsv(filename):
    """Sort CSV rows and return the file"""
    filename = os.path.normpath(filename)
    input_file = open(filename, 'rU')
    csv_reader_infile = csv.reader(input_file)

    # The first entry is the header line
    infields = csv_reader_infile.next()

    #  write to a temporary file and sort it
    file_temp = open(os.path.normpath("tempfile"), 'wb')
    csv_writer = csv.writer(file_temp)
    for row in csv_reader_infile:
        csv_writer.writerow(row)
    file_temp.close()
    input_file.close()

    # sort the temp file
    sorted_txt = sort_file(os.path.normpath("tempfile"))

    # write sorted row content to csv filename with header "infields"
    tmp =open(sorted_txt, "rU")
    in_txt = csv.reader(tmp, delimiter=',')
    out_csv = csv.writer(open(filename, 'wb'))
    out_csv.writerow(infields)
    out_csv.writerows(in_txt)
    tmp.close()
    os.remove(os.path.normpath("tempfile"))
    return unix_file_format(filename)


def final_cleanup(engine):
    """Perform final cleanup operations after all scripts have run."""
    pass


config_path = os.path.join(HOME_DIR, 'connections.config')


def get_saved_connection(engine_name):
    """Given the name of an engine, returns the stored connection for that engine
    from connections.config."""
    parameters = {}
    if os.path.isfile(config_path):
        config = open(config_path, "rU")
        for line in config:
            values = line.rstrip('\n').split(',')
            if values[0] == engine_name:
                try:
                    parameters = eval(','.join(values[1:]))
                except:
                    pass
    return parameters


def save_connection(engine_name, values_dict):
    """Saves connection information for an engine in connections.config."""
    lines = []
    if os.path.isfile(config_path):
        config = open(config_path, "rb")
        for line in config:
            if line.split(',')[0] != engine_name:
                lines.append('\n' + line.rstrip('\n'))
        config.close()
        os.remove(config_path)
        config = open(config_path, "wb")
    else:
        config = open(config_path, "wb")
    if "file" in values_dict:
        values_dict["file"] = os.path.abspath(values_dict["file"])
    config.write(engine_name + "," + str(values_dict))
    for line in lines:
        config.write(line)
    config.close()


def get_default_connection():
    """Gets the first (most recently used) stored connection from
    connections.config."""
    if os.path.isfile(config_path):
        config = open(config_path, "rb")
        default_connection = config.readline().split(",")[0]
        config.close()
        return default_connection
    else:
        return None


def choose_engine(opts, choice=True):
    """Prompts the user to select a database engine"""
    from retriever.engines import engine_list

    if "engine" in opts.keys():
        enginename = opts["engine"]
    elif opts["command"] == "download":
        enginename = "download"
    else:
        if not choice:
            return None
        print "Choose a database engine:"
        for engine in engine_list:
            if engine.abbreviation:
                abbreviation = "(" + engine.abbreviation + ") "
            else:
                abbreviation = ""
            print "    " + abbreviation + engine.name
        enginename = raw_input(": ")
    enginename = enginename.lower()

    engine = Engine()
    if not enginename:
        engine = engine_list[0]
    else:
        for thisengine in engine_list:
            if (enginename == thisengine.name.lower() or
                    thisengine.abbreviation and
                    enginename == thisengine.abbreviation):
                engine = thisengine

    engine.opts = opts
    return engine


def reset_retriever(scope):
    """Remove stored information on scripts, data, and connections"""

    warning_messages = {
        'all': "This will remove existing scripts, cached data, and information on database connections. Specifically it will remove the scripts and raw_data folders and the connections.config file in {}. Do you want to proceed? (y/N)\n",
        'scripts': "This will remove existing scripts. Specifically it will remove the scripts folder in {}. Do you want to proceed? (y/N)\n",
        'data': "This will remove raw data cached by the Retriever. Specifically it will remove the raw_data folder in {}. Do you want to proceed? (y/N)\n",
        'connections': "This will remove stored information on database connections. Specifically it will remove the connections.config file in {}. Do you want to proceed? (y/N)\n"
    }

    warn_msg = warning_messages[scope].format(HOME_DIR)
    confirm = raw_input(warn_msg)
    while not (confirm.lower() in ['y', 'n', '']):
        print("Please enter either y or n.")
        confirm = raw_input()
    if confirm.lower() == 'y':
        if scope in ['data', 'all']:
            shutil.rmtree(os.path.join(HOME_DIR, 'raw_data'))
        if scope in ['scripts', 'all']:
            shutil.rmtree(os.path.join(HOME_DIR, 'scripts'))
        if scope in ['connections', 'all']:
            try:
                os.remove(os.path.join(HOME_DIR, 'connections.config'))
            except:
                pass


def is_valid_json(input_file):
    """Validate a json file"""
    try:
        fp = open(input_file, 'r')
        json.loads(fp.read())
    except ValueError:
        return False
    return True


def json2csv(input_file, output_file=None, header_values=None):
    """Convert Json file to CSV

    [
    {"User": "Alex", "Country": "US", "Age": "25"}
    ]
    Alex,US,25

    cross tab
    [
    {"User": "Alex", "Country": ["US","PT"], "Age": "25"},
    ]

    User,Country,Age
    Alex,US,25
    Alex,PT,25
    """
    try:
        fp = open(input_file, 'r')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

    if not is_valid_json(input_file):
        print "invalid json file"
        exit(1)

    # set output file name and write header
    if output_file is None:
        output_file = os.path.splitext(os.path.basename(input_file))[0] + "." + json
    outfile = open(output_file, 'w')
    outfile.write(",".join(header_values))

    raw_data = json.loads(fp.read())

    # lines in json file
    for item in raw_data:
        previous_list = [""]
        if header_values:
            # for each line, get values corresponding to the column name values
            for column_name in header_values:
                new_list = []

                # if column name has more than one value process ass a cross tab
                if type(item[column_name]) is list:
                    for child_item in item[column_name]:

                        # Create newlist with previous values and new cross-tab values added
                        for old_lines in previous_list:
                            temp = str(str(old_lines) + str(child_item) + ",")
                            new_list.append(temp)
                    previous_list = new_list

                else:
                    for p_strings in previous_list:
                        new_list.append("".join(str(p_strings) + str(item[column_name]) + ","))
                    previous_list = new_list

        for lines in previous_list:
            outfile.write("\n" + str(lines[0:-1]))
    outfile.close()


def xml2csv(input_file, output_file, header_values=None, row_tag="row"):
    """Convert xml to csv

    <root>
    <row>
       <User>Alex</User>
       <Country>US</Country>
       <Country>PT</Country>
       <Age>25</Age>
    </row>
    <row>
       <User>Ben</User>
       <Country>US</Country>S
       <Age>24</Age>
    </row>
    </root>

    User,Country,Age
    Alex,US,25
    Alex,Uk,25
    Ben,US,24
    """
    tree = ET.parse(input_file)
    root = tree.getroot()

    outfile = open(output_file, 'w')
    outfile.write(",".join(header_values))

    # lines in xml
    for rows in root.findall(row_tag):
        previous_list = [""]
        if header_values:
            # for each line, extract values for corresponding to column name
            for column_name in header_values:
                new_list = []
                # check if multiple values exist
                if len(rows.findall(column_name)) > 1:
                    for child_item in rows.findall(column_name):
                        # create new list with previous values and new cross-tab values added
                        for old_lines in previous_list:
                            temp = str(str(old_lines) + str(child_item.text) + ",")
                            new_list.append(temp)
                    previous_list = new_list
                else:
                    # no multiple values, just add available child
                    for p_strings in previous_list:
                        new_list.append("".join(str(p_strings) + str(rows.find(column_name).text) + ","))
                        previous_list = new_list
        else:
            print ("no header provided")
            exit()
        for lines in previous_list:
            outfile.write("\n" + str(lines[0:-1]))
