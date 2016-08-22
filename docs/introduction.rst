============ 
Introduction
============


We handle the data so you can focus on the science
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Large quantities of ecological and environmental data are increasingly
available thanks to initiatives sponsoring the collection of large-scale
data and efforts to increase the publication of already collected
datasets. As a result, progress in ecology is increasingly limited by
the speed at which we can organize and analyze data. To help improve
ecologists’ ability to quickly access and analyze data we have been
developing software that designs database structures for ecological
datasets and then downloads the data, pre-processes it, and installs it
into major database management systems (at the moment we support MySQL,
PostgreSQL, SQLite, and Microsoft Access).

Once the Data Retriever has loaded the data into the database it is
easy to connect to the database using standard tools (e.g., MS Access,
Filemaker, etc.).The Data Retriever can download and install small
datasets in seconds and large datasets in minutes. The program also
cleans up known issues with the datasets and automatically restructures
them into a format appropriate for standard database management systems.
The automation of this process reduces the time for a user to get most
large datasets up and running by hours, and in some cases days.


What data tasks does the Retriever handle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Data Retriever handles a number of common tasks including: 1) creating
the underlying database structures, including automatically determining the data
types; 2) downloading the data; 3) transforming data into appropriately
normalized forms for database management systems (e.g., "wide" data into "long"
data and splitting tables into proper sub-tables to reduce duplication); 4)
converting heterogeneous null values (e.g., 999.0, -999, NaN) into standard null
values; 5) combining multiple data files into single tables; and 6) placing all
related tables in a single database or schema.

A couple of examples on the more complicated end include the Breeding Bird
Survey of North America (BBS) and the Alwyn Gentry Tree Transect data:

- BBS data consists of multiple tables. The main table is divided into one file
  per region in 70 individual compressed files. Supplemental tables required to
  work with the data are posted in a variety of locations and formats. The
  Data Retriever automates: downloading all data files, extracting data from
  region-specific raw data files into single tables, correcting typographic
  errors, replacing non-standard null values, and adding a Species table that
  links numeric identifiers to actual species names.
- The Gentry data is stored in over 200 Excel spreadsheets, each representing an
  individual study site, and compressed in a zip archive. Each spreadsheet
  contains counts of individuals found at a given site and all stems measured
  from that individual; each stem measurement is placed in a separate column,
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


To install the Data Retriever from source, you’ll need Python 2.6+
with the following packages installed:

-  xlrd


The following packages are optional
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  PyMySQL (for MySQL)
-  sqlite3 (for SQLite)
-  psycopg2 (for PostgreSQL)
-  pyodbc (for MS Access - this option is only available on Windows)

To install from source
~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository
2. From the directory containing setup.py, run the following command:
   ``python setup.py install``
3. After installing, type ``retriever`` from a command prompt to launch
   the Data Retriever

Using the Command Line
~~~~~~~~~~~~~~~~~~~~~~

After installing, run ``retriever update`` to download all of the
available dataset scripts. To see the full list of command line options
and datasets run ``retriever --help``. The output will look like this:

::

    usage: retriever  [-h] [-v] [-q]
                      {download,install,update,new,ls,citation,reset,help}
                      ...

    positional arguments:
        {download,install,update,new,ls,citation,reset,help}
                              sub-command help
          download            download raw data files for a dataset
          install             download and install dataset
          update              download updated versions of scripts
          new                 create a new sample retriever script
          ls                  display a list all available dataset scripts
          citation            view citation
          reset               reset retriever: removes configation settings,
                              scripts, and cached data
          help
      
      optional arguments:
        -h, --help            show this help message and exit
        -v, --version         show program's version number and exit
        -q, --quiet           suppress command-line output


To install datasets, use ``retriever install``::
 
    usage: retriever install [-h] [--compile] [--debug]
                             {mysql,postgres,sqlite,msaccess,csv} ...

    positional arguments:
      {mysql,postgres,sqlite,msaccess,csv}
                            engine-specific help
        mysql               MySQL
        postgres            PostgreSQL
        sqlite              SQLite
        msaccess            Microsoft Access
        csv                 CSV

    optional arguments:
      -h, --help            show this help message and exit
      --compile             force re-compile of script before downloading
      --debug               run in debug mode


Examples
~~~~~~~~



These examples are using Breeding Bird Survey data (BBS)

Using Install::
   
   retriever install -h (gives install options)
         
Using a specific database engine. The retriever has support for various engines; mysql, postgres, sqlite, msaccess, csv, download_only::
          
   retriever install {Engine}
   
   retriever install mysql -h     ..(gives install mysql options)::
   
   retriever install mysql –user myuser –password ***** –host localhost –port 8888 –database_name testdbase BBS
         
install data into an sqlite database named mydatabase.db you would use::
         
   retriever install sqlite BBS -f mydatabase.db
         
Using download::
   
   retriever download -h    (gives you help options) 
   retriever download BBS 
   retriever download BBS –path  C:\Users\Documents   
         
Using citation::

   retriever citation   (citation of the retriever engine)
   retriever citation BBS   (citation of BBS data)
      

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
.. _project website: http://ecodataretriever.org
.. _Morris & White 2013: https://dx.doi.org/10.1371/journal.pone.0065848