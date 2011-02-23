script_template = """from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

SCRIPT = BasicTextTemplate(%s)"""


def compile_script(script_file):
    definition = open(script_file + ".script", 'rb')
    
    values = {}
    urls = {}
    tables = {}
    last_table = ""
    replace = []
    
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
            elif key == "nulls":
                if last_table:
                    nulls = value.split(',')
                    try:
                        tables[last_table]
                    except KeyError:
                        if replace:
                            tables[last_table] = {'replace_columns': str(replace)}
                        else:
                            tables[last_table] = {}
                    tables[last_table]['cleanup'] = "Cleanup(correct_invalid_value, nulls=" + str(nulls) + ")"
            elif key == "replace":
                replace = [(v.split(',')[0].strip(), v.split(',')[1].strip())
                           for v in [v.strip() for v in value.split(';')]]
            elif key == "tags":
                values['tags'] = [v.strip() for v in value.split(',')]
            else:
                values[key] = '"' + value + '"'
        
    values['urls'] = str(urls)
    
    def get_value(key):
        try:
            return values[key]
        except KeyError:
            return ""
            
    table_desc = "{"
    for (key, value) in tables.items():
        table_desc += "'" + key + "': Table('" + key + "', "
        table_desc += ','.join([key + "=" + value for key, value, in value.items()])
        table_desc += "),"
    if table_desc != '{':
        table_desc = table_desc[:-1] 
    table_desc += "}"
    
    values['tables'] = table_desc
    
    script_desc = []
    for key, value in values.items():
        if key == "url":
            key = "ref"
        script_desc.append(key + "=" + str(value))
    script_desc = (',\n' + ' ' * 27).join(script_desc)
    
    script_contents = (script_template % script_desc)
    
    new_script = open(script_file + '.py', 'wb')
    new_script.write(script_contents)
    new_script.close()
    
    definition.close()
