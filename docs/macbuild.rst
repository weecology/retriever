Mac OSX Build
=============

Building the Retriever on OSX.

Python binaries
---------------

This build will allow you to successfully build the Mac App for
distribution to other systems.

1. Install the Python 3 Installer (or Python 2 if you have a specific reason for doing so)
   from the `Python download site`_.
2. Use pip to install any desired optional dependencies ``pip install pymysql psycopg2 pyinstaller pytest``
   You will need all of these dependencies, for example pyinstaller, if you want to build the Mac App for distribution

Homebrew
--------

Homebrew works great if you just want to install the Retriever from
source on your own machine, but at least based on this recipe it does
not support distribution of the Mac App to other versions of OS X (i.e.,
if you build the App on OS X 10.9 it will only run on 10.9)

1.  Install Homebrew
    ``ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"``
2.  Install Xcode
3.  Install Python ``brew install python``
4.  Install the Xcode command line tools ``xcode-select --install``
5.  Make brew’s Python the default
    ``echo export PATH='usr/local/bin:$PATH' >> ~/.bash_profile``
6.  Install xlrd via pip ``pip install xlrd``. No ``sudo`` is necessary
    since we’re using brew.
7.  Clone the Retriever
    ``git clone git@github.com:weecology/retriever.git``
8. Switch directories ``cd retriever``
9. Standard install ``pip install . --upgrade``

If you also want to install the dependencies for MySQL and PostgreSQL
this can be done using a combination of homebrew and pip.

1. ``brew install mysql``
2. Follow the instructions from ``brew`` for starting MySQL
3. ``brew install postgresql``
4. Follow the instructions from ``brew`` for starting Postgres
5. ``sudo pip install pymysql MySQL-python psycopg2``

``MySQL-python`` should be installed in addition to ``pymysql`` for
building the ``.app`` file since pymysql is not currently working
properly in the ``.app``.

Conda
-----

-  This hasn’t been tested yet

.. _Python download site: http://www.python.org/download/

