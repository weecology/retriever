import os
from retriever.engines.sqlite import engine 
from retriever.lib.defaults import DATA_DIR
from retriever.lib.install import install_sqlite


def fetch(dataset, file=os.path.join(DATA_DIR, 'sqlite.db'),
          table_name='{db}_{table}'):
    """Import a dataset into pandas data frames"""

    install_sqlite(dataset, file=file, table_name=table_name)
    sqlite = engine()
    sqlite.opts = {"file": file, "table_name": table_name}
    df = sqlite.fetch_tables(dataset)
    return df
