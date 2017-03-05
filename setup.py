"""Use the following command to install retriever: python setup.py install"""
from __future__ import absolute_import

from setuptools import setup
from pkg_resources import parse_version
import platform
import sys
import warnings
import os
import subprocess

current_platform = platform.system().lower()
extra_includes = []
if current_platform == "darwin":
    if(subprocess.check_output("[ ! -f .git/hooks/pre-commit ] && echo \"Not Found\"") == "Not Found"):
      os.system("chmod +x hooks/pre-commit")
      os.system("cp -p hooks/pre-commit .git/hooks/pre-commit")
    else:
      os.system("ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit")
    try:
        import py2app
    except ImportError:
        pass
    extra_includes = []
elif current_platform == "windows":
    os.system("chmod +x hooks/pre-commit")
    os.system("mklink hooks/pre-commit .git/hooks/pre-commit")
    try:
        import py2exe
    except ImportError:
        pass
    import sys
    extra_includes = ['pyodbc', 'inspect']
    sys.path.append(
        "C:\\Windows\\winsxs\\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91")

__version__ = 'v2.0.0'
with open("_version.py", "w") as version_file:
    version_file.write("__version__ = " + "'" + __version__ + "'\n")
    version_file.close()


def clean_version(v):
    return parse_version(v).__repr__().lstrip("<Version('").rstrip("')>")

packages = [
    'retriever.lib',
    'retriever.engines',
    'retriever',
]

includes = [
    'xlrd',
    'future',
    'pymysql',
    'psycopg2',
    'sqlite3',
] + extra_includes

excludes = [
    'pyreadline',
    'doctest',
    'pickle',
    'pdb',
    'pywin', 'pywin.debugger',
    'pywin.debugger.dbgcon',
    'pywin.dialogs', 'pywin.dialogs.list',
    'Tkconstants', 'Tkinter', 'tcl', 'tk'
]

setup(name='retriever',
      version=clean_version(__version__),
      description='Data Retriever',
      author='Ben Morris, Akash Goel, Henry Senyondo, Ethan White',
      author_email='ethan@weecology.org',
      url='https://github.com/weecology/retriever',
      classifiers=['Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',],
      packages=packages,
      package_dir={
          'retriever': ''
      },
      entry_points={
          'console_scripts': [
              'retriever = retriever.__main__:main',
          ],
      },
      install_requires=[
          'xlrd',
          'future'
      ],

      # py2app flags
      app=['__main__.py'],
      data_files=[('', ['CITATION'])],
      setup_requires=[],
      )


try:
    from retriever.compile import compile
    from retriever.lib.repository import check_for_updates
    compile()
    check_for_updates()
except:
    pass
