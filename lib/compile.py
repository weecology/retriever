script_template = """from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

name = "%s"
shortname = "%s"
description = "%s"
urls = %s

SCRIPT = BasicTextTemplate(name=name, description=description,
                           shortname=shortname, urls=urls)"""


def compile_script(script_file):
    definition = open(script_file + ".script", 'rb')
    
    values = dict()
    urls = dict()
    
    for line in [line.strip() for line in definition]:
        if line and ':' in line and not line[0] == '#':
            split_line = [a.strip() for a in line.split(":")]
            key = split_line[0].lower()
            value = ':'.join(split_line[1:])
            if key == "table":
                table_name = value.split(',')[0].strip()
                table_url = ','.join(value.split(',')[1:]).strip()
                urls[table_name] = table_url
            else:
                values[key] = value
        
    def get_value(key):
        try:
            return values[key]
        except KeyError:
            return ""
    
    script_contents = (script_template % (
                                          get_value('name'),
                                          get_value('shortname'),
                                          get_value('description'),
                                          str(urls)
                                          )
                       )
    
    new_script = open(script_file + '.py', 'wb')
    new_script.write(script_contents)
    new_script.close()
    
    definition.close()
