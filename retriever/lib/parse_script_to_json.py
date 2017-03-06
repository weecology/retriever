import json
import os
from copy import copy

JSON_DIR = "../scripts/"
SCRIPT_DIR = "../scripts/"


def parse_script_to_json(script_file, location=SCRIPT_DIR):

    definition = open(os.path.join(location, script_file) + ".script", 'r')
    values = {}
    tables = []
    last_table = {}
    replace = []
    keys_to_ignore = ["template"]
    urls = {}
    values["retriever"] = "True"
    values["version"] = "1.0.0"
    values["retriever_minimum_version"] = "2.0.dev"

    for line in [str(line).strip() for line in definition]:
        if line and ':' in line and not line[0] == '#':

            split_line = [a.strip() for a in line.split(":")]
            key = split_line[0].lower()
            value = ':'.join(split_line[1:])

            if key == "name":
                values["title"] = value

            elif key == "shortname":
                values["name"] = value

            elif key == "description":
                values["description"] = value

            elif key == "tags":
                values["keywords"] = [v.strip() for v in value.split(",")]

            elif key == "url" or key == "ref":
                values["homepage"] = value

            elif key == "citation":
                values["citation"] = value

            elif key == "replace":
                # could be made a dict
                replace = [(v.split(',')[0].strip(), v.split(',')[1].strip())
                           for v in [val for val in value.split(';')]]

            elif key == "table":

                last_table = {}
                last_table["name"] = value.split(',')[0].strip()
                last_table["url"] = ','.join(value.split(',')[1:]).strip()
                last_table["schema"] = {}
                last_table["dialect"] = {}

                tables.append(last_table)

                urls[last_table["name"]] = last_table["url"]

                if replace:
                    last_table["dialect"]["replace_columns"] = replace

            elif key == "*column":
                if last_table:
                    vs = [v.strip() for v in value.split(',')]

                    if "fields" not in last_table["schema"]:
                        last_table["schema"]["fields"] = []

                    column = {}
                    column['name'] = vs[0]
                    column['type'] = vs[1]
                    if len(vs) > 2:
                        column['size'] = vs[2]

                    last_table["schema"]["fields"].append(copy(column))

            elif key == "*nulls":
                if last_table:
                    nulls = [eval(v) for v in [val.strip()
                                               for val in value.split(',')]]
                    last_table["dialect"]["nulls"] = nulls

            elif key == "*ct_column":
                if last_table:
                    last_table["schema"]["ct_column"] = value

            elif key == "*ct_names":
                if last_table:
                    last_table["schema"]["ct_names"] = [v.strip() for v in
                                                        value.split(',')]

            elif key[0] == "*":
                # attribute that should be applied to the most recently
                # declared table
                key = key[1:]
                if last_table:
                    try:
                        e = eval(value)
                    except:
                        e = str(value)

                    last_table["dialect"][key] = str(e)
            else:
                values[key] = str(value)

    values["resources"] = tables
    values["urls"] = urls

    if 'name' not in values:
        try:
            values['name'] = values['title']
        except:
            pass

    for key, value in values.items():
        if key in keys_to_ignore:
            values.pop(key, None)

    with open(os.path.join(location, values['name']) + '.json', 'w') as json_file:
        json_str = json.dumps(values, json_file, sort_keys=True, indent=4,
                              separators=(',', ': '))
        json_file.write(json_str + '\n')
        json_file.close()

    definition.close()

if __name__ == "__main__":
    for file in os.listdir(SCRIPT_DIR):
        if file[-6:] == "script":
            parse_script_to_json(file[:-7])
