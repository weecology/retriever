The EcoData Retriever
=====================

Large quantities of ecological and environmental data are increasingly available thanks to initiatives sponsoring the collection of large-scale data and efforts to increase the publication of already collected datasets. As a result, progress in ecology is increasingly limited by the speed at which we can organize and analyze data. To help improve ecologists' ability to quickly access and analyze data we have been developing software that designs database structures for ecological datasets and then downloads the data, pre-processes it, and installs it into major database management systems (at the moment we support MySQL, PostgreSQL, SQLite, and Microsoft Access).

Once the EcoData Retriever has loaded the data into the database it is easy to connect to the database using standard tools (e.g., MS Access, Filemaker, etc.).The EcoData Retriever can download and install small datasets in seconds and large datasets in minutes. The program also cleans up known issues with the datasets and automatically restructures them into a format appropriate for standard database management systems. The automation of this process reduces the time for a user to get most large datasets up and running by hours, and in some cases days.


Installing (binaries)
---------------------

Precompiled binaries the most recent release are available for Windows and Ubuntu/Debian (OSX packages are available but hit and miss depending on the system) at the [project website](http://ecodataretriever.org).


Installing From Source
----------------------

To install the EcoData Retriever from source, you'll need Python 2.6 with the following packages installed:

* wxPython
* xlrd

The following packages are optional
-----------------------------------

* PyMySQL or MySQLdb (for MySQL)
* sqlite3 (for SQLite)
* psycopg2 (for PostgreSQL)
* pyodbc (for MS Access - this option is only available on Windows)

To install from source
----------------------

1. Clone the repository
2. From the directory containing setup.py, run the following command: python setup.py install
3. After installing, type retriever from a command prompt to launch the Database Toolkit,
   or find main.py in your Retriever directory and run it in Python.

License
-------
The EcoData Retriever is licensed under the open source [MIT License](http://opensource.org/licenses/MIT)

Copyright (c) 2011 Weecology

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


