ecoretriever
============

R interface to the [EcoData Retriver](http://ecodataretriever.org).

The EcoData Retriever automates the tasks of finding, downloading, and cleaning
up publicly available ecological data, and then stores them in a local database
or csv files. This lets ecologists spend less time cleaning up and managing
data, and more time doing science.

This package lets you access the Retriever using R, so that the Retriever's data
handling can easily be integrated into R workflows.

Installation
------------
To use the R package `ecoretriever` you first need to install the Retriever.
Installers are available for all major operating systems from the [Download page](http://ecodataretriever.org/download.html) or it can be installed from [source](https://github.com/weecology/retriever).


To install the development version of the R package `ecoretriever`, use the `devtools` package:

```coffee
# install.packages("devtools")
library(devtools)
install_github("ecoretriever", "ropensci")
```

Example
-------
```coffee
library(ecoretriever)

# Download the Gentry dataset to csv files in your working directory
download_publict_data('Gentry', 'csv')
```
