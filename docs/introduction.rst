============
Introduction
============


We handle the data so you can focus on the science
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finding data is one thing. Getting it ready for analysis is another. Acquiring,
cleaning, standardizing and importing publicly available data is time consuming
because many datasets lack machine readable metadata and do not conform to
established data structures and formats.

The Data Retriever automates the first
steps in the data analysis pipeline by downloading, cleaning, and standardizing
datasets, and importing them into relational databases, flat files, or
programming languages. The automation of this process reduces the time for a
user to get most large datasets up and running by hours, and in some cases days.


What data tasks does the Retriever handle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Data Retriever handles a number of common tasks including:
 #. Creating the underlying database structures, including automatically determining the data types
 #. Downloading the data
 #. Transforming data into appropriately normalized forms for database management systems (e.g., "wide" data into "long" data and splitting tables into proper sub-tables to reduce duplication)
 #. Converting heterogeneous null values (e.g., 999.0, -999, NaN) into standard null values
 #. Combining multiple data files into single tables; and 6) placing all related tables in a single database or schema.

A couple of examples on the more complicated end include the Breeding Bird
Survey of North America (breed-bird-survey) and the Alwyn Gentry Tree Transect
data(gentry-forest-transects):

- Breeding bird survey data consists of multiple tables. The main table is divided
  into one file per region in 70 individual compressed files. Supplemental tables
  required to work with the data are posted in a variety of locations and formats.
  The Data Retriever automates: downloading all data files, extracting data from
  region-specific raw data files into single tables, correcting typographic
  errors, replacing non-standard null values, and adding a Species table that
  links numeric identifiers to actual species names.
- The Gentry forest transects data is stored in over 200 Excel spreadsheets, each
  representing an individual study site, and compressed in a zip archive.
  Each spreadsheet contains counts of individuals found at a given site and all stems
  measured from that individual; each stem measurement is placed in a separate column,
  resulting in variable numbers of columns across rows, a format that is
  difficult to work with in both database and analysis software. There is no
  information on the site in the data files themselves, it is only present in
  the names of the files. The Retriever downloads the archive, extracts the
  files, and splits the data they contain into four tables: Sites, Species,
  Stems, and Counts, keeping track of which file each row of count data
  originated from in the Counts table and placing a single stem on each row in
  the Stems table.

*Adapted from* `Morris & White 2013`_.

Installing (binaries)
~~~~~~~~~~~~~~~~~~~~~

Precompiled binaries of the most recent release are available for Windows,
OS X, and Ubuntu/Debian at the `project website`_.

Installing From Source
~~~~~~~~~~~~~~~~~~~~~~

**Required packages**

To install the Data Retriever from source, you’ll need Python 2.6+ or Python 3.3+
with the following packages installed:

-  xlrd

**The following packages are optional**

-  PyMySQL (for MySQL)
-  sqlite3 (for SQLite, v3.8 or higher required)
-  psycopg2 (for PostgreSQL)
-  pypyodbc (for MS Access)

**Steps to install from source**

1. Clone the repository
2. From the directory containing setup.py, run the following command:
   ``python setup.py install`` or use pip ``pip install . --upgrade`` to install and
   ``pip uninstall retriever`` to uninstall the retriever

3. After installing, type ``retriever`` from a command prompt to see the available options of
   the Data Retriever. Use ``retriever --version`` to confirm the version installed on your system.

Using the Data Retriever Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installing, run ``retriever update`` to download all of the
available dataset scripts. Run ``retriever ls`` to see the available datasets

To see the full list of command line options
and datasets run ``retriever --help``. The output will look like this:

::

    usage: retriever [-h] [-v] [-q]
                     {download,install,defaults,update,new,new_json,edit_json,delete_json,ls,citation,reset,help}
                     ...

    positional arguments:
      {download,install,defaults,update,new,new_json,edit_json,delete_json,ls,citation,reset,help}
                            sub-command help
        download            download raw data files for a dataset
        install             download and install dataset
        defaults            displays default options
        update              download updated versions of scripts
        new                 create a new sample retriever script
        new_json            CLI to create retriever datapackage.json script
        edit_json           CLI to edit retriever datapackage.json script
        delete_json         CLI to remove retriever datapackage.json script
        ls                  display a list all available dataset scripts
        citation            view citation
        reset               reset retriever: removes configation settings,
                            scripts, and cached data
        help

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -q, --quiet           suppress command-line output

