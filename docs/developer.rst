=================
Developer's guide
=================

1. Quickstart by forking the main repository https://github.com/weecology/retriever
2. Clone your copy of the repository

    - Using https ``git clone https://github.com/henrykironde/retriever.git``
    - Using ssh ``git clone git@github.com:henrykironde/retriever.git``

3. Link or point your cloned copy to the main repository. (I always name it upstream)

    - ``git remote add upstream https://github.com/weecology/retriever.git``

5. Check/confirm your settings using ``git remote -v``

::

    origin	git@github.com:henrykironde/retriever.git (fetch)
    origin	git@github.com:henrykironde/retriever.git (push)
    upstream	https://github.com/weecology/retriever.git (fetch)
    upstream	https://github.com/weecology/retriever.git (push)

6. Install the package from the main directory.
use `-U or --upgrade` to upgrade or overwrite any previously installed versions.

::

    pip install . -U

7. Check if the package was installed

::

    retriever ls
    retriever -v

8. Run sample test on  CSV engine only, with the option `-k`

::

   pip install pytest
   pytest -k "CSV" -v


Required Modules
================

You will need Python 3.6.8+
Make sure the required modules are installed: ``Pip install -r requirements.txt``

Developers need to install these extra packages.

::

   pip install codecov
   pip install pytest-cov
   pip install pytest-xdist
   pip install pytest
   pip install yapf
   pip install pylint
   pip install flake8
   Pip install pypyodbc # For only Windows(MS Access)

Setting up servers
==================

You need to install all the database infrastructures to enable local testing.


`PostgresSQL`_
`MySQL`_
`SQLite`_
`MSAccess`_ (For only Windows, MS Access)

After installation, configure passwordless access to MySQL and PostgresSQL Servers

Passwordless configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

To avoid supplying the passwords when using the tool, use the config files
`.pgpass`(`pgpass.conf` for Microsoft Windows) for Postgres and `.my.cnf`
for MySQL.

Create if not exists, and add/append the configuration details as below.
PostgresSQL conf file `~/.pgpass` file.

For more information regarding Passwordless configuration you can visit `PostgreSQL Password File`_ 
and `MySQL Password File`_ 

::

  localhost:*:*:postgres:Password12!

**Postgress:**

(Linux / Macos):- A `.pgpass` file in your HOME directory(~)

(WINDOWS 10-) - A `pgpass.conf` in your HOME directory(~)

(WINDOWS 10+):- Entering `%APPDATA%` will take you to `C:/\Users/\username/\AppData/\Roaming`.

In this directory create a new subdirectory named `postgresql`. Then create the `pgpass.conf` file inside it. On Microsoft Windows, it is assumed that the file is stored in a secure directory, hence no special permissions setting is needed.

Make sure you set the file permissions to 600

::

  # Linux / Macos
  chmod 600 ~/.pgpass
  chmod 600 ~/.my.cnf

For most of the recent versions of **Postgress server 10+**, you need to find `pg_hba.conf`. This file is located in the installed Postgres directory.
One way to find the location of the file `pg_hba.conf` is using ``psql -t -P format=unaligned -c 'show hba_file';``
To allow passwordless login to Postgres, change peer to `trust` in `pg_hba.conf` file.

::

  # Database administrative login by Unix domain socket
  local   all             postgres                                trust

Run commands in terminal to create user
::

  PostgreSQL
  ----------
  psql -c "CREATE USER postgres WITH PASSWORD 'Password12!'"
  psql -c 'CREATE DATABASE testdb_retriever'
  psql -c 'GRANT ALL PRIVILEGES ON DATABASE testdb_retriever to postgres'

Restart the server and test Postgress passwordless setup using retriever without providing the password

``retriever install postgres iris``

**MySQL:** Create if not exists `.my.cnf` in your HOME directory(~).
Add the configuration info to the MySQL conf file `~.my.cnf` file.

::

  [client]
  user="travis"
  password="Password12!"
  host="mysqldb"
  port="3306"

Run commands in terminal to create user
::

  MySQL
  -----
  mysql -e "CREATE USER 'travis'@'localhost';" -uroot
  mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'travis'@'localhost';" -uroot
  mysql -e "GRANT FILE ON *.* TO 'travis'@'localhost';" -uroot

 Restart the server and test MySQL passwordless setup using retriever without providing the password

``retriever install mysql iris``

Testing
=======

