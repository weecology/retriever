==============
Create Release
==============

Start
-----

1. **Run the tests**. Seriously, do it now.
2. In the `master` branch update the version number in ``setup.py`` (if it
   hasn’t already been bumped)
3. Run ``python version.py`` (this will update ``version.txt``)
4. Update the version number in ``retriever_installer.iss`` (if it
   hasn’t already been bumped)
5. Update ``CHANGES.md`` with major updates since last release
6. Commit changes
7. Add a tag with appropriate version number, e.g.
   ,\ ``git tag -a v1.8.0 -m "Version 1.8.0"``
8. Push the release commit and the tag

   ::

       git push upstream master
       git push upstream --tags

Linux
-----

1. **Run the tests** (unless you just ran them on the same machine)
2. Checkout master
3. Run ``bash build.sh``

Windows
-------

1. **Run the tests**. This helps makes sure that the build environment
   is properly set up.
2. Checkout master
3. Run ``build_win``

Mac
---

1. **Run the tests**. This helps makes sure that the build environment
   is properly set up.
2. Checkout master
3. Run ``bash build_mac``. This creates a folder called “mac” with two
   files; retriever.app and retriever.zip
4. Install the retriever for verification. Reference
   http://www.data-retriever.org/download.html

Pypi
----

1. sudo python setup.py sdist upload

Cleanup
-------

1. Bump the version numbers in ``__init__.py`` and
   ``retriever_installer.iss``
2. In ``__init__.py`` change ``MASTER = False`` to ``MASTER = True``
