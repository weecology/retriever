script_template = """from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

name = "%s"
shortname = "%s"
description = "%s"
url = "%s"
urls = %s
tables = %s

SCRIPT = BasicTextTemplate(name=name, description=description,
                           ref=url, shortname=shortname, 
                           urls=urls, tables=tables)"""


def compile_script(script_file):
    definition = open(script_file + ".script", 'rb')
    
    values = {}
    urls = {}
    tables = {}
    last_table = ""
    
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
                        tables[last_table] = {}
                    tables[last_table]['cleanup'] = "Cleanup(correct_invalid_value, nulls=" + str(nulls) + ")"
            else:
                values[key] = value
        
    def get_value(key):
        try:
            return values[key]
        except KeyError:
            return ""
            
    table_desc = "{"
    for (key, value) in tables.items():
        table_desc += "'" + key + "': Table('" + key + "', "
        table_desc += ','.join([key + "=" + value for key, value, in value.items()])
        table_desc += ")"
    table_desc += "}"
    
    script_contents = (script_template % (
                                          get_value('name'),
                                          get_value('shortname'),
                                          get_value('description'),
                                          get_value('url'),
                                          str(urls),
                                          table_desc
                                          )
                       )
    
    new_script = open(script_file + '.py', 'wb')
    new_script.write(script_contents)
    new_script.close()
    
    definition.close()
