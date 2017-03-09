rdataretriever [![Build Status](https://cranlogs.r-pkg.org/badges/grand-total/ecoretriever)](https://cran.rstudio.com/web/packages/ecoretriever/index.html)
============

R interface to the [Data Retriever](http://data-retriever.org).

The Data Retriever automates the tasks of finding, downloading, and cleaning up
publicly available data, and then stores them in a local database or csv
files. This lets data analysts spend less time cleaning up and managing data,
and more time analyzing it.

This package lets you access the Retriever using R, so that the Retriever's data
handling can easily be integrated into R workflows.

Installation
------------
To use the R package `rdataretriever` you first need to install the Retriever.
Installers are available for all major operating systems from the [Install page](http://www.data-retriever.org/#install)
or it can be installed from [source](https://github.com/weecology/retriever).

Add Retriever to the path
-------------------------
The R package takes advantage of the Data Retriever's command line interface
which must be enabled by adding it to the path on Mac platforms.
On a Windows platform the Retriever should be added automatically to the path.

Install R package
-----------------

To install the development version of the R package `rdataretriever`, use the `devtools` package:

```coffee
# install.packages("devtools")
library(devtools)
install_github("ropensci/rdataretriever")
```

Examples
--------
```coffee
library(rdataretriever)

# List the datasets available via the Retriever
rdataretriever::datasets()

# Install the portal into csv files in your working directory
rdataretriever::install('portal', 'csv')

# Download the raw portal dataset files without any processing to the
# subdirectory named data
rdataretriever::download('portal', './data/')

# Install and load a dataset as a list
portal = rdataretriever::fetch('portal')
names(portal)
head(portal$species)
```

To get citation information for the `rdataretriever` in R use `citation(package = 'rdataretriever')`

Acknowledgements
----------------
A big thanks to Ben Morris for helping to develop the Data Retriever.
Thanks to the rOpenSci team with special thanks to Gavin Simpson,
Scott Chamberlain, and Karthik Ram who gave helpful advice and fostered
the development of this R package.
Development of this software was funded by the [National Science Foundation](http://nsf.gov/)
as part of a [CAREER award to Ethan White](http://nsf.gov/awardsearch/showAward.do?AwardNumber=0953694).

---
[![ropensci footer](http://ropensci.org/public_images/github_footer.png)](http://ropensci.org)
