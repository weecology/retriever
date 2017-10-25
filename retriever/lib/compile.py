import json
import sys
import pprint
import os
import imp
from builtins import str

if sys.version_info[0] < 3:
    from codecs import open
from retriever.lib.templates import TEMPLATES
from retriever.lib.models import Cleanup, Table, correct_invalid_value
from retriever.lib.defaults import SCRIPT_SEARCH_PATHS
from os.path import join, isfile, getmtime, exists

def MODULE_LIST(force_compile=False):
    """Load scripts from scripts directory and return list of modules."""
    modules = []
    loaded_scripts = []
    
    for search_path in [search_path for search_path in SCRIPT_SEARCH_PATHS if exists(search_path)]:
        to_compile = [
            file for file in os.listdir(search_path) if file[-5:] == ".json" and
            file[0] != "_" and (
                (not isfile(join(search_path, file[:-5] + '.py'))) or (
                    isfile(join(search_path, file[:-5] + '.py')) and (
                        getmtime(join(search_path, file[:-5] + '.py')) < getmtime(
                            join(search_path, file)))) or force_compile)]
        for script in to_compile:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_scripts:
                compiled_script = compile_json(join(search_path, script_name))
                setattr(compiled_script, "_file", os.path.join(search_path, script))
                setattr(compiled_script, "_name", script_name)
                modules.append(compiled_script)
                loaded_scripts.append(script_name)

        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_" and
                 '#retriever' in ' '.join(open(join(search_path, file), 'r').readlines()[:2]).lower()]


        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_scripts:
                loaded_scripts.append(script_name)
                file, pathname, desc = imp.find_module(script_name, [search_path])
                try:
                    new_module = imp.load_module(script_name, file, pathname, desc)
                    if hasattr(new_module, "retriever_minimum_version"):
                        # a script with retriever_minimum_version should be loaded
                        # only if its compliant with the version of the retriever
                        if not parse_version(VERSION) >= parse_version("{}".format(
                                new_module.retriever_minimum_version)):
                            print("{} is supported by Retriever version "
                                  "{}".format(script_name, new_module.retriever_minimum_version))

                            print("Current version is {}".format(VERSION))
                            continue
                    # if the script wasn't found in an early search path
                    # make sure it works and then add it
                    new_module.SCRIPT.download
                    setattr(new_module.SCRIPT, "_file", os.path.join(search_path, script))
                    setattr(new_module.SCRIPT, "_name", script_name)
                    modules.append(new_module.SCRIPT)

                except Exception as e:
                    sys.stderr.write("Failed to load script: %s (%s)\nException: %s \n" % (
                        script_name, search_path, str(e)))
    return modules


def SCRIPT_LIST(force_compile=False):
    scripts = [module for module in MODULE_LIST(force_compile)]
    
    return scripts 


def get_script(dataset):
    """Return the script for a named dataset."""
    scripts = {script.name: script for script in SCRIPT_LIST()}
    if dataset in scripts:
        return scripts[dataset]
    else:
        raise KeyError("No dataset named: {}".format(dataset))

def add_dialect(table_dict, table):
    """
    Reads dialect key of JSON script and extracts key-value pairs to store them
    in python script
    Contains properties such 'nulls', delimiter', etc
    """
    for (key, val) in table['dialect'].items():
        # dialect related key-value pairs
        # copied as is
        if key == "missingValues":
            table_dict['cleanup'] = Cleanup(correct_invalid_value, nulls=val)

        elif key == "delimiter":
            table_dict[key] = str(val)
        else:
            table_dict[key] = val


def add_schema(table_dict, table):
    """
    Reads schema key of JSON script and extracts values to store them in
    python script

    Contains properties related to table schema, such as 'fields' and cross-tab
    column name ('ct_column').
    """
    for (key, val) in table['schema'].items():
        # schema related key-value pairs

        if key == "fields":
            # fields = columns of the table

            # list of column tuples
            column_list = []
            for obj in val:
                # fields is a collection of JSON objects
                # (similar to a list of dicts in python)

                if "size" in obj:
                    column_list.append((obj["name"],
                                        (obj["type"], obj["size"])))
                else:
                    column_list.append((obj["name"],
                                        (obj["type"],)))

            table_dict["columns"] = column_list

        elif key == "ct_column":
            table_dict[key] = "'" + val + "'"

        else:
            table_dict[key] = val


def compile_json(json_file, debug=False):
    """
    Function to compile JSON script files to python scripts
    The scripts are created with `retriever new_json <script_name>` using
    command line
    """
    pp = pprint.PrettyPrinter(indent=4)
    json_object = {}
    source_encoding = "latin-1"
    try:
        json_object = json.load(open(json_file + ".json", "r"))
    except ValueError:
        pass
    if type(json_object) is not dict:
        return
    if "retriever" not in json_object.keys():
        # Compile only files that have retriever key
        return

    values = {'urls': {}}

    keys_to_ignore = ["template"]

    required_fields = {
        "title":"title",
        "name":"name",
        "description": "description",
        "version": "version",
        "tables": "tables"
    }

    for (key, value) in json_object.items():

        if key == "title":
            values["title"] = str(value)

        elif key == "name":
            values["name"] = str(value)

        elif key == "description":
            values["description"] = str(value)

        elif key == "addendum":
            values["addendum"] = str(value)

        elif key == "homepage":
            values["ref"] = str(value)

        elif key == "citation":
            values["citation"] = str(value)

        elif key == "licenses":
            values["licenses"] = value

        elif key == "keywords":
            values["keywords"] = value

        elif key == "version":
            values["version"] = str(value)

        elif key == "encoding":
            values["encoding"] = "\"" + str(value) + "\""
            # Adding the key 'encoding'
            source_encoding = str(value)

        elif key == "retriever_minimum_version":
            values["retriever_minimum_version"] = str(value)

        elif key == "message":
            values["message"] = "\"" + str(value) + "\""

        elif key == "resources":
            # Array of table objects
            tables = {}
            for table in value:
                # Maintain a dict for table keys and values
                table_dict = {}

                try:
                    values['urls'][table['name']] = table['url']
                except Exception as e:
                    print(e, "\nError in reading table: ")
                    pp.pprint(table)
                    continue

                if table["schema"] == {} and table["dialect"] == {}:
                    continue

                for (t_key, t_val) in table.items():

                    if t_key == "dialect":
                        add_dialect(table_dict, table)

                    elif t_key == "schema":
                        add_schema(table_dict, table)

                tables[table["name"]] = table_dict

        else:
            values[key] = value 

    # Create a Table object string using the tables dict
    table_obj = {}
    for (key, value) in tables.items():
        table_obj[key] = Table(key, **value)

    values["tables"] = table_obj

    if 'template' in values.keys():
        template = values["template"]
    else:
        template = "default"

    check=True
    fields = []
    for item in required_fields.keys(): 
        if item not in values:
            fields.append(required_fields[item])
            check = False

    if check:
        if debug:
            print("Values being passed to template: ")
            pp.pprint(values)
        return TEMPLATES[template](**values)
    else:
        print(json_file + " is missing parameters: \n")
        print(fields)
        sys.exit()
