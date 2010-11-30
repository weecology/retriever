#!/bin/bash

# cleanup, then create current-release folder
sudo rm current-release -rf
mkdir current-release
cd current-release # current-release

# create src folder and checkout from SVN
mkdir src
cd src # current-release/src
svn checkout https://weecology.svn.beanstalkapp.com/dbtk/trunk/
mv trunk retriever
cd retriever # current-release/src/retriever

# remove non-source files from source directory
sudo rm build.sh make-windows-executables.bat
mv categories ../../
mv scripts ../../
cd ../.. # current-release
sudo rm categories/.svn -rf
sudo rm scripts/.svn -rf

# install latest version
cd src/retriever # current-release/src/retriever
sudo python setup.py install

# generate version.txt and put it in current-release root folder
mv version.py ../../
cd ../.. # current-release
python version.py
sudo rm version.py scripts/*.pyc

# make apidocs
sudo pydoctor --add-package=src/retriever --make-html
cd src/retriever # current-release/src/retriever
sudo cp apidocs/*.* ../../apidocs/
sudo rm apidocs -rf

# build deb package
sudo python setup.py --command-packages=stdeb.command bdist_deb
sudo rm retriever.egg-info build dist __init__.pyc -rf
cd deb_dist # current-release/src/retriever/deb_dist
cp *.deb ../
cd .. # current-release/src/retriever
sudo rm deb_dist stdeb.cfg -rf
mkdir linux
mv *.deb linux/
mv linux ../../
mv globe.ico ../
sudo rm .svn lib/.svn engines/.svn app/.svn -rf

# build src package
cd .. # current-release/src
tar czvf retriever-src.tar.gz retriever
mv globe.ico retriever/
