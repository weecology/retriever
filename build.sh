#!/bin/bash

# setup
sudo python setup.py install
python version.py
sudo rm build dist __init__.pyc deb_dist packages -rf
mkdir packages

# create source tarball
sudo python setup.py sdist
sudo mv dist/*.tar.gz packages

# build deb package
sudo python setup.py --command-packages=stdeb.command bdist_deb
sudo mv deb_dist/*.deb packages
sudo rm retriever.egg-info build dist __init__.pyc deb_dist -rf
