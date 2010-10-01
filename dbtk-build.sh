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
sudo rm dbtk/dbtk-build.sh

# make apidocs
cd .. # current-release
sudo pydoctor --add-package=src/dbtk --make-html
cd src/dbtk # current-release/src/dbtk
sudo cp apidocs/*.* ../../apidocs/
sudo rm apidocs -rf

# build deb package
sudo python setup.py --command-packages=stdeb.command bdist_deb
sudo rm dbtk.egg-info build dist -rf
cd deb_dist # current-release/src/dbtk/deb_dist
cp *.deb ../
cd .. # current-release/src/dbtk
sudo rm deb_dist -rf
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
tar czvf dbtk-1.0.tar.gz dbtk
