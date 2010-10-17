#!/bin/bash

# cleanup, then create current-release folder
sudo rm current-release -rf
mkdir current-release
cd current-release # current-release

# create src folder and checkout from SVN
mkdir src
cd src # current-release/src
svn checkout https://weecology.svn.beanstalkapp.com/dbtk/trunk/
mv trunk dbtk
cd dbtk # current-release/src/dbtk

# generate version.txt and put it in current-release root folder
python version.py
mv version.txt ../../

# remove non-source files from source directory
sudo rm build.sh make-windows-executables.bat version.py
mv categories ../../
mv scripts ../../
cd .. # current-release/src
cd .. # current-release
sudo rm categories/.svn -rf
sudo rm scripts/.svn scripts/*.pyc -rf

# make apidocs
sudo pydoctor --add-package=src/dbtk --make-html
cd src/dbtk # current-release/src/dbtk
sudo cp apidocs/*.* ../../apidocs/
sudo rm apidocs -rf

# build deb package
sudo python setup.py --command-packages=stdeb.command bdist_deb
sudo rm dbtk.egg-info build dist __init__.pyc -rf
cd deb_dist # current-release/src/dbtk/deb_dist
cp *.deb ../
cd .. # current-release/src/dbtk
sudo rm deb_dist stdeb.cfg -rf
mkdir linux
mv *.deb linux/
mv linux ../../
sudo rm .svn -rf
cd lib # current-release/src/dbtk/lib
sudo rm .svn -rf
cd ../scripts # current-release/src/dbtk/scripts
sudo rm .svn -rf
cd .. # current-release/src/dbtk

# build src package
cd .. # current-release/src
tar czvf dbtk-src.tar.gz dbtk