Before running the tests make sure Postgis is set up `Spatial database setup`_.

Follow these instructions to run a complete set of tests for any branch
Clone the branch you want to test.

Two ways of installing the program using the `setup tools`_.

we can either install from source as

.. code-block:: bash

  pip install . --upgrade or python setup.py install

or install in development mode.

.. code-block:: bash

  python setup.py develop

For more about `installing`_ refer to the python setuptools `documentation`_.

you can also install from Git.

.. code-block:: bash

  # Local repository
  pip install git+file:///path/to/your/git/repo #  test a PIP package located in a local git repository
  pip install git+file:///path/to/your/git/repo@branch  # checkout a specific branch by adding @branch_name at the end

  # Remote GitHub repository
  pip install git+git://github.com/myuser/myproject  #  package from a GitHub repository
  pip install git+git://github.com/myuser/myproject@my_branch # github repository Specific branch


Running tests locally
^^^^^^^^^^^^^^^^^^^^^

Services Used
-------------

`Read The Docs`_,
`codecov`_,
`AppVeyor`_

From the source top-level directory, Use Pytest as examples below

.. code-block:: sh

  $   py.test -v # All tests
  $   py.test -v -k"csv" # Specific test with expression csv
  $   py.test ./test/test_retriever.py # Specific file

In case ``py.test`` requests for Password (even after Passwordless configuration), change the owner and group
permissions for the config files ``~/.pgpass, ~/.my.cnf``

Style Guide for Python Code
---------------------------

Use ``yapf -d --recursive retriever/ --style=.style.yapf`` to check style.

Use ``yapf -i --recursive retriever/ --style=.style.yapf`` refactor style

Continuous Integration
^^^^^^^^^^^^^^^^^^^^^^

The main GitHub repository runs the test on both the GitHub Actions (Linux) and AppVeyor
(Windows) continuous-integration platforms.

Pull requests submitted to the repository will automatically be tested using
these systems and results reported in the ``checks`` section of the pull request
page.


Create Release
==============

Start
^^^^^

1. **Run the tests**. Seriously, do it now.
2. Update ``CHANGES.md`` with major updates since the last release
3. Run ``python version.py`` (this will update ``version.txt``)
4. Update the version number `bumpversion release` or provide a version as `bumpversion --new-version 3.1.0`
5. On Github draft a release with the version changes. Provide a version as tag and publish.
6. After the release, update the version to dev, run `bumpversion patch`

Release on Test PyPi and PyPi is handled by Github actions.

   ::

       git push upstream main
       git push upstream --tags

Pypi
^^^^

You will need to create an API key on PyPI and store it in ~/.pypirc to upload to PyPI.

1. `sudo python setup.py sdist bdist_wheel`
2. `sudo python -m twine upload -r pypi dist/*`

Cleanup
^^^^^^^

1. Bump the version numbers as needed. The version number is located in the ``setup.py``,
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
source on your machine, but at least based on this recipe it does
not support the distribution of the Mac App to other versions of OS X (i.e.,
if you build the App on OS X 10.9 it will only run on 10.9)

1.  Install Homebrew
    ``ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"``
2.  Install Xcode
3.  Install Python ``brew install python``
4.  Install the Xcode command-line tools ``xcode-select --install``
5.  Make brew’s Python the default
    ``echo export PATH='usr/local/bin:$PATH' >> ~/.bash_profile``
6.  Install xlrd via pip ``pip install xlrd``. No ``sudo`` is necessary since we’re using brew.
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

Once forked, open a pull request to the retriever-feedstock repository. Your package will be tested on Windows, Mac, and Linux.

When your pull request is merged, the package will be rebuilt and become automatically available on conda-forge.

All branches in the conda-forge/retriever-feedstock are created and uploaded immediately, so PRs should be based on branches in forks. Branches in the main repository shall be used to build distinct package versions only.

For producing a uniquely identifiable distribution:

 - If the version of a package is not being incremented, then the build/number can be added or increased.
 - If the version of a package is being incremented, then remember to change the build/number back to 0.

Documentation
=============

We are using `Sphinx`_ and `Read the Docs`_. for the documentation.
Sphinx uses reStructuredText as its markup language.
Source Code documentation is automatically included after committing to the main.
Other documentation (not source code) files are added as new reStructuredText in the docs folder

In case you want to change the organization of the Documentation, please refer to `Sphinx`_

