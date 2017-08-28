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
The function returns a list of all the available scripts locally.

.. code-block:: python

  >>> rt.dataset_names()

You can add more datasets locally by yourself.
`Adding dataset <http://retriever.readthedocs.io/en/latest/scripts.html>`_ documentation.

.. code-block:: python

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

There are a lot of different attributes provided in the Scripts class. Some notably useful ones are:

.. code-block:: python

  name
  citation
  description
  keywords
  title
  urls
  version

Update Datasets
===============

If there are no scripts available or you want to update scripts to the latest version.
``check_for_updates`` function can be used.

.. code-block:: python

  >>> rt.check_for_updates()


Downloading for the first time the functions will take sometime depending on the internet connection.
In case of poor internet connection or other problems an error is raised.

Download Datasets
=================

To download datasets the ``download`` function can be used.
It has the following function definition.

.. code-block:: python

  def download(dataset, path='./', quiet=False, subdir=False, debug=False):

A simple download for the ``iris`` dataset can be done using.

.. code-block:: python

  >>> rt.download("iris")

Output:

.. code-block:: python

  => Downloading iris

  Downloading bezdekIris.data...
  100%  0 seconds Copying bezdekIris.data from /home/user_name/.retriever/raw_data/iris


This downloads the dataset in your current directory.
You can control where the dataset downloads using ``path`` parameter.
There are in all 4 default parameters.

.. code-block:: python

  path (String): Specify dataset download path.

  quiet  (Bool): Setting True minimizes the console output.

  subdir (Bool): Setting True keeps the subdirectories for archived files.

  debug  (Bool): Setting True helps in debugging in case of errors.

Install Datasets
================

Retriever supports scripts installation into 7 major formats or engines as we call them.

.. code-block::

  csv
  json
  msaccess
  mysql
  postgres
  sqlite
  xml


The function definition of the functions is as follows:

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

.. code-block::

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
