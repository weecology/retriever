=====================
Using the Socrata API
=====================

This tutorial explains the usage of the Socrata API in Data Retriever. It includes both the
CLI (Command Line Interface) commands as well as the Python interface for the same.

.. note::
  Currently Data Retriever only supports tabular Socrata datasets (tabular Socrata datasets which are of type map are not supported).


Command Line Interface
======================

Listing the Socrata Datasets
----------------------------

The ``retriever ls -s`` command displays the Socrata datasets which contain the provided keywords in their title.

$ ``retriever ls -h`` (gives listing options)

::

    usage: retriever ls [-h] [-l L [L ...]] [-k K [K ...]] [-v V [V ...]]
                    [-s S [S ...]]

    optional arguments:
      -h, --help    show this help message and exit
      -l L [L ...]  search datasets with specific license(s)
      -k K [K ...]  search datasets with keyword(s)
      -v V [V ...]  verbose list of specified dataset(s)
      -s S [S ...]  search socrata datasets with name(s)

**Example**

This example will list the names of the socrata datasets which contain the word ``fishing``.

$ ``retriever ls -s fishing``

::

    Autocomplete suggestions : Total 34 results

    [?] Select the dataset name: Recommended Fishing Rivers And Streams
     > Recommended Fishing Rivers And Streams
       Recommended Fishing Rivers And Streams API
       Iowa Fishing Report
       Recommended Fishing Rivers, Streams, Lakes and Ponds Map
       Public Fishing Rights Parking Areas Map
       Fishing Atlas
       Cook County - Fishing Lakes
       [ARCHIVED] Fishing License Sellers
       Public Fishing Rights Parking Areas
       Recommended Fishing Lakes and Ponds Map
       Recommended Fishing Lakes and Ponds
       Delaware Fishing Licenses and Trout Stamps
       Cook County - Fishing Lakes - KML

Here the user is prompted to select a dataset name. After selecting a dataset, the command returns some information related to the dataset selected.

Let's select the ``Public Fishing Rights Parking Areas`` dataset, after pressing Enter, the command returns
some information regarding the dataset selected.

::

    Autocomplete suggestions : Total 34 results

    [?] Select the dataset name: Public Fishing Rights Parking Areas
       Iowa Fishing Report
       Recommended Fishing Rivers, Streams, Lakes and Ponds Map
       Fishing Atlas
       Public Fishing Rights Parking Areas Map
       [ARCHIVED] Fishing License Sellers
       Cook County - Fishing Lakes
     > Public Fishing Rights Parking Areas
       Recommended Fishing Lakes and Ponds Map
       Recommended Fishing Lakes and Ponds
       Delaware Fishing Licenses and Trout Stamps
       Cook County - Fishing Lakes - KML
       General Fishing and Salmon Licence Sales
       Hunting and Fishing License Sellers

    Dataset Information of Public Fishing Rights Parking Areas: Total 1 results

    1. Public Fishing Rights Parking Areas
      ID : 9vef-6whi
      Type : {'dataset': 'tabular'}
      Description : The New York State Department of Environmental Con...
      Domain : data.ny.gov
      Link : https://data.ny.gov/Recreation/Public-Fishing-Rights-Parking-Areas/9vef-6whi


Downloading the Socrata Datasets
--------------------------------

The ``retriever download socrata-<socrata id>`` command downloads the Socrata dataset which matches the provided ``socrata id``.

**Example**

From the example in ``Listing the Socrata Datasets`` section, we selected the *Public Fishing Rights Parking Areas* dataset.
Since the dataset is of type ``tabular``, we can download it. The information received in the previous example contains the ``socrata id``.
We use this ``socrata id`` to download the dataset.

$ ``retriever download socrata-9vef-6whi``

::

    => Installing socrata-9vef-6whi
    Downloading 9vef-6whi.csv: 10.0B [00:03, 2.90B/s]
    Done!

The downloaded raw data files are stored in the ``raw_data`` directory in the ``~/.retriever`` directory.


Installing the Socrata Datasets
-------------------------------

