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
  psycopg2 (PostgreSQL)
  pyodbc (MS Access).
  py2app (Mac)
  py2exe (Windows)

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

  $ pip setup.py install

or install in development mode.

.. code-block:: bash

  $  pip setup.py develop

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

To run tests we use pytest.
From the source top level directory, run

.. code-block:: sh

  $   py.test


In case we want to run tests on a specific test category, we add the path of the test module, py.test [path]

.. code-block:: sh

  $   py.test ./test/test_retriever.py

This will only run test_retriever.py

Continuous Integration
^^^^^^^^^^^^^^^^^^^^^^

The main GitHub repository runs test on both the Travis (Linux) and AppVeyor
(Windows) continuous integration platforms.

Pull requests submitted to the repository will automatically be tested using
these systems and results reported in the `checks` section of the pull request
page.

Services Used
-------------

Check the services' home pages in case you have to add the same capabilities to your master branch.

::

  Travis
  AppVeyor
  readthedocs
  codecov


links `Read The Docs`_, `codecov`_, `AppVeyor`_ and  `Travis`_

After installing the servers we need to configure them by granting privileges to our testing user .

::

  MySQL
  -----
  GRANT ALL PRIVILEGES ON testdb.* TO 'travis'@'localhost';
  GRANT FILE ON *.* TO 'travis'@'localhost';
  ​
  Install MySQL on Mac
  --------------------
  ​
     brew install mysql
  ​
  Follow instructions for starting/autostarting
  ​
  PostgreSQL
  ----------
  psql -c "CREATE USER postgres WITH PASSWORD 'testpass'"
  psql -c 'CREATE DATABASE testdb'
  psql -c 'GRANT ALL PRIVILEGES ON DATABASE testdb to postgres'
  ​
  Create .pgpass in your home directory:
  localhost:*:testdb:postgres:testpass

Documentation
=============

We are using `Sphinx`_ and `Read the Docs`_. for the documentation.
Sphinx uses reStructuredText as its markup language.
Source Code documentation is automatically included after committing to the master.
Other documentation (not source code) files are added as new reStructuredText in the docs folder

In case you want to change the organization of the Documentation, please refer to `Sphinx`_

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

Example; ``add version number to postgres.py to enable tracking. fixes #3``

**Clean histroy**

We try to make one commit for each issue.
As you work on an issue, try adding all the commits into one general commit rather than several commits.

Use ``git commit --amend`` to add new changes to a branch.

Use ``-f`` flag to force pushing changes to the branch. ``git push -f origin [branch_name]``


.. _codecov: https://codecov.io/
.. _project website: http://ecodataretriever.org
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _Read The Docs: https://readthedocs.org//
.. _Travis: https://travis-ci.org/
.. _AppVeyor: https://www.appveyor.com/
.. _documentation: https://pythonhosted.org/an_example_pypi_project/setuptools.html
.. _installing: https://docs.python.org/2/install/
.. _installing the wheel: http://www.lfd.uci.edu/~gohlke/pythonlibs/
.. _setup tools: https://pythonhosted.org/an_example_pypi_project/setuptools.html
