# v2.0.0

## Major changes

* Add Python 3 support, python 2/3 compatibility
* Add json and xml as output formats
* Switch to using the frictionless data datapackage json standard. This a
  **backwards incompatible change** as the form of dataset description files the
  retriever uses to describe the location and processing of simple datasets has
  changed.
* Add CLI for creating, editing, deleting datapackage.json scripts
* Broaden scope to include non-ecological data and rename to Data Retriever
* Major expansion of documentation and move documentation to Read the Docs
* Add developer documentation
* Remove the GUI
* Use csv module for reading of raw data to improve handling of newlines in fields
* Major expansion of integration testing
* Refactor regression testing to produce a single hash for a dataset regardless
  of output format
* Add continuous integration testing for Windows


## Minor changes

* Use pyinstaller for creating exe for windows and app for mac and remove py2app
* Use 3 level semantic versioning for both scripts and core code
* Rename datasets with more descriptive names
* Add a retriever minimum version for each dataset
* Rename dataset description files to follow python modules conventions
* Switch to py.test from nose
* Expand unit testing
* Add version requirements for sqlite and postgresql
* Default to latin encoding
* Improve UI for updating user on downloading and processing progress


## New datasets

* Added machine Learning datasets from UC Irvine's machine learning data sets

# v1.8.3

* Fixed regression in GUI

# v1.8.2

* Improved cleaning of column names
* Fixed thread bug causing Gentry dataset to hang when installed via GUI
* Removed support for 32-bit only Macs in binaries
* Removed unused code

# v1.8.0

* Added scripts for 21 new datasets: leaf herbivory, biomass allocation,
  community dynamics of shortgrass steppe plants, mammal and bird foraging
  attributes, tree demography in Indian, small mammal community dynamics in
  Chile, community dynamics of Sonoran Desert perennials, biovolumes of
  freshwater phytoplankton, plant dynamics in Montana, Antarctic Site Inventory
  breeding bird survey, community abundance data compiled from the literature,
  spatio-temporal population data for butterflies, fish parasite host ecological
  characteristics, eBird, Global Wood Density Database, multiscale community
  data on vascular plants in a North Carolina, vertebrate home range sizes,
  PRISM climate data, Amniote life history database, woody plan Biomass And
  Allometry Database, Vertnet data on amphibians, birds, fishes, mammals,
  reptiles
* Added `reset` command to allow resetting database configuration settings,
  scripts, and cached raw data
* Added Dockerfile for building docker containers of each version of the
  software for reproducibility
* Added support for wxPython 3.0
* Added support for `tar` and `gz` archives
* Added support for archive files whose contents don't fit in memory
* Added checks for and use of system proxies
* Added ability to download archives from web services
* Added tests for regressions in download engine
* Added `citation` command to provide information on citing datasets
* Improved column name cleanup
* Improved whitespace consistency
* Improved handling of Excel files
* Improved function documentation
* Improved unit testing and added coverage analysis
* Improved the sample script by adding a url field
* Improved script loading behavior by only loading a script the first time it is
  discovered
* Improved operating system identification
* Improved download engine by allowing ability to maintain archive and
  subdirectory structure (particular relevant for spatial data)
* Improved cross-platform directory and line ending handling
* Improved testing across platforms
* Improved checking for updated scripts so that scripts are only downloaded if
  the current version isn't available
* Improved metadata in setup.py
* Fixed type issues in Portal dataset
* Fixed GUI always downloading scripts instead of checking if it needed to
* Fixed bug that sometimes resulted in `.retriever` directories not belonging to
  the user who did the installation
* Fixed issues with downloading files to specific paths
* Fixed BBS50 script to match newer structure of the data
* Fixed bug where csv files were not being closed after installation
* Fixed errors when closing the GUI
* Fixed issue where enclosing quotes in csv files were not being respected
  during cross-tab restructuring
* Fixed bug causing v1.6 to break when newer scripts were added to `version.txt`
* Fixed Bioclim script to include `hdr` files
* Fixed missing icon images on Windows
* Removed unused code

# v1.7.0

* Added ability to download files directly for non-tabular data
* Added scripts to download Bioclim and Mammal Supertree data
* Added a script for the MammalDIET database
* Fixed bug where some nationally standardized FIA surveys where not included
* Added check for wxpython on installation to allow non-gui installs
* Fixed several minor issues with Gentry script including a missing site and a column in one file that was misnamed
* Windows install now adds the retriever to the path to facilitate command line use
* Fixed a bug preventing installation from PyPI
* Added icons to installers
* Fixed the retriever failing when given a script it couldn't handle

# v1.6.0

* Added full OS X support to the Retriever
* Added a proper Windows installer
* Fixed a number of bugs
