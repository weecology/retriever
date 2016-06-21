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

