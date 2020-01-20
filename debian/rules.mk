#!/usr/bin/make -f

%:
    dh $@ --with python-virtualenv

override_dh_virtualenv:
    dh_virtualenv --python /usr/bin/python3.5 \
        --setuptools

override_dh_builddeb:
    dh_builddeb --destdir=/tmp/python-deb-pkg/debian/dist