To install datasets, use the ``install`` command.

Examples
~~~~~~~~

**Using install**

The install command downloads the datasets and installs them in the desired engine.

$ ``retriever install -h`` (gives install options)

::

    usage: retriever install [-h] [--compile] [--debug]
                             {mysql,postgres,sqlite,msaccess,csv,json,xml} ...
    positional arguments:
      {mysql,postgres,sqlite,msaccess,csv,json,xml}
                            engine-specific help
        mysql               MySQL
        postgres            PostgreSQL
        sqlite              SQLite
        msaccess            Microsoft Access
        csv                 CSV
        json                JSON
        xml                 XML
    optional arguments:
      -h, --help            show this help message and exit
      --compile             force re-compile of script before downloading
      --debug               run in debug mode


**Examples using install**


These examples use Breeding Bird Survey data (breed-bird-survey).
The retriever has support for various databases and flat file
formats (mysql, postgres, sqlite, msaccess, csv, json, xml).
All the engines have a variety of options or flags. Run ```retriever defaults`` to see the defaults.
For example, the default options for mysql and postgres engines are given below.

::

    retriever defaults

    Default options for engine  MySQL
    user   root
    password
    host   localhost
    port   3306
    database_name   {db}
    table_name   {db}.{table}

    Default options for engine  PostgreSQL
    user   postgres
    password
    host   localhost
    port   5432
    database   postgres
    database_name   {db}
    table_name   {db}.{table}

Help information for a particular engine can be obtained by running
retriever install [engine name] [-h] [--help], for example, ``retriever install mysql -h``.
Both mysql and postgres require the database user name ``--user [USER], -u [USER]``
and password ``--password [PASSWORD], -p [PASSWORD]``.
MySQL and PostgreSQL database management systems support the use of configuration files.
The configuration files provide a mechanism to support using the engines without providing authentication directly.
To set up the configuration files please refer to the respective database management systems documentation.

Install data into Mysql::

   retriever install mysql –-user myusername –-password ***** –-host localhost –-port 8888 –-database_name testdbase breed-bird-survey
   retriever install mysql –-user myusername breed-bird-survey (using attributes in the client authentication configuration file)

Install data into postgres::

   retriever install postgres –-user myusername –-password ***** –-host localhost –-port 5432 –-database_name testdbase breed-bird-survey
   retriever install postgres breed-bird-survey (using attributes in the client authentication configuration file)

Install data into sqlite::

   retriever install sqlite breed-bird-survey -f mydatabase.db (will use mydatabase.db)
   retriever install sqlite breed-bird-survey (will use or create default sqlite.db in working directory)

Install data into csv::

   retriever install csv breed-bird-survey --table_name  "BBS_{table}.csv"
   retriever install csv breed-bird-survey

**Using download**

The ``download`` command downloads the raw data files exactly as they occur at the
source without any clean up or modification. By default the files will be stored in the working directory.

``--path`` can be used to specify a location other than the working directory to download the files to. E.g., ``--path ./data``

``--subdir`` can be used to maintain any subdirectory structure that is present in the files being downloaded.

::

   retriever download -h (gives you help options)
   retriever download breed-bird-survey (download raw data files to the working directory)
   retriever download breed-bird-survey –path  C:\Users\Documents (download raw data files to path)


**Using citation**

The ``citation`` command show the citation for the retriever and for the scripts.

::

   retriever citation (citation of the Data retriever)
   retriever citation breed-bird-survey (citation of Breed bird survey data)


**To create new, edit, delete scripts please read the documentation on scripts**

Acknowledgments
~~~~~~~~~~~~~~~

Development of this software was funded by `the Gordon and Betty Moore
Foundation’s Data-Driven Discovery Initiative`_ through `Grant
GBMF4563`_ to Ethan White and the `National Science Foundation`_ as part
of a `CAREER award to Ethan White`_.


.. _the Gordon and Betty Moore Foundation’s Data-Driven Discovery Initiative: http://www.moore.org/programs/science/data-driven-discovery
.. _Grant GBMF4563: http://www.moore.org/grants/list/GBMF4563
.. _National Science Foundation: http://nsf.gov/
.. _CAREER award to Ethan White: http://nsf.gov/awardsearch/showAward.do?AwardNumber=0953694
.. _project website: http://data-retriever.org
.. _Morris & White 2013: https://dx.doi.org/10.1371/journal.pone.0065848
