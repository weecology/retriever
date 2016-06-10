"""Contains DBMS-specific Engine implementations."""

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
