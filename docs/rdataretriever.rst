==================================
Using the Data Retriever from R
==================================

rdataretriever
~~~~~~~~~~~~~~

The `Data Retriever`_ provides an R interface to the Data Retriever so
that the Retriever's data handling can easily be integrated into R workflows.

Installation
~~~~~~~~~~~~

To use the R package ``rdataretriever``, you first need to `install the Retriever <introduction.html#installing-binaries>`_.

The ``rdataretriever`` can then be installed using
``install.packages("rdataretriever")``

To install the development version, use ``devtools``

::

  # install.packages("devtools")
  library(devtools)
  install_github("ropensci/rdataretriever")

Note: The R package takes advantage of the Data Retriever's command line
interface, which must be available in the path. This should occur automatically
when following the installation instructions for the Retriever.


Examples
~~~~~~~~

::

 library(rdataretriever)
 
 # List the datasets available via the Retriever
 rdataretriever::datasets()
 
 # Install the Gentry forest transects dataset into csv files in your working directory
 rdataretriever::install('gentry-forest-transects', 'csv')
 
 # Download the raw Gentry dataset files without any processing to the 
 # subdirectory named data
 rdataretriever::download('gentry-forest-transects', './data/')
 
 # Install and load a dataset as a list
 Gentry = rdataretriever::fetch('gentry-forest-transects')
 names(gentry-forest-transects)
 head(gentry-forest-transects$counts)


To get citation information for the ``rdataretriever`` in R use ``citation(package = 'rdataretriever')``:


.. _Data Retriever: http://data-retriever.org
