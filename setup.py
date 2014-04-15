"""Use the following command to install retriever: python setup.py install"""

from setuptools import setup
import platform
import sys
p = platform.platform().lower()
extra_includes = []
if "darwin" in p:
    try: import py2app
    except ImportError: pass
    extra_includes = []
elif "win" in p:
    try: import py2exe
    except ImportError: pass
    import sys
    extra_includes = ['pyodbc', 'inspect']
    sys.path.append("C:\\Windows\\winsxs\\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91")
from __init__ import VERSION

def is_importable(module):
    """Returns True if 'module' is installed"""
    try:
        return __import__(module)
    except ImportError:
        return None


def is_wxpython_installed():
    """Returns True if  wxpython is installed"""
    if is_importable('wx'):
        return True
    return False

def continue_installation(question):
    while True:
        print question, "(y/n)"
        response = raw_input().lower()
        if response[0] in ['y', 'n']:
            break
        print ('Please answer y/n')

    return response[0] == 'y'

def clean_version(v):
    if v == 'master':
        return '1.0.0'
    return v.replace('v', '').replace('.rc', '').replace('.beta', '')

packages = [
            'retriever.lib',
            'retriever.engines',
            'retriever.app',
            'retriever',
            ]

includes = [
            'xlrd',
            'wx',
            'pymysql',
            'psycopg2',
            'sqlite3',
            ] + extra_includes

excludes = [
            'pyreadline',
            'doctest',
            'optparse',
            'getopt',
            'pickle',
            'calendar',
            'pdb',
            'inspect',
            'email',
            'pywin', 'pywin.debugger',
            'pywin.debugger.dbgcon',
            'pywin.dialogs', 'pywin.dialogs.list',
            'Tkconstants', 'Tkinter', 'tcl',
            ]


wx_installed = is_wxpython_installed()

if wx_installed is False:
    should_continue = continue_installation('wxpython is not installed. Continue?')

if should_continue is False:
    sys.exit(1)

setup(name='retriever',
      version=clean_version(VERSION),
      description='EcoData Retriever',
      author='Ben Morris',
      author_email='ben.morris@weecology.org',
      url='http://www.ecodataretriever.org',
      packages=packages,
      package_dir={
                'retriever':''
                },
      entry_points={
        'console_scripts': [
            'retriever = retriever.__main__:main',
        ],
      },
      install_requires=[
                        'xlrd',
                        ],

      # py2exe flags
      console = [{'script': "__main__.py",
                  'dest_base': "retriever",
                  'icon_resources':[(1,'icon.ico')]
                  }],
      zipfile = None,

      # py2app flags
      app=['__main__.py'],
      data_files=[('', ['CITATION'])],
      setup_requires=['py2app'] if 'darwin' in p else [],

      # options
      # optimize is set to 1 of py2app to avoid errors with pymysql
      # bundle_files = 1 or 2 was causing failed builds so we moved
      # to bundle_files = 3 and Inno Setup
      options = {'py2exe': {'bundle_files': 3,
                            'compressed': 2,
                            'optimize': 1,
                            'packages': packages,
                            'includes': includes,
                            'excludes': excludes,
                            },
                 'py2app': {'packages': ['retriever'],
                            'includes': includes,
                            'site_packages': True,
                            'resources': [],
                            'optimize': 1,
                            'argv_emulation': True,
                            'no_chdir': True,
                            },
                },
      )


try:
    from compile import compile
    compile()
except:
    pass
