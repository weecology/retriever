"""Use the following command to install retriever: python setup.py install"""
from __future__ import absolute_import

import os
import platform

from pkg_resources import parse_version
from setuptools import setup, find_packages

current_platform = platform.system().lower()
extra_includes = []
if current_platform == "windows":
    extra_includes += ["pypyodbc"]

if os.path.exists(".git/hooks"):  # check if we are in git repo
    os.system("cp hooks/pre-commit .git/hooks/pre-commit")
    os.system("chmod +x .git/hooks/pre-commit")

app_data = "~/.retriever/scripts"
if os.path.exists(app_data):
    os.system("rm -r {}".format(app_data))

__version__ = 'v2.2.0'
with open(os.path.join("retriever", "_version.py"), "w") as version_file:
    version_file.write("__version__ = " + "'" + __version__ + "'\n")
    version_file.close()


def clean_version(v):
    return parse_version(v).__repr__().lstrip("<Version('").rstrip("')>")


includes = ['argcomplete',
            'future',
            'pandas',
            'psycopg2',
            'xlrd',
            'pymysql',
            'requests',
            'tqdm',
            'xlrd'] + extra_includes

excludes = [
    '.cache',
    'docker',
    'docs',
    'doctest',
    'hooks',
    'pdb',
    'pickle',
    'pyreadline',
    'scripts',
    'tests'
    'pywin', 'pywin.debugger',
    'pywin.debugger.dbgcon',
    'pywin.dialogs', 'pywin.dialogs.list',
    'Tkconstants', 'Tkinter', 'tcl', 'tk'
]

setup(name='retriever',
      version=clean_version(__version__),
      description='Data Retriever',
      long_description=('The Data Retriever is a package manager for data. '
                        'It downloads, cleans, and stores publicly available data, '
                        'so that analysts spend less time cleaning and managing data, '
                        'and more time analyzing it.'),
      author='Ben Morris, Shivam Negi, Akash Goel, Andrew Zhang, Henry Senyondo, Ethan White',
      author_email='ethan@weecology.org',
      url='https://github.com/weecology/retriever',
      classifiers=['Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3', ],
      packages=find_packages(
          exclude=excludes),
      entry_points={
          'console_scripts': [
              'retriever = retriever.__main__:main',
          ],
      },
      install_requires=includes,
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

    check_for_updates(False)
    compile()
except:
    pass
