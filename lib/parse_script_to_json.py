import json
import os


SCRIPT_DIR = "../scripts/"
JSON_DIR = "../scripts/"


def parse_script_to_json(script_file):
    definition = open(SCRIPT_DIR+script_file+'.script', 'rb')

    values = {}
    urls = {}
    tables = {}
    last_table = ""
    replace = []
    keys_to_ignore = ["template"]

    for line in [line.strip() for line in definition]:
        if line and ':' in line and not line[0] == '#':
            split_line = [a.strip() for a in line.split(":")]
            key = split_line[0].lower()
            value = ':'.join(split_line[1:])
            if key == "table":
                table_name = value.split(',')[0].strip()
                last_table = table_name
                table_url = ','.join(value.split(',')[1:]).strip()
                urls[table_name] = table_url
                if replace:
                    try:
                        tables[last_table]
                    except:
                        tables[table_name] = {'replace_columns': replace}
            elif key == "*nulls":
                if last_table:
                    nulls = [eval(v) for v in [v.strip()
                                               for v in value.split(',')]]
                    try:
                        tables[last_table]
                    except KeyError:
                        if replace:
                            tables[last_table] = {
                                'replace_columns': replace}
                        else:
                            tables[last_table] = {}
                    tables[last_table]['cleanup'] = {"nulls" :nulls}
            elif key == "replace":
                replace = [(v.split(',')[0].strip(), v.split(',')[1].strip())
                           for v in [v.strip() for v in value.split(';')]]
            elif key == "tags":
                values["tags"] = [v.strip() for v in value.split(',')]
            elif key == "*ct_names":
                tables[last_table]["ct_names"] = [v.strip()
                                                  for v in value.split(',')]
            elif key == "*column":
                if last_table:
                    vs = [v.strip() for v in value.split(',')]
                    column = [
                        (vs[0], (vs[1], vs[2]) if len(vs) > 2 else (vs[1],))]
                    try:
                        tables[last_table]
                    except KeyError:
                        tables[last_table] = {}

                    try:
                        tables[last_table]['columns'] += column
                    except KeyError:
                        tables[last_table]['columns'] = column
            elif key[0] == "*":
                # attribute that should be applied to the most recently
                # declared table
                if key[0] == "*":
                    key = key[1:]
                if last_table:
                    try:
                        tables[last_table]
                    except KeyError:
                        tables[last_table] = {}

                    try:
                        e = eval(value)
                    except:
                        e = str(value)

                    tables[last_table][key] = str(e) if e.__class__ != str else "'" + e + "'"
            elif key == ["ref","tags","urls"]:
                # general script attributes
                values[key] = value
            else:
                values[key] = str(value)

    if 'shortname' not in values.keys():
        try:
            values['shortname'] = values['name']
        except:
            pass
    values['urls'] =urls

    table_desc = {}
    for (key, value) in tables.items():
        table_desc[key]={}
        for v_key, v_value in value.items():
            table_desc[key][v_key] = v_value
    values['tables'] = table_desc

    for key, value in values.items():
        if key == "url":
            key = "ref"
        if key in keys_to_ignore:
            values.pop(key,None)

    with open(JSON_DIR+script_file + '.json', 'w') as json_file:
        json.dump(values,json_file,sort_keys=True, indent=4,
            separators=(',', ': '))

    definition.close()

if __name__=="__main__":
    for file in os.listdir(SCRIPT_DIR):
        if file[-6:]=="script":
            # print file
            parse_script_to_json(file[:-7])