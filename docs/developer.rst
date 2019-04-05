=================
Developer's guide
=================

Required Modules
================

If you are installing from source you will need a Python 2.6+ installation and the following modules:

::

  setuptools
  xlrd
  Sphinx


Setting up servers
==================

You need to install all the database infrastructures to enable local testing.

::

  SQLite
  MySQL
  PostgreSQL
  MSAccess

You will also need the following modules:

::

  mysqldb (MySQL)
  psycopg2-binary (PostgreSQL)
  pypyodbc (MS Access)

Style Guide for Python Code
===========================

Run ``pep8`` on the given file to make sure the file follows the right style.
In some cases we do tend to work outside the ``pep8`` requirements.
The compromise on ``pep8``  may be a result of enforcing better code readability.
In some cases ``pep`` shows errors for long lines, but that can be ignored.

``pep8 pythonfile.py``

Testing
=======

Follow these instructions to run a complete set of tests for any branch
Clone the branch you want to test.

Two ways of installing the program using the `setup tools`_.

we can either install from source as

.. code-block:: bash

  $ pip install . --upgrade or python setup.py install

or install in development mode.

.. code-block:: bash

  $  python setup.py develop

For more about `installing`_ refer to the python setuptools `documentation`_.

you can also install from Git.

.. code-block:: bash

  # Local repository
  pip install git+file:///path/to/your/git/repo #  test a PIP package located in a local git repository
  pip install git+file:///path/to/your/git/repo@branch  # checkout a specific branch by adding @branch_name at the end

  # Remote github repository
  pip install git+git://github.com/myuser/myproject  #  package from a github repository
  pip install git+git://github.com/myuser/myproject@my_branch # github repository Specific branch

Running tests locally
^^^^^^^^^^^^^^^^^^^^^

Services Used
-------------

Check the services' home pages in case you have to add the same capabilities to your master branch.

::

  Travis
  AppVeyor
  readthedocs
  codecov


links `Read The Docs`_, `codecov`_, `AppVeyor`_ and  `Travis`_

To run the tests you will need to have all of the relevant database management systems and associated
modules installed (see ``Setting up servers``). Create the appropriate permissions for the tests to access
the databases. You can do this by running the following commands in MySQL and
PostgreSQL and creating the .pgpass(pgpass.conf for Microsoft Windows) file as described below:

Passwordless configuration
--------------------------

To avoid supplying the passwords when using the tool, use the config files
`.pgpass`(`pgpass.conf` for Microsoft Windows) for Postgres and `.my.cnf`
for MySQL. The files are kept in the HOME directory(~/.pgpass, ~/.my.cnf).
Make sure you set the file permissions to 600. For Postgres, on Microsoft
Windows, entering `%APPDATA%` will take you to `C:\Users\username\AppData\Roaming`.
In this directory create a new subdirectory named `postgresql`. Then create the
`pgpass.conf` file inside it. On Microsoft Windows, it is assumed that the file
is stored in a directory that is secure, so no special permissions check is made.

::

  chmod 600 ~/.pgpass
  chmod 600 ~/.my.cnf

::

  MySQL
  -----
  mysql -e "CREATE USER 'travis'@'localhost';" -uroot
  mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'travis'@'localhost';" -uroot
  mysql -e "GRANT FILE ON *.* TO 'travis'@'localhost';" -uroot
  Sample  `~.my.cnf` file
  [client]
  user="travis"
  password="Password12!"
  host="mysqldb"
  port="3306"

::

  PostgreSQL
  ----------
  psql -c "CREATE USER postgres WITH PASSWORD 'Password12!'"
  psql -c 'CREATE DATABASE testdb_retriever'
  psql -c 'GRANT ALL PRIVILEGES ON DATABASE testdb_retriever to postgres'
  ​
  Create .pgpass in your home directory:
  localhost:*:testdb_retriever:postgres:Password12!




To run tests we use pytest.
From the source top level directory, run

.. code-block:: sh

  $   py.test


To run tests on a specific test category add the path of the test module to the end of the py.test command: 

.. code-block:: sh

  $   py.test ./test/test_retriever.py

This will only run test_retriever.py

In case ``py.test`` requests for Password (even after Passwordless configuration), change the owner and group
from the permissions of the files ``~/.pgpass, ~/.my.cnf``

Continuous Integration
^^^^^^^^^^^^^^^^^^^^^^

The main GitHub repository runs test on both the Travis (Linux) and AppVeyor
(Windows) continuous integration platforms.

Pull requests submitted to the repository will automatically be tested using
these systems and results reported in the ``checks`` section of the pull request
page.


Create Release
==============

Start
^^^^^

1. **Run the tests**. Seriously, do it now.
2. In the `master` branch update the version number in ``setup.py`` (if it
   hasn’t already been bumped)
3. Run ``python version.py`` (this will update ``version.txt``)
4. Update the version number in ``retriever_installer.iss`` (if it
   hasn’t already been bumped)
5. Update ``CHANGES.md`` with major updates since last release
6. Commit changes
7. Add a tag with appropriate version number, e.g.
   ,\ ``git tag -a v1.8.0 -m "Version 1.8.0"``
8. Push the release commit and the tag

   ::

       git push upstream master
       git push upstream --tags

Linux
^^^^^

