"""Use the following command to install retriever: python setup.py install"""
from __future__ import absolute_import

import platform
import os

from setuptools import setup
from pkg_resources import parse_version

current_platform = platform.system().lower()
extra_includes = []

if os.path.exists(".git/hooks"):  # check if we are in git repo
    os.system("cp hooks/pre-commit .git/hooks/pre-commit")
    os.system("chmod +x .git/hooks/pre-commit")


__version__ = 'v2.0.0'
with open(os.path.join("retriever", "_version.py"), "w") as version_file:
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
    'argcomplete',
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
                   'Programming Language :: Python :: 3', ],
      packages=packages,
      package_dir={
          'retriever': 'retriever'
      },
      entry_points={
          'console_scripts': [
              'retriever = retriever.__main__:main',
          ],
      },
      install_requires=[
          'xlrd',
          'future',
          'argcomplete'
      ],

      # py2app flags
      app=['__main__.py'],
      data_files=[('', ['CITATION'])],
      setup_requires=[],
      )

# windows doesn't have bash. No point in using bash-completion
if current_platform != "windows":
    # if platform is OS X use "~/.bash_profile"
    if current_platform == "darwin":
        bash_file = "~/.bash_profile"
    # if platform is Linux use "~/.bashrc
    elif current_platform == "linux":
        bash_file = "~/.bashrc"
    # else write and discard
    else:
        bash_file = "/dev/null"

    argcomplete_command = 'eval "$(register-python-argcomplete retriever)"'
    with open(os.path.expanduser(bash_file), "a+") as bashrc:
        bashrc.seek(0)
        # register retriever for arg-completion if not already registered
        # whenever a new shell is spawned
        if argcomplete_command not in bashrc.read():
            bashrc.write(argcomplete_command + "\n")
            bashrc.close()
    os.system("activate-global-python-argcomplete")
    # register for the current shell
    os.system(argcomplete_command)

try:
    from retriever.compile import compile
    from retriever.lib.repository import check_for_updates
    compile()
    check_for_updates()
except:
    pass
