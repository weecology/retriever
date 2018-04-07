from retriever import install_sqlite
from retriever.lib.engine_tools import getmd5
from retriever import datasets
from retriever.engines import engine_list
from tempfile import mkdtemp
from shutil import rmtree
import os
import urllib.request
import json
from datetime import datetime
from difflib import HtmlDiff

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = engine_list

file_location = os.path.dirname(os.path.realpath(__file__))

example_datasets = ['bird-size', 'mammal-masses', 'airports', 'portal']


def check_resources(dataset):
    """
    Parameters
    ----------
    dataset : dataset script object

    Returns
    -------
    dict : A dictionary containing those resources of a dataset which generate error when
           trying to check whether the url for that resource is working or not.

    Example
    -------
    >>> for dataset in datasets():
    ...     if dataset.name=='aquatic-animal-excretion':
    ...         print(check_resources(dataset))
    ...
    {'aquatic_animals': ('http://onlinelibrary.wiley.com/store/10.1002/ecy.1792/asset/supinfo/ecy1792-sup-0001-DataS1.zip?v=1&s=3a9094a807bbc2d03ba43045d2b72782bfb348ef', 'Method Not Allowed', 405)}

    """
    failed = {}
    tables_urls = {}
    if len(dataset.tables) != 0:
        for table_n in dataset.tables.values():
            tables_urls[table_n.name] = table_n.url if table_n.url != None or len(table_n.url) != 0 else None
    else:
        for table_n, url in dataset.urls.items():
            tables_urls[table_n] = url if url != None or len(url) != 0 else None
    for table_n, url in tables_urls.items():
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'
        try:
            urllib.request.urlopen(request)
        except urllib.request.HTTPError as e:
            failed[table_n] = (url, e.msg, e.code)
    return failed


def get_last_modified(dataset):
    """
    Parameters
    ----------
    dataset : dataset script object

    Returns
    -------
    dict : A dictionary containing resources of a dataset with resource name as keys and
           their last modified date as values.
    None : If the function fails to find the last modified date of any resource it returns None

    Example
    -------
    >>> for dataset in datasets():
    ...     if dataset.name=='airports':
    ...         print(get_last_modified(dataset))
    ...
    {'navaids': datetime.datetime(2018, 2, 20, 8, 53, 29), 'airports': datetime.datetime(2018, 2, 20, 8, 53, 14),
    'regions': datetime.datetime(2018, 2, 20, 8, 53, 30), 'runways': datetime.datetime(2018, 2, 20, 8, 53, 23),
    'countries': datetime.datetime(2018, 2, 20, 8, 53, 29), 'airport_frequencies': datetime.datetime(2018, 2, 20, 8, 53, 26)}
    """

    tables_urls = {}
    last_modified = {}
    ignore_list = ['nd-gain']
    if dataset.name in ignore_list:
        return
    if len(dataset.tables) != 0:
        for table_n in dataset.tables.values():
            tables_urls[table_n.name] = table_n.url if table_n.url != None or len(table_n.url) != 0 else None
    else:
        for table_n, url in dataset.urls.items():
            tables_urls[table_n] = url if url != None or len(url) != 0 else None
    for table_n, url in tables_urls.items():
        if url is None or len(url) == 0:
            return
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'
        try:
            response = urllib.request.urlopen(request)
            if response.code != 200:
                return
            last_modified[table_n] = datetime.strptime(response.headers['Last-Modified'], "%a, %d %b %Y %H:%M:%S %Z")
        except:
            return
    if len(last_modified) == 0 or None in last_modified.values():
        return
    return last_modified


def get_dataset_md5(dataset):
    """
    Parameters
    ----------
    dataset : dataset script object

    Returns
    -------
    str : The md5 value of a particular dataset.

    Example
    -------
    >>> for dataset in datasets():
    ...     if dataset.name=='aquatic-animal-excretion':
    ...         print(get_dataset_md5(dataset))
    ...
    683c8adfe780607ac31f58926cf1d326
    """
    workdir = mkdtemp(dir=file_location)
    os.chdir(workdir)
    install_sqlite(dataset.name, use_cache=False, file=os.path.join(file_location, 'new_sqlite.db'))
    engine_obj = dataset.checkengine(sqlite_engine)
    engine_obj.to_csv()
    current_md5 = getmd5(os.getcwd(), data_type='dir')
    os.chdir(file_location)
    os.remove("new_sqlite.db")
    rmtree(workdir)
    return current_md5


def create_diff(csv1, csv2, diff_file, context, numlines):
    """
        Parameters
        ----------
        csv1 : The first csv file.
        csv2 : The second csv file.
        diff_file : The diff_file that is to be generated.

        Returns
        -------
        None: Just creates a html source code file with diff details.

        Example
        -------
        >>> create_diff('file1.csv', 'file2.csv', 'differ.html')
    """
    html_diff = HtmlDiff()
    with open(csv1, 'r') as file1, open(csv2, 'r') as file2, open(diff_file, 'w') as file3:
        file3.writelines(html_diff.make_file(file1, file2, context=context, numlines= numlines))


def create_json(path="dataset_details.json"):
    """
    This function creates a json file with md5 values of all(currently those in example_datasets)
    datasets and their last modified dates.
    """
    data = {}
    for dataset in datasets():
        if dataset.name in example_datasets:
            modification_datetime = get_last_modified(dataset)
            if modification_datetime == None:
                max_last_modified = ""
            else:
                max_last_modified = max(modification_datetime.values()).strftime("%a, %d %b %Y %H:%M:%S GMT")
            data[dataset.name] = {"md5": get_dataset_md5(dataset),
                                  "last_modified": max_last_modified}
        with open(path, 'w') as json_file:
            json.dump(data, json_file, sort_keys=True, indent=4)


if __name__ == '__main__':
    create_json()
