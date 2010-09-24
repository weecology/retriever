"""Use the following command to install dbtk: python setup.py install"""

from setuptools import setup
import py2exe

setup(name='dbtk',
      version='1.0',
      description='Database Toolkit',
      author='Ben Morris',
      author_email='ben.morris@weecology.org',
      url='http://www.ecologicaldata.org/database-toolkits',
      packages=[
                'dbtk',
                'dbtk.lib',
                'dbtk.scripts'
                ],
      package_dir={
                'dbtk':''
                },
      entry_points={
        'console_scripts': [
            'dbtk = dbtk.main:main',
        ],
      },
      # py2exe options
      options = {'py2exe': {'bundle_files': 1,
                            'packages': ['dbtk',
                                         'dbtk.lib',
                                         'dbtk.scripts',
                                         ],
                            }
                 },
      windows = [{'script': "main.py"}],
      zipfile = None,
     )
