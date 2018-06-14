"""Contains DBMS-specific Engine implementations."""
import os

from retriever.lib.engine import Engine

engines = [
    "mysql",
    "postgres",
    "sqlite",
    "msaccess",
    "csvengine",
    "download_only",
    "jsonengine",
    "xmlengine"
]

engine_module_list = [
    __import__("retriever.engines." + module, fromlist="engines")
    for module in engines
    ]

engine_list = [module.engine() for module in engine_module_list]


def choose_engine(opts, choice=True):
    """Prompts the user to select a database engine"""
    if "engine" in list(opts.keys()):
        enginename = opts["engine"]
    elif opts["command"] == "download":
        enginename = "download"
    else:
        if not choice:
            return None
        print("Choose a database engine:")
        for engine in engine_list:
            if engine.abbreviation:
                abbreviation = "(" + engine.abbreviation + ") "
            else:
                abbreviation = ""
            print("    " + abbreviation + engine.name)
        enginename = input(": ")
    enginename = enginename.lower()

    engine = Engine()
    if not enginename:
        engine = engine_list[0]
    else:
        for thisengine in engine_list:
            if (enginename == thisengine.name.lower() or thisengine.abbreviation and
                    enginename == thisengine.abbreviation):
                engine = thisengine
    if 'table_name' in opts:
        if opts['table_name'] \
                and "{table}" not in opts['table_name'] \
                or "{db}" not in opts['table_name']:
            for opt in engine.required_opts:
                if opt[0] == 'table_name':
                    raise Exception('Accepted Table format '
                                    '{fom}'.format(fom=opt[2]))

    engine.opts = opts
    return engine