The ``retriever install <engine> socrata-<socrata id>`` command downloads the raw data, creates the script for it and then installs
the Socrata dataset which matches the provided ``socrata id`` into the provided ``engine``.

**Example**

From the example in ``Listing the Socrata Datasets`` section, we selected the *Public Fishing Rights Parking Areas* dataset.
Since the dataset is of type ``tabular``, we can install it. The information received in that section contains the ``socrata id``.
We use this ``socrata id`` to install the dataset.

$ ``retriever install postgres socrata-9vef-6whi``

::

    => Installing socrata-9vef-6whi
    Downloading 9vef-6whi.csv: 10.0B [00:03, 2.69B/s]
    Processing... 9vef-6whi.csv
    Successfully wrote scripts to /home/user/.retriever/socrata-scripts/9vef_6whi.csv.json
    Updating script name to socrata-9vef-6whi.json
    Updating the contents of script socrata-9vef-6whi
    Successfully updated socrata_9vef_6whi.json
    Creating database socrata_9vef_6whi...

    Bulk insert on ..  socrata_9vef_6whi.socrata_9vef_6whi
    Done!

The script created for the Socrata dataset is stored in the ``socrata-scripts`` directory in the ``~/.retriever`` directory.


Python Interface in Data Retriever
==================================

Searching Socrata Datasets
--------------------------

The function ``socrata_autocomplete_search`` takes a list of strings as input and returns a list of strings which are the autocompleted names.

.. code-block:: python

  >>> import retriever as rt
  >>> names = rt.socrata_autocomplete_search(['clinic', '2015', '2016'])
  >>> for name in names:
  ...     print(name)
  ...
  2016 & 2015 Clinic Quality Comparisons for Clinics with Five or More Service Providers
  2015 - 2016 Clinical Quality Comparison (>=5 Providers) by Geography
  2016 & 2015 Clinic Quality Comparisons for Clinics with Fewer than Five Service Providers


Socrata Dataset Info by Dataset Name
------------------------------------

The input argument for the function ``socrata_dataset_info`` should be a string (valid dataset name returned by ``socrata_autocomplete_search``).
It returns a list of dicts, because there are multiple datasets on socrata with same name (e.g. ``Building Permits``).

.. code-block:: python

  >>> import retriever as rt
  >>> resource = rt.socrata_dataset_info('2016 & 2015 Clinic Quality Comparisons for Clinics with Five or More Service Providers')
  >>> from pprint import pprint
  >>> pprint(resource)
  [{'description': 'This data set includes comparative information for clinics '
                   'with five or more physicians for medical claims in 2015 - '
                   '2016. \r\n'
                   '\r\n'
                   'This data set was calculated by the Utah Department of '
                   'Health, Office of Healthcare Statistics (OHCS) using Utah’s '
                   'All Payer Claims Database (APCD).',
    'domain': 'opendata.utah.gov',
    'id': '35s3-nmpm',
    'link': 'https://opendata.utah.gov/Health/2016-2015-Clinic-Quality-Comparisons-for-Clinics-w/35s3-nmpm',
    'name': '2016 & 2015 Clinic Quality Comparisons for Clinics with Five or '
            'More Service Providers',
    'type': {'dataset': 'tabular'}}]


Finding Socrata Dataset by Socrata ID
-------------------------------------

The input argument of the function ``find_socrata_dataset_by_id`` should be the four-by-four socrata dataset identifier (e.g. ``35s3-nmpm``).
The function returns a dict which contains metadata about the dataset.

.. code-block:: python

  >>> import retriever as rt
  >>> from pprint import pprint
  >>> resource = rt.find_socrata_dataset_by_id('35s3-nmpm')
  >>> pprint(resource)
  {'datatype': 'tabular',
   'description': 'This data set includes comparative information for clinics '
                  'with five or more physicians for medical claims in 2015 - '
                  '2016. \r\n'
                  '\r\n'
                  'This data set was calculated by the Utah Department of '
                  'Health, Office of Healthcare Statistics (OHCS) using Utah’s '
                  'All Payer Claims Database (APCD).',
   'domain': 'opendata.utah.gov',
   'homepage': 'https://opendata.utah.gov/Health/2016-2015-Clinic-Quality-Comparisons-for-Clinics-w/35s3-nmpm',
   'id': '35s3-nmpm',
   'keywords': ['socrata'],
   'name': '2016 & 2015 Clinic Quality Comparisons for Clinics with Five or More '
           'Service Providers'}


