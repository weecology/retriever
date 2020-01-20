# ------------------------------------------------------------------------- #
# DEBIAN PACKAGE CONTROL FILE                                               #
#                                                                           #
# This file is a Debian control file. For more information on the config in #
# this file, please run `man deb-control`.                                  #
# ------------------------------------------------------------------------- #

Source: python-deb-pkg
Section: contrib/python
Priority: extra
Maintainer: weecology/retriever
Build-Depends: debhelper (>= 9), python3.5, python3-setuptools, dh-virtualenv (>> 0.6)
Standards-Version: 3.9.5

Package: python-deb-pkg
Architecture: any
Pre-Depends: dpkg (>= 1.16.1),  python3.5
Depends: make
Description: python-deb-pkg service