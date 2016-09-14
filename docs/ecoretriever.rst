==================================
Using the Data Retriever from R
==================================

Ecoretriever
~~~~~~~~~~~~

The `Data Retriever`_ provides an R interface to the Data Retriever so
that the Retriever's data handling can easily be integrated into R workflows.

Installation
~~~~~~~~~~~~

To use the R package ``ecoretriever``, you first need to `install the Retriever <introduction.html#installing-binaries>`_.

The ``ecoretriever`` can then be installed using
``install.packages("ecoretriever")``

To install the development version, use ``devtools``

::

  # install.packages("devtools")
  library(devtools)
  install_github("ropensci/ecoretriever")

Note: The R package takes advantage of the Data Retriever's command line
interface, which must be available in the path. This should occur automatically
when following the installation instructions for the Retriever.


Examples
~~~~~~~~

::

 library(ecoretriever)
 
 # List the datasets available via the Retriever
 ecoretriever::datasets()
 
 # Install the Gentry dataset into csv files in your working directory
 ecoretriever::install('Gentry', 'csv')
 
 # Download the raw Gentry dataset files without any processing to the 
 # subdirectory named data
 ecoretriever::download('Gentry', './data/')
 
 # Install and load a dataset as a list
 Gentry = ecoretriever::fetch('Gentry')
 names(Gentry)
 head(Gentry$counts)


To get citation information for the ``ecoretriever`` in R use ``citation(package = 'ecoretriever')``:


.. _Data Retriever: http://data-retriever.org