**Update Documentation**

The documentation is automatically updated for changes within modules.
However, the documentation should be updated after the addition of new modules in the engines or lib directory.
Change to the docs directory and create a temporary directory, i.e. ``source``.
Run

.. code-block:: bash

  cd  docs
  mkdir source
  sphinx-apidoc -f  -o ./source /Users/../retriever/

The ``source`` is the destination folder for the source rst files. ``/Users/../retriever/`` is the path to where
the retriever source code is located.
Copy the ``.rst`` files that you want to update to the docs directory, overwriting the old files.
Make sure you check the changes and edit if necessary to ensure that only what is required is updated.
Commit and push the new changes.
Do not commit the temporary source directory.

**Test Documentation locally**

.. code-block:: bash

  cd  docs  # go the docs directory
  make html && python3 -m http.server --directory _build/html
  # Makes the html files and hosts a HTTP server on localhost:8000 to view the documentation pages locally

.. note::
  Do not commit the _build directory after making HTML.

**Read The Docs configuration**

Configure read the docs (advanced settings) so that the source is first installed then docs are built.
This is already set up but could be changed if need be.

Collaborative Workflows with GitHub
===================================

First fork the `Data Retriever repository`_.
Then Clone your forked version with either HTTPS or SSH

   ::

      # Clone with HTTPS
      git clone https://github.com/[myusername]/retriever.git
      # Clone with SSH
      git clone git@github.com:[myusername]/retriever.git

This will update your `.git/config` to point to your repository copy of the Data Retriever as `remote "origin"`

   ::

       [remote "origin"]
       url = git@github.com:[myusername]/retriever.git
       fetch = +refs/heads/*:refs/remotes/origin/*

Point to Weecology `Data Retriever repository`_ repo.
This will enable you to update your main(origin) and you can then push to your origin main.
In our case, we can call this upstream().

   ::

      git remote add upstream https://github.com/weecology/retriever.git

This will update your `.git/config` to point to the Weecology `Data Retriever repository`_.

.. code-block:: bash

  [remote "upstream"]
  url = https://github.com/weecology/retriever.git
  fetch = +refs/heads/*:refs/remotes/upstream/*
  # To fetch pull requests add
  fetch = +refs/pull/*/head:refs/remotes/origin/pr/*

Fetch upstream main and create a branch to add the contributions to.

.. code-block:: bash

  git fetch upstream
  git checkout main
  git reset --hard upstream main
  git checkout -b [new-branch-to-fix-issue]

**Submitting issues**

Categorize the issues based on labels. For example (Bug, Dataset Bug, Important, Feature Request, etc..)
Explain the issue explicitly with all details, giving examples and logs where applicable.

**Commits**

From your local branch of retriever, commit to your origin.
Once tests have passed you can then make a pull request to the retriever main (upstream)
For each commit, add the issue number at the end of the description with the tag ``fixes #[issue_number]``.

Example
::

  Add version number to postgres.py to enable tracking

  Skip a line and add more explanation if needed
  fixes #3

**Clean history**

Make one commit for each issue.
As you work on a particular issue, try adding all the commits into one general commit rather than several commits.

Use ``git commit --amend`` to add new changes to a branch.

Use ``-f`` flag to force pushing changes to the branch. ``git push -f origin [branch_name]``


.. _codecov: https://codecov.io/
.. _project website: http://data-retriever.org
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _Read The Docs: https://readthedocs.org/
.. _AppVeyor: https://www.appveyor.com/
.. _documentation: https://pythonhosted.org/an_example_pypi_project/setuptools.html
.. _installing: https://docs.python.org/3.6/install/
.. _installing the wheel: http://www.lfd.uci.edu/~gohlke/pythonlibs/
.. _setup tools: https://pythonhosted.org/an_example_pypi_project/setuptools.html
.. _Data Retriever repository: https://github.com/weecology/retriever
.. _Spatial database setup: developer.html#Spatial-database-setup
.. _PostgresSQL: https://www.postgresql.org/download/
.. _SQlite: https://sqlite.org/download.html
.. _MySQL: https://www.mysql.com/downloads/
.. _MSAccess: https://www.microsoft.com/en-ww/microsoft-365/access
.. _PostgreSQL Password File : https://www.postgresql.org/docs/current/libpq-pgpass.html
.. _MySQL Password File : https://dev.mysql.com/doc/refman/8.0/en/option-files.html