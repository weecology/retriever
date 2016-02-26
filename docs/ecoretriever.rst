==================================
Using the EcoData Retriever from R
==================================

Ecoretriever
~~~~~~~~~~~~

R interface to the `EcoData Retriever`_..


Provides an R interface to the EcoData Retriever via the EcoData Retriever's command line interface.

The EcoData Retriever automates the tasks of finding, downloading, and cleaning
up publicly available ecological data, and then stores them in a local database
or csv files. This lets ecologists spend less time cleaning up and managing
data, and more time doing science.

This package lets you access the Retriever using R, so that the Retriever's data
handling can easily be integrated into R workflows.

Installation
~~~~~~~~~~~~

To use the R package ``ecoretriever``, you first need to install the Retriever.
The Retriever's installers are available for all major operating systems from the `Download page`_
or it can be installed from `source`_.

The required installers for `Ecoretriever`_ can be found on the `CRAN page`_.
 
Add Retriever to the path
~~~~~~~~~~~~~~~~~~~~~~~~~
The R package takes advantage of the EcoData Retriever's command line interface
which must be enabled by adding it to the path on Mac platforms.
On a Windows platform the Retriever should be added automatically to the path.

Install R package
~~~~~~~~~~~~~~~~~

To install the development version of the R package ``ecoretriever``, use the ``devtools`` package

::

  # install.packages("devtools")
  library(devtools)
  install_github("ropensci/ecoretriever")

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

Acknowledgments
~~~~~~~~~~~~~~~

A big thanks to Ben Morris for helping to develop the EcoData Retriever. 
Thanks to the rOpenSci team with special thanks to Gavin Simpson, Scott Chamberlain, and Karthik Ram who gave helpful advice and fostered the development of this R package.
Development of this software was funded by the `National Science Foundation`_ as part of a `CAREER award to Ethan White`_.

.. _National Science Foundation: http://nsf.gov/
.. _CAREER award to Ethan White: http://nsf.gov/awardsearch/showAward.do?AwardNumber=0953694
.. _EcoData Retriever: http://ecodataretriever.org
.. _Download page: http://ecodataretriever.org/download.html
.. _source: https://github.com/weecology/retriever
.. _Ecoretriever: https://github.com/ropensci/ecoretriever/
.. _CRAN page: https://cran.r-project.org/web/packages/ecoretriever/index.html
