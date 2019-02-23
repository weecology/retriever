import os
from retriever.engines.sqlite import engine 
from retriever.lib.defaults import DATA_DIR
from retriever.lib.install import install_sqlite


def fetch(dataset, file='sqlite.db', table_name='{db}_{table}', data_dir=DATA_DIR):
    """Import a dataset into pandas data frames"""
    res_engine = install_sqlite(dataset, file=file, table_name=table_name)
    db_table_names = [name
                      for name, _ in res_engine.script_table_registry[dataset]]
    sqlite = engine()
    sqlite.opts = {"file": file, "table_name": table_name, "data_dir": data_dir}
    df = sqlite.fetch_tables(dataset, db_table_names)
    return df