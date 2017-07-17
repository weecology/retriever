![Retriever logo](http://i.imgur.com/se7TtrK.png)


[![Build Status](https://travis-ci.org/weecology/retriever.png)](https://travis-ci.org/weecology/retriever)
[![Build Status (windows)](https://ci.appveyor.com/api/projects/status/qetgo4jxa5769qtb/branch/master?svg=true)](https://ci.appveyor.com/project/ethanwhite/retriever/branch/master)
[![Research software impact](http://depsy.org/api/package/pypi/retriever/badge.svg)](http://depsy.org/package/python/retriever)
[![codecov.io](https://codecov.io/github/weecology/retriever/coverage.svg?branch=master)](https://codecov.io/github/weecology/retriever?branch=master)
[![Documentation Status](https://readthedocs.org/projects/retriever/badge/?version=latest)](http://retriever.readthedocs.io/en/latest/?badge=latest)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/weecology/retriever/master/LICENSE)
[![Join the chat at https://gitter.im/weecology/retriever](https://badges.gitter.im/weecology/retriever.svg)](https://gitter.im/weecology/retriever?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Finding data is one thing. Getting it ready for analysis is another. Acquiring,
cleaning, standardizing and importing publicly available data is time consuming
because many datasets lack machine readable metadata and do not conform to
established data structures and formats. The Data Retriever automates the first
steps in the data analysis pipeline by downloading, cleaning, and standardizing
datasets, and importing them into relational databases, flat files, or
programming languages. The automation of this process reduces the time for a
user to get most large datasets up and running by hours, and in some cases days.

## Installing the Current Release

If you have Python installed you can install the current release using either `pip`:

```
pip install retriever
```

or `conda` after adding the `conda-forge` channel (`conda config --add channels conda-forge`):

```
conda install retriever
```

Depending on your system configuration this may require `sudo` for `pip`:

```
sudo pip install retriever
```

Precompiled binary installers are also available for Windows, OS X, and
Ubuntu/Debian on
the [releases page](https://github.com/weecology/retriever/releases). These do
not require a Python installation. Download the installer for your operating
system and follow the instructions at on
the [download page](http://www.data-retriever.org/download.html).


Installing From Source
----------------------

To install the Data Retriever from source, you'll need Python 2.7+ or 3.3+ with the following packages installed:

* xlrd

The following packages are optionally needed to interact with associated
database management systems:

* PyMySQL (for MySQL)
* sqlite3 (for SQLite)
* psycopg2 (for PostgreSQL)
* pyodbc (for MS Access - this option is only available on Windows)
* Microsoft Access Driver (ODBC for windows)

### To install from source

Either use pip to install directly from GitHub:

```
pip install git+https://git@github.com/weecology/retriever.git
```

or:

1. Clone the repository
2. From the directory containing setup.py, run the following command: `pip
   install .`. You may need to include `sudo` at the beginning of the
   command depending on your system (i.e., `sudo pip install .`).

More extensive documentation for those that are interested in developing can be found [here](http://retriever.readthedocs.io/en/latest/?badge=latest)

Using the Command Line
----------------------
After installing, run `retriever update` to download all of the available dataset scripts.
To see the full list of command line options and datasets run `retriever --help`.
The output will look like this:
```
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
```

To install datasets, use `retriever install`:

```
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
```


### Examples

```
These examples are using the [*Iris* flower dataset](https://en.wikipedia.org/wiki/Iris_flower_data_set).
More exapmles can be found in the Data Retriever documentation.

Using Install

  retriever install -h   (gives install options)

Using specific database engine, retriever install {Engine}

  retriever install mysql -h     (gives install mysql options)
  retriever install mysql --user myuser --password ******** --host localhost --port 8888 --database_name testdbase iris

install data into an sqlite database named iris.db you would use:

  retriever install sqlite iris -f iris.db

Using download

  retriever download -h    (gives you help options)
  retriever download iris
  retriever download iris --path C:\Users\Documents

Using citation
  retriever citation   (citation of the retriever engine)
  retriever citation iris  (citation for the iris data)
  ```

Website
-------

For more information see the
[Data Retriever website](http://www.data-retriever.org/).

Acknowledgments
---------------

Development of this software was funded by [the Gordon and Betty Moore
Foundation's Data-Driven Discovery
Initiative](http://www.moore.org/programs/science/data-driven-discovery) through
[Grant GBMF4563](http://www.moore.org/grants/list/GBMF4563) to Ethan White and
the [National Science Foundation](http://nsf.gov/) as part of a [CAREER award to
Ethan White](http://nsf.gov/awardsearch/showAward.do?AwardNumber=0953694).
