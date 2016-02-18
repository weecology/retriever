Mac OSX Build
=============

Building the Retriever on OSX.

Python binaries
---------------

This build will allow you to successfully build the Mac App for
distribution to other systems.

1. If running OS X 10.8+ go to
   ``System Preferences -> Security & Privacy -> General`` and select
   ``Allow apps downloaded from Anywhere``. This is necessary because
   GateKeeper will try to prevent this installation. You can return this
   setting to its previous state following the installation.
2. Install the Python 2.7 Installer from the `Python download site`_
   (double click the dmg and then double click the installer). Use the
   Mac OS X 64-bit/32-bit x86-64/i386 Installer for Mac OS X 10.6 and
   later unless you have a good reason to do otherwise.
3. Install the wxPython Installer from the `wxPython site`_. Use the
   Cocoa build unless you have a good reason to do otherwise.
4. Install setuptools (if you haven’t already)

   -  Download `ez\_setup.py`_
   -  Navigate to the directory where you downloaded it and run
      ``sudo python ez_setup.py``)

5. Install pip: ``easy_install pip``
6. Use pip to install the xlrd ``pip install xlrd``
7. Use pip to install any desired optional dependencies
   ``pip install PyMySQL MySQL-python psycopg2 py2app``

   -  You will need all of these dependencies if you want to build the
      Mac App for distribution

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
5.  Install wxPython using Homebrew
    ``brew install --python wxmac --devel``. **NOTE: This takes a very
    long time**
6.  Make brew’s Python the default
    ``echo export PATH='usr/local/bin:$PATH' >> ~/.bash_profile``
7.  Install xlrd via pip ``pip install xlrd``. No ``sudo`` is necessary
    since we’re using brew.
8.  Install py2app via pip ``pip install py2app``.
9.  Clone the Retriever
    ``git clone git@github.com:weecology/retriever.git``
10. Switch directories ``cd retriever``
11. Standard install ``python setup.py install``

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
.. _wxPython site: http://wxpython.org/download.php#osx
.. _ez\_setup.py: https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
