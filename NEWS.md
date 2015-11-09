ecoretriever 0.2
================

NEW FEATURES
* We added a new function `get_updates` which can be used to update the `retriever` scripts. This is a big improvement for users becuase the past behavior everytime the package was loaded it updated its scripts which resulted in annoying lag times. The log of the scripts update can be printed pretty easily as well. 

MINOR IMPROVEMENTS

* default data_dir argument is now set to working directory rather than NULL for the function `install()`

BUG FIXES

* On windows machine if the data directory was not specified for a dataset install an error would occur. Now the dataset directory is always specified in external calls to `retriever install ...`

