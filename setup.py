from setuptools import setup

setup(name='dbtk',
      version='1.0',
      description='Database Toolkit',
      author='Ben Morris',
      author_email='ben.morris@weecology.org',
      url='http://www.ecologicaldata.org/database-toolkits',
      packages={'':'', 'lib':'', 'scripts':''},
      entry_points = {
        'console_scripts': [
            'dbtk = dbtk:main',
        ],
      }
     )
