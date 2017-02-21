rdataretriever 1.0.0
====================

NEW PACKAGE NAME

* The `EcoData Retriever` has been renamed to `Data Retriever` to reflect its 
utility outside of ecological data and consequently we have renamed the R package
from `ecoretriever` to `rdataretriever`

NEW COAUTHORS

* We welcome Henry Senyondo and Shawn Taylor as coauthors on the package. Thanks
for the great help Henry and Shawn!

NEW FEATURES

* Add `reset` which allows a user to delete all the `Data Retriever` downloaded
files

MINOR IMPROVEMENTS

* Accomodate new retriever naming conventions in fetch
* Don't change the class or return the update log
* Specify in documentation which functions are for internal use.
* Change dataset names in source and README.md

BUG FIXES

* Search for Anaconda installs of the `Data Retriever`

ecoretriever 0.3.0
==================

MINOR IMPROVEMENTS

* Improve documentation for using the connection file

BUG FIXES

* Fix issues with running on some Windows machines by using `shell()` instead of
  `system()` on Windows
* Fix new `--subdir` functionality (released in 0.2.2)


ecoretriever 0.2
================

NEW FEATURES
* We added a new function `get_updates` which can be used to update the `retriever` scripts. This is a big improvement for users because it avoids automatically updating the scripts every time the package is imported. The log of the scripts update can be printed in a cleaner format as well. 
* Added support for maintaining subdirectory structure when using the function `download`. 

MINOR IMPROVEMENTS

* default data_dir argument is now set to working directory rather than NULL for the function `install()`

BUG FIXES

* On windows machine if the data directory was not specified for a dataset install an error would occur. Now the dataset directory is always specified in external calls to `retriever install ...`

