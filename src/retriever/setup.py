"""Use the following command to install retriever: python setup.py install"""

from setuptools import setup
import platform
if "win" in platform.platform().lower():
    import py2exe
from __init__ import VERSION


packages = [
            'retriever.lib',
            'retriever.engines',
            'retriever.app',
            'retriever',
            ]
            
includes = [
            'xlrd',
            'pyodbc'
            ]
            
excludes = [
            '_ssl',
            'pyreadline',
            'difflib',
            'doctest',
            'optparse',
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

setup(name='retriever',
      version=VERSION,
      description='EcoData Retriever',
      author='Ben Morris',
      author_email='ben.morris@weecology.org',
      url='http://www.ecologicaldata.org/database-toolkits',
      packages=packages,
      package_dir={
                'retriever':''
                },
      entry_points={
        'console_scripts': [
            'retriever = retriever.main:main',
        ],
      },
      # py2exe options
      options = {'py2exe': {'bundle_files': 1,
                            'compressed': 2,
                            'optimize': 2,
                            'packages': packages,
                            'includes': includes,
                            'excludes': excludes,
                            }
                 },
      windows = [{'script': "main.py",
                  'dest_base': "retriever",
                  'icon_resources':[(1,'globe.ico')]
                  }],
      zipfile = None,
     )
