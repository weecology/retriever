#!/bin/bash

# create src folder
sudo rm src -rf
mkdir src
mkdir src/retriever
cp -r app/ src/
cp -r lib/ src/
cp -r engines/ src/
cp __init__.py src
cp main.py src
cp setup.py src

sudo python setup.py install
python version.py

# build deb package
sudo python setup.py --command-packages=stdeb.command bdist_deb
sudo rm retriever.egg-info build dist __init__.pyc -rf
sudo rm linux -rf
mkdir linux
sudo mv deb_dist/*.deb linux
sudo rm deb_dist -rf

# build src package
tar czvf retriever-src.tar.gz src
