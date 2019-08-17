====================
Retriever Provenance
====================

Retriever allows committing of datasets and installation of the committed dataset into the database of your choice at a
later date.
This ensures that the previous outputs/results can be produced easily.

Provenance Directory
====================
The directory to save your committed dataset can be defined by setting the environment variable ``PROVENANCE_DIR``.
However, you can still save the committed dataset in a directory of your choice by defining the ``path`` while committing
the dataset.

Commit Datasets
===============

Retriever supports committing of a dataset into a compressed archive.


.. code-block:: python

  def commit(dataset, commit_message='', path=None, quiet=False):

A description of the default parameters mentioned above:

.. code-block:: python

  dataset               (String): Name of the dataset.

  commit_message        (String): Specify commit message for a commit.

  path                  (String): Specify the directory path to store the compressed archive file.

  quiet                   (Bool): Setting True minimizes the console output.


Example to commit dataset:

.. code-block:: bash

   retriever commit abalone-age -m "Example commit" --path .
   Committing dataset abalone-age
   Successfully committed.


.. code-block:: python

  >>> from retriever import commit
  >>> commit('abalone-age', commit_message='Example commit', path='/home/')

If the path is not provided the committed dataset is saved in the ``provenance directory``.

Log Of Committed Datasets
=========================
You can view the log of commits of the datasets stored in the provenance directory.

.. code-block:: python

  def commit_log(dataset):

A description of the parameter mentioned above:

.. code-block:: python

  dataset       (String): Name of the dataset.

Example:

.. code-block:: bash

  retriever log abalone-age

  Commit message: Example commit
  Hash: 02ee77
  Date: 08/16/2019, 16:12:28


.. code-block:: python

  >>> from retriever import commit_log
  >>> commit_log('abalone-age')


Installing Committed Dataset
============================
You can install committed datasets by using the hash-value or by providing the path of the compressed archive.
Installation using hash-value is supported only for datasets stored in the provenance directory.

For installing dataset from a committed archive you can provide the path to the archive in place of dataset name:

.. code-block:: bash

  retriever install sqlite abalone-age-02ee77.zip

.. code-block:: python

  >>> from retriever import install_sqlite
  >>> install_sqlite('abalone-age-02ee77.zip')

Also, you can install using the hash-value of the datasets stored in provenance directory. You can always look up the
hash-value of your previous commits using the command ``retriever log dataset_name``.

For installing dataset from provenance directory provide the ``hash-value`` of the commit.

.. code-block:: bash

  retriever install sqlite abalone-age --hash-value 02ee77

.. code-block:: python

  >>> from retriever import install_sqlite
  >>> install_sqlite('abalone-age', hash_value='02ee77')
