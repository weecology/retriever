from builtins import str
import json
import sys
import pprint
if sys.version_info[0] < 3:
    from codecs import open
from retriever.lib.templates import TEMPLATES
from retriever.lib.models import Cleanup, Table, correct_invalid_value


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
    try:
        json_object = json.load(open(json_file + ".json", "r"))
    except ValueError as e:
        pass
    if type(json_object) is not dict:
        return
    if "retriever" not in json_object.keys():
        # Compile only files that have retriever key
        return

    values = {'urls': {}}

    keys_to_ignore = ["template"]

    required_fields = {
        "shortname":"name",
        "name":"title",
        "description": "description",
        "version": "version",
        "tables": "tables"
    }

    for (key, value) in json_object.items():

        if key == "title":
            values["name"] = str(value)

        elif key == "name":
            values["shortname"] = str(value)

        elif key == "description":
            values["description"] = str(value)

        elif key == "addendum":
            values["addendum"] = str(value)

        elif key == "homepage":
            values["ref"] = str(value)

        elif key == "citation":
            values["citation"] = str(value)

        elif key == "keywords":
            values["tags"] = value

        elif key == "version":
            values["version"] = str(value)

        elif key == "encoding":
            values["encoding"] = "\"" + str(value) + "\""
            # Adding the key 'encoding'

        elif key == "retriever_minimum_version":
            values["retriever_minimum_version"] = str(value)

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
