===========================
Data Retriever using Python
===========================


`Data Retriever <http://data-retriever.org>`_ is written purely in `python <http://www.python.org/>`_.
The Python interface provides the core functionality supported by the CLI (Command Line Interface).



Installation
============

The installation instructions for the CLI and module are the same. Links have been provided below for convenience.

- Instructions for installing from binaries `project website <http://data-retriever.org>`_.
- Instructions for installing from source  `install from Source <https://github.com/weecology/retriever>`_.

Note: The python interface requires version 2.1 and above.

Tutorial
========

Importing retriever

.. code-block:: python

  >>> import retriever

In this tutorial, the module will be referred as ``rt``.

.. code-block:: python

  >>> import retriever as rt

List Datasets
=============

Listing available datasets using ``dataset_names`` function.
The function returns a list of all the currently available scripts.

.. code-block:: python

  >>> rt.dataset_names()

  ['abalone-age',
   'antarctic-breed-bird',
   .
   .
   'wine-composition',
   'wine-quality']


For more detailed description of the scripts installed in retriever ``datasets`` function can be used.
This function returns a list objects of ``Scripts`` class.
From these objects, we can access the available Script's attributes.

.. code-block:: python

  >>> for dataset in rt.datasets():
        print(dataset.name)
        
  abalone-age
  airports
  amniote-life-hist
  antarctic-breed-bird
  aquatic-animal-excretion
  .
  .


There are a lot of different attributes provided in the Scripts class. Some notably useful ones are:

.. code-block:: python

  name
  citation
  description
  keywords
  title
  urls
  version

You can add more datasets locally by yourself.
`Adding dataset <http://retriever.readthedocs.io/en/latest/scripts.html>`_ documentation.

Update Datasets
===============

If there are no scripts available, or you want to update scripts to the latest version,
``check_for_updates`` will download the most recent version of all scripts.


.. code-block:: python

  >>> rt.check_for_updates()
  
  Downloading scripts...
  Download Progress: [####################] 100.00%
  The retriever is up-to-date


Downloading recipes for all datasets can take a while depending on the internet connection.

Download Datasets
=================

To directly download datasets without cleaning them use the ``download`` function

.. code-block:: python

  def download(dataset, path='./', quiet=False, subdir=False, debug=False):

A simple download for the ``iris`` dataset can be done using.

.. code-block:: python

  >>> rt.download("iris")

Output:

.. code-block:: python

  => Downloading iris

  Downloading bezdekIris.data...
  100%  0 seconds Copying bezdekIris.data


This downloads the dataset in your current working directory.
You can control where the dataset is downloaded using the ``path`` parameter.


.. code-block:: python

  path (String): Specify dataset download path.

  quiet  (Bool): Setting True minimizes the console output.

  subdir (Bool): Setting True keeps the subdirectories for archived files.

  debug  (Bool): Setting True helps in debugging in case of errors.

Install Datasets
================

Retriever supports installation of datasets into 7 major databases and file formats.

.. code-block:: python

  csv
  json
  msaccess
  mysql
  postgres
  sqlite
  xml


There are separate functions for installing into each of the 7 backends:

.. code-block:: python

    def install_csv(dataset, table_name=None, compile=False, debug=False,
                quiet=False, use_cache=True):

    def install_json(dataset, table_name=None, compile=False,
                 debug=False, quiet=False, use_cache=True):

    def install_msaccess(dataset, file=None, table_name=None,
                     compile=False, debug=False, quiet=False, use_cache=True):

    def install_mysql(dataset, user='root', password='', host='localhost',
                  port=3306, database_name=None, table_name=None,
                  compile=False, debug=False, quiet=False, use_cache=True):

    def install_postgres(dataset, user='postgres', password='',
                     host='localhost', port=5432, database='postgres',
                     database_name=None, table_name=None,
                     compile=False, debug=False, quiet=False, use_cache=True):

    def install_sqlite(dataset, file=None, table_name=None,
                   compile=False, debug=False, quiet=False, use_cache=True):

    def install_xml(dataset, table_name=None, compile=False, debug=False,
                quiet=False, use_cache=True):

A description of default parameters mentioned above:

.. code-block:: python

  compile   (Bool): Setting True recompiles scripts upon installation.

  database_name(String): Specify database name. For postgres, mysql users.

  debug     (Bool): Setting True helps in debugging in case of errors.

  file      (String): Enter file_name for database. For msaccess, sqlite users.

  host      (String): Specify host name for database. For postgres, mysql users.

  password  (String): Specify password for database. For postgres, mysql users.

  port      (Int): Specify the port number for installtion. For postgres, mysql users.

  quiet     (Bool): Setting True minimizes the console output.

  table_name(String): Specify the table name to install.

  use_cache (Bool): Setting False reinstall scripts if it is already installed.

  user      (String): Specify the user_name. For postgres, mysql users.
