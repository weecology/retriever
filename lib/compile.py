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


def compile_script(script_file):
    definition = open(script_file + ".script", 'rb')

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
                        tables[table_name] = {'replace_columns': str(replace)}
            elif key == "*nulls":
                if last_table:
                    nulls = [eval(v) for v in [v.strip()
                                               for v in value.split(',')]]
                    try:
                        tables[last_table]
                    except KeyError:
                        if replace:
                            tables[last_table] = {
                                'replace_columns': str(replace)}
                        else:
                            tables[last_table] = {}
                    tables[last_table]['cleanup'] = "Cleanup(correct_invalid_value, nulls=" + str(nulls) + ")"
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

                    tables[last_table][key] = "'" + str(e) + "'"
            else:
                # general script attributes
                values[key] = '"' + value + '"'

    if 'shortname' not in values.keys():
        try:
            values['shortname'] = values['name']
        except:
            pass
    values['urls'] = str(urls)

    def get_value(key):
        try:
            return values[key]
        except KeyError:
            return ""

    table_desc = "{"
    for (key, value) in tables.items():
        table_desc += "'" + key + "': Table('" + key + "', "
        table_desc += ','.join([key + "=" + str(value)
                                for key, value, in value.items()])
        table_desc += "),"
    if table_desc != '{':
        table_desc = table_desc[:-1]
    table_desc += "}"

    values['tables'] = table_desc

    script_desc = []
    for key, value in values.items():
        if key == "url":
            key = "ref"
        if key not in keys_to_ignore:
            script_desc.append(key + "=" + str(value))
    script_desc = (',\n' + ' ' * 27).join(script_desc)

    if 'template' in values.keys():
        template = values["template"]
    else:
        template = "default"
    script_contents = (script_templates[template] % script_desc)

    new_script = open(script_file + '.py', 'wb')
    new_script.write(script_contents)
    new_script.close()

    definition.close()