Updating the Contents of Socrata Dataset Script
-----------------------------------------------

The function ``update_socrata_contents`` updates the contents of the socrata script created by ``create_socrata_dataset``.

The input arguments are:
  - json_file = The content of the script created
  - script_name =  The name of the script
  - url = The url through which the dataset is downloaded
  - resource = The object returned by the ``find_socrata_dataset_by_id``

The function returns ``True, json_file`` if the resource dict is correct,
otherwise, it returns ``False, None``.

.. code-block:: python

  import retriever as rt
  import json
  from retriever.lib.defaults import SOCRATA_SCRIPT_WRITE_PATH

  resource = rt.find_socrata_dataset_by_id('35s3-nmpm')
  filename = resource["id"] + '.csv'
  url = 'https://' + resource["domain"] + '/resource/' + filename
  script_name = 'socrata-35s3-nmpm'
  script_path = SOCRATA_SCRIPT_WRITE_PATH
  script_filename = script_name.replace("-","_") + ".json"
  with open(f"{script_path}/{script_filename}", "r") as f:
         json_file = json.load(f)
  f.close()
  result, json_file = rt.update_socrata_contents(json_file, script_name, url, resource)


Updating and Renaming the Socrata Dataset Script
------------------------------------------------

The function ``update_socrata_script(script_name, filename, url, resource, script_path)`` renames the script, 
calls the ``update_socrata_contents``, and then writes the new content returned by ``update_socrata_contents``

.. code-block:: python

  import retriever as rt
  from retriever.lib.defaults import SOCRATA_SCRIPT_WRITE_PATH

  script_path = SOCRATA_SCRIPT_WRITE_PATH
  resource = rt.find_socrata_dataset_by_id('35s3-nmpm')
  filename = resource["id"] + '.csv'
  url = 'https://' + resource["domain"] + '/resource/' + filename
  script_name = 'socrata-35s3-nmpm'
  rt.update_socrata_script(script_name, filename, url, resource, script_path)


Creating a Socrata Dataset Script
---------------------------------

The function ``create_socrata_dataset(engine, name, resource, script_path=None)``
creates socrata dataset scripts for retriever. This function downloads the raw data, creates the script,
then updates it and at last, it installs the dataset according to the engine using that script.

.. note::

  If the engine is ``download`` then the function just downloads the raw data files.
  But if the engine is other than ``download`` (e.g. ``postgres``), then it creates the script
  and then installs the dataset into the engine provided.

.. code-block:: python

  import retriever as rt
  from retriever.engines import choose_engine
  from retriever.lib.defaults import SOCRATA_SCRIPT_WRITE_PATH

  # engine = choose_engine({'command':'install', 'engine':'postgres'})
  # OR
  engine = choose_engine({'command': 'download'})
  script_path = SOCRATA_SCRIPT_WRITE_PATH
  resource = rt.find_socrata_dataset_by_id('35s3-nmpm')
  name = 'socrata-35s3-nmpm'
  rt.create_socrata_dataset(engine, name, resource, script_path)


Downloading a Socrata Dataset
-----------------------------

.. code-block:: python

  import retriever as rt
  rt.download('socrata-35s3-nmpm')


Installing a Socrata Dataset
----------------------------

.. code-block:: python

  import retriever as rt
  rt.install_postgres('socrata-35s3-nmpm')


.. note::

  For downloading or installing the Socrata Datasets, the dataset should follow the syntax given.
  The dataset name should be ``socrata-<socrata id>``. The ``socrata id`` should be the four-by-four
  socrata dataset identifier (e.g. ``35s3-nmpm``).

  Example:
    - Correct: ``socrata-35s3-nmpm``

    - Incorrect:  ``socrata35s3-nmpm``, ``socrata35s3nmpm``
