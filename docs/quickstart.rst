===========
Quick Start
===========

The Data Retriever is written in Python and has a Python interface, a command
line interface or an associated R package. It installs publicly available data
into a variety of databases (MySQL, PostgreSQL, SQLite) and flat file formats
(csv, json, xml).

Installation
~~~~~~~~~~~~

Using conda:

$ ``conda install retriever -c conda-forge``

or pip:

$ ``pip install retriever``

To install the associated R package:

$ ``install.packages('rdataretriever')``

Python interface
~~~~~~~~~~~~~~~~

Import:

$ ``import retriever as rt``

List available datasets:

$ ``rt.dataset_names()``

Load data on GDP from the World bank:

$ ``rt.fetch('gdp')``

Install the World Bank data on GDP into an SQLite databased named
"gdp.sqlite":

$ ``rt.install_sqlite('gdp', file='gdp.sqlite)``

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

List available datasets:

$ ``retriever ls``

Install the `Portal dataset <https://github.com/weecology/portaldata>`_ into a
set of json files:

$ ``retriever install json portal``

Install the Portal dataset into an SQLite database named "portal.sqlite":

$ ``retriever install sqlite portal -f portal.sqlite``

R interface
~~~~~~~~~~~

List available datasets:

$ ``rdataretriever::datasets()``

Load data on GDP from the World bank:

$ ``rdataretriever::fetch(dataset = 'gdp')``

Install the GDP dataset into SQLite:

$ ``rdataretriever::install('gdp', 'sqlite')``

Learn more
~~~~~~~~~~

Check out the rest of the documentation for more commands, details, and
datasets.

Available install formats for all interfaces are: mysql, postgres, sqlite,
csv, json, and xml.
