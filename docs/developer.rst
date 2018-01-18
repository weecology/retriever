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
PostgreSQL and creating the .pgpass file as described below:

::

  MySQL
  -----
  mysql -e "CREATE USER 'travis'@'localhost';" -uroot
  mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'travis'@'localhost';" -uroot
  mysql -e "GRANT FILE ON *.* TO 'travis'@'localhost';" -uroot
  ​
  PostgreSQL
  ----------
  psql -c "CREATE USER postgres WITH PASSWORD 'Password12!'"
  psql -c 'CREATE DATABASE testdb'
  psql -c 'GRANT ALL PRIVILEGES ON DATABASE testdb to postgres'
  ​
  Create .pgpass in your home directory:
  localhost:*:testdb:postgres:Password12!

To run tests we use pytest.
From the source top level directory, run

.. code-block:: sh

  $   py.test


To run tests on a specific test category add the path of the test module to the end of the py.test command: 

.. code-block:: sh

  $   py.test ./test/test_retriever.py

This will only run test_retriever.py

Continuous Integration
^^^^^^^^^^^^^^^^^^^^^^

The main GitHub repository runs test on both the Travis (Linux) and AppVeyor
(Windows) continuous integration platforms.

Pull requests submitted to the repository will automatically be tested using
these systems and results reported in the ``checks`` section of the pull request
page.

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

