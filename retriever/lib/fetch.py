import os
import sys
from retriever.engines.sqlite import engine
from retriever.lib.defaults import DATA_DIR
from retriever.lib.download import download
from retriever.lib.install import install_sqlite



def fetch(dataset, file= os.path.join(DATA_DIR, 'sqlite.db'),
        table_name=None):
    """Import a dataset into pandas data frames

    Imports each table in the dataset into a data frame and stores the data frames
    together in a dict.

    Parameters
    ----------
    dataset : str
        Name of dataset
    
    file : str
        Path to sqlite file

    table_name : str
        Specific table name to fetch

    Returns
    -------
    dict
        with table names as key and dataframes as value

    Example
    -------
    data = rt.fetch('portal')
    data['portal_surveys']

    """

    if table_name:
        install_sqlite(dataset, file=file, table_name=table_name)
    else:
        install_sqlite(dataset, file=file)
    df = engine.fetch_tables(dataset, file=file, table_name=table_name) 
    return df
    