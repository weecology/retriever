from builtins import str
import json
import sys
if sys.version_info[0] < 3:
    from codecs import open

script_templates = {
    "default": """#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(%s)""",

    "html_table": """#retriever
from retriever.lib.templates import HtmlTableTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = HtmlTableTemplate(%s)""",
}


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
            table_dict[
                'cleanup'] = "Cleanup(correct_invalid_value, nulls=" + str(val) + ")"

        elif key == "delimiter":
            table_dict[key] = "'" + str(val) + "'"
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


def compile_json(json_file):
    """
    Function to compile JSON script files to python scripts
    The scripts are created with `retriever create_json <script_name` using
    command line
    """
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

    values = {}
    values['urls'] = {}

    keys_to_ignore = ["template"]

    for (key, value) in json_object.items():

        if key == "title":
            values["name"] = "\"" + str(value) + "\""

        elif key == "name":
            values["shortname"] = "\"" + str(value) + "\""

        elif key == "description":
            values["description"] = "\"" + str(value) + "\""

        elif key == "addendum":
            values["addendum"] = "\"" + str(value) + "\""

        elif key == "homepage":
            values["ref"] = "\"" + str(value) + "\""

        elif key == "citation":
            values["citation"] = "\"" + str(value) + "\""

        elif key == "keywords":
            values["tags"] = value

        elif key == "version":
            values["version"] = "\"" + str(value) + "\""

        elif key == "retriever_minimum_version":
            values["retriever_minimum_version"] = "\"" + str(value) + "\""

        elif key == "resources":
            # Array of table objects
            tables = {}
            for table in value:
                # Maintain a dict for table keys and values
                table_dict = {}

                try:
                    values['urls'][table['name']] = table['url']
                except Exception as e:
                    print(e, "\nError in reading table: " + table)
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
    table_desc = "{"
    for (key, value) in tables.items():
        table_desc += "'" + key + "': Table('" + key + "', "
        table_desc += ','.join([key + "=" + str(value)
                                for key, value, in value.items()])
        table_desc += "),"
    if table_desc != '{':
        table_desc = table_desc[:-1]
    table_desc += "}"

    values["tables"] = table_desc

    script_desc = []
    for key, value in values.items():
        if key not in keys_to_ignore:
            script_desc.append(key + "=" + str(value))
    script_desc = (',\n' + ' ' * 27).join(script_desc)

    if 'template' in values.keys():
        template = values["template"]
    else:
        template = "default"
    script_contents = (script_templates[template] % script_desc)

    new_script = open(json_file + '.py', 'w', encoding='utf-8')
    new_script.write('# -*- coding: latin-1 -*-\n')
    new_script.write(script_contents)
    new_script.close()
