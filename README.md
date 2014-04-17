ecoretriever
============

R interface to the [EcoData Retriever](http://ecodataretriever.org).

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

Add Retriever to the path
-------------------------
The R package takes advantage of the EcoData Retriever's command line interface which must be enabled by adding it to the path on Windows and Mac platforms.

**Windows Specific Instructions**
*Temporarily add retriever to path*
In an active R session the following commands will temporaily add the retriever to the path:

```coffee
## first check that retriever is not already on the path
grepl('EcoDataRetriever', Sys.getenv('PATH'))
#[1] FALSE
## add to existing path
newpath = paste(Sys.getenv('PATH'), 'C:\\Program Files\\EcoDataRetriever', sep=';')
Sys.setenv('PATH' = newpath)
```
*Permanently add retriever to path*
How you set the path (aka environment variable) is system specific: * Under Windows 2000/XP/2003 you can use 'System' in the control panel or the properties of 'My Computer' (under the 'Advanced' tab). * Under Vista and Windows 7, go to 'User Accounts' in the control panel, and select your account and then 'Change my environment variables'

Once you are in the change environment variable box, select “New”. Name the new variable “PATH” and then set the value to (at a minimum):

PATH=C:/Program Files/EcoDataRetriever;

Install R package
-----------------

To install the development version of the R package `ecoretriever`, use the `devtools` package:

```coffee
# install.packages("devtools")
library(devtools)
install_github("ecoretriever", "ropensci")
```

Examples
--------
```coffee
library(ecoretriever)

# List the datasets available via the Retriever
data_ls()

# Install the Gentry dataset into csv files in your working directory
install_data('Gentry', 'csv')

# Download the raw Gentry dataset files without any processing to the `data` subdirectory
download_data('Gentry', './data/')

# Install and load a dataset as a list
Gentry = fetch('Gentry')
names(Gentry)
head(Gentry$counts)

# Update the Retriever scripts
update_scripts()

# Create a new example Retriever script
new_script('newdataset.script')
```