**Building the DEB package does not work using conda. If conda is your main**
**Python change `python` in `build.sh` to `/usr/bin/python` or otherwise**
**Adjust the path to use the system Python.**

1. **Run the tests** (unless you just ran them on the same machine)
2. Checkout master
3. Run ``build.sh``

Windows
^^^^^^^

1. **Run the tests**. This helps makes sure that the build environment
   is properly set up.
2. Checkout master
3. Run ``sh build_win``

Mac
^^^

1. **Run the tests**. This helps makes sure that the build environment
   is properly set up.
2. Checkout master
3. Run ``build_mac``
4. Install the retriever for verification. Reference
   http://www.data-retriever.org/download.html

Pypi
^^^^

1. `sudo python setup.py sdist bdist_wheel upload`

Cleanup
^^^^^^^

1. Bump the version numbers as needed. The version number are located in the ``setup.py``,
   ``retriever_installer.iss``, ``version.txt`` and ``retriever/_version.py``

Mac OSX Build
=============

Building the Retriever on OSX.

Python binaries
^^^^^^^^^^^^^^^

This build will allow you to successfully build the Mac App for
distribution to other systems.

1. Install the Python 3 Installer (or Python 2 if you have a specific reason for doing so)
   from the `Python download site`_.
2. Use pip to install any desired optional dependencies ``pip install pymysql psycopg2-binary pyinstaller pytest``
   You will need all of these dependencies, for example pyinstaller, if you want to build the Mac App for distribution

Homebrew
^^^^^^^^

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
5. ``sudo pip install pymysql MySQL-python psycopg2-binary``

``MySQL-python`` should be installed in addition to ``pymysql`` for
building the ``.app`` file since pymysql is not currently working
properly in the ``.app``.

Conda
^^^^^

-  This hasn’t been tested yet

.. _Python download site: http://www.python.org/download/



Creating or Updating a Conda Release
====================================

To create or update a Conda Release, first fork the conda-forge `retriever-feedstock repository <https://github.com/conda-forge/retriever-feedstock>`_.

Once forked, open a pull request to the retriever-feedstock repository. Your package will be tested on Windows, Mac and Linux.

When your pull request is merged, the package will be rebuilt and become automatically available on conda-forge.

All branches in the conda-forge/retriever-feedstock are created and uploaded immediately, so PRs should be based on branches in forks. Branches in the main repository shall be used to build distinct package versions only.

For producing a uniquely identifiable distribution:

 - If the version of a package is not being incremented, then the build/number can be added or increased.
 - If the version of a package is being incremented, then remember to return the build/number back to 0.

Documentation
=============

We are using `Sphinx`_ and `Read the Docs`_. for the documentation.
Sphinx uses reStructuredText as its markup language.
Source Code documentation is automatically included after committing to the master.
Other documentation (not source code) files are added as new reStructuredText in the docs folder

In case you want to change the organization of the Documentation, please refer to `Sphinx`_

**Update Documentation**

The documetation is automatically updated for changes with in modules.
However, the documentation should be updated after addition of new modules in the engines or lib directory.
Change to the docs directory and create a temporary directory, i.e. ``source``.
Run

.. code-block:: bash

  cd  docs
  mkdir source
  sphinx-apidoc -f  -o ./source /Users/../retriever/

The ``source`` is the destination folder for the source rst files. ``/Users/../retriever/`` is the path to where
the retriever source code is located.
Copy the ``.rst`` files that you want to update to the docs direcotry, overwriting the old files.
Make sure you check the changes and edit if necessary to ensure that only what is required is updated.
Commit and push the new changes.
Do not commit the temporary source directory.

**Test Documentation locally**

.. code-block:: bash

  cd  docs  # go the docs directory
  make html # Run

  Note:
  Do not commit the build directory after making html.

**Read The Docs configuration**

Configure read the docs (advanced settings) so that the source is first installed then docs are built.
This is already set up but could be change if need be.

Collaborative Workflows with GitHub
===================================

**Submiting issues**

Categorize the issues based on labels. For example (Bug, Dataset Bug, Important, Feature Request and etc..)
Explain the issue explicitly with all details, giving examples and logs where applicable.

**Commits**

From your local branch of retriever, commit to your origin.
Once tests have passed you can then make a pull request to the retriever master (upstream)
For each commit, add the issue number at the end of the description with the tag ``fixes #[issue_number]``.

Example::

  Add version number to postgres.py to enable tracking

  Skip a line and add more explanation if needed
  fixes #3

**Clean histroy**

We try to make one commit for each issue.
As you work on an issue, try adding all the commits into one general commit rather than several commits.

Use ``git commit --amend`` to add new changes to a branch.

Use ``-f`` flag to force pushing changes to the branch. ``git push -f origin [branch_name]``


.. _codecov: https://codecov.io/
.. _project website: http://data-retriever.org
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _Read The Docs: https://readthedocs.org//
.. _Travis: https://travis-ci.org/
.. _AppVeyor: https://www.appveyor.com/
.. _documentation: https://pythonhosted.org/an_example_pypi_project/setuptools.html
.. _installing: https://docs.python.org/3.6/install/
.. _installing the wheel: http://www.lfd.uci.edu/~gohlke/pythonlibs/
.. _setup tools: https://pythonhosted.org/an_example_pypi_project/setuptools.html

