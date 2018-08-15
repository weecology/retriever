===============================
Using the Data Retriever from R
===============================

rdataretriever
==============

The `Data Retriever`_ provides an R interface to the Data Retriever so
that the ``retriever``'s data handling can easily be integrated into R workflows.

Installation
============

To use the R package ``rdataretriever``, you first need to `install the retriever <introduction.html#installing-binaries>`_.

The ``rdataretriever`` can then be installed using
``install.packages("rdataretriever")``

To install the development version, use ``devtools``

::

  # install.packages("devtools")
  library(devtools)
  install_github("ropensci/rdataretriever")

Note: The R package takes advantage of the Data Retriever's command line
interface, which must be available in the path. This path is given to the 
``rdataretriever`` using the function ``use_RetrieverPath()``. The location of 
``retriever`` is dependent on the Python installation (Python.exe, Anaconda, Miniconda),
the operating system and the presence of virtual environments in the system. The following instances
exemplify this reliance and how to find retriever's path.

Ubuntu OS with default Python:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If ``retriever`` is installed in default Python, it can be found out in the system with the help
of ``which`` command in the terminal. For example:

::

  $ which retriever
  /home/<system_name>/.local/bin/retriever

The path to be given as input to ``use_RetrieverPath()`` function is */home/<system_name>/.local/bin/*
as shown below:

:: 

  library(rdataretriever)
  use_RetrieverPath("/home/<system_name>/.local/bin/")

The ``which`` command in the terminal finds the location of ``retriever`` including the name
of the program, but the path required by the function is the directory that contains ``retriever``.
Therefore, the `retriever` needs to be removed from the path before using it.

Ubuntu OS with Anaconda environment:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When ``retriever`` is installed in an virtual environment, the user can track its location only
when that particular environment is activated. To illustrate, assume the virtual environment is *py27*:

::

  $ conda activate py27
  (py27) $ which retriever
  /home/<system_name>/anaconda2/envs/py27/bin/retriever

This path can be used for ``rdataretriever`` after removing `retriever` as follows:

::

  library(rdataretriever)
  use_RetrieverPath("/home/<system_name>/anaconda2/envs/py27/bin/")

Note: ``rdataretriever`` will be able to locate ``retriever`` even if the virtual environment is
deactivated.

rdataretriever functions:
=========================

datasets()
^^^^^^^^^^
**Description** : The function returns a list of available datasets.

**Arguments** : No arguments needed.

**Example** :

::

  rdataretriever::datasets()

fetch()
^^^^^^^
**Description** : Each datafile in a given dataset is downloaded to a temporary directory and then imported as a
data.frame as a member of a named list.

**Arguments** :

- ``dataset`` (String): Name of dataset to be downloaded
- ``quiet`` (Bool): The argument decides if warnings need to be displayed (TRUE/FALSE)
- ``data_name`` (String): Name assigned to dataset once it is downloaded

**Example** :

::

  rdataretriever :: fetch(dataset = 'portal')

download()
^^^^^^^^^^
**Description** : Used to download datasets directly without cleaning them and when user does not 
have a specific preference for the format of the data and the kind of database.


**Arguments** :

- ``dataset`` (String): Name of the dataset to be downloaded.

- ``path`` (String): Specify dataset download path.

- ``quiet``  (Bool): Setting TRUE minimizes the console output.

- ``sub_dir`` (Bool): Setting TRUE keeps the subdirectories for archived files.

- ``debug``  (Bool): Setting TRUE helps in debugging in case of errors.

**Example** :

::

  rdataretriever :: download("iris","/Users/username/Desktop")

Installation functions
^^^^^^^^^^^^^^^^^^^^^^
Format specific installation
----------------------------
**Description** : ``rdataretriever`` supports installation of datasets in three file formats through different functions: 

- csv (``install_csv``)
- json (``install_json``)
- xml (``install_xml``)

**Arguments** : These functions require same arguments.

- ``dataset`` (String): Name of the dataset to install.

- ``table_name`` (String): Specify the table name to install.

- ``debug`` (Bool): Setting TRUE helps in debugging in case of errors.

- ``use_cache`` (Bool): Setting FALSE reinstalls scripts even if they are already installed.

**Example** :

::

  rdataretriever :: install_csv("bird-size",table_name = "Bird_Size",debug = TRUE)

Database specific installation
------------------------------
**Description** : ``rdataretriever`` supports installation of datasets in four different databses through different functions:

- MySQL (``install_mysql``)
- PostgreSQL (``install_postgres``)
- SQLite (``install_sqlite``)
- MSAccess (``install_msaccess``)

**Arguments for PostgreSQL and MySQL** :

- ``database_name`` (String): Specify database name.

- ``debug``           (Bool): Setting True helps in debugging in case of errors.

- ``host``          (String): Specify host name for database.

- ``password``      (String): Specify password for database.

- ``port``             (Int): Specify the port number for installation.

- ``quiet``           (Bool): Setting True minimizes the console output.

- ``table_name``    (String): Specify the table name to install.

- ``use_cache``       (Bool): Setting False reinstalls scripts even if they are already installed.

- ``user``          (String): Specify the username.

**Example** :

::

  rdataretriever :: install_postgres(dataset = 'portal', user='postgres', password='abcdef')

**Arguments for MSAccess and SQLite** :

- ``file`` (String): Enter file_name for database.

- ``table_name`` (String): Specify the table name to install.

- ``debug`` (Bool): Setting True helps in debugging in case of errors.

- ``use_cache`` (Bool): Setting False reinstalls scripts even if they are already installed.

**Example** :

::

  rdataretriever :: install_sqlite(dataset = 'iris', file = 'sqlite.db',debug=FALSE, use_cache=TRUE)

get_updates()
^^^^^^^^^^^^^
**Description** : This function will check if the version of the retriever’s scripts in your local directory ‘
~/.retriever/scripts/' is up-to-date with the most recent official retriever release.

**Example** :

::

  rdataretriever :: get_updates()

reset()
^^^^^^^
**Description** : The function will Reset the components of rdataretriever using scope [ all, scripts, data, connection]

**Arguments** :

- ``scope`` : Specifies what components to reset.  Options include:  ’scripts’, ’data’, ’connection’ and
’all’, where ’all’ is the default setting that resets all components.

**Example** :

::

  rdataretriever :: reset(scope = 'data')


Examples
========

::

 library(rdataretriever)
 
 # List the datasets available via the retriever
 rdataretriever::datasets()
 
 # Install the Gentry forest transects dataset into csv files in your working directory
 rdataretriever::install('gentry-forest-transects', 'csv')
 
 # Download the raw Gentry dataset files without any processing to the 
 # subdirectory named data
 rdataretriever::download('gentry-forest-transects', './data/')
 
 # Install and load a dataset as a list
 Gentry = rdataretriever::fetch('gentry-forest-transects')
 names(gentry-forest-transects)
 head(gentry-forest-transects$counts)


To get citation information for the ``rdataretriever`` in R use ``citation(package = 'rdataretriever')``:


.. _Data Retriever: http://data-retriever.org





