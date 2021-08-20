=======================
Using the Rdatasets API
=======================

This tutorial explains the usage of the Rdatasets API in Data Retriever. It includes both the
CLI (Command Line Interface) commands as well as the Python interface for the same.


Command Line Interface
======================

Listing the Rdatasets
---------------------

The ``retriever ls rdataset`` command displays the Rdatasets. 

$ ``retriever ls rdataset -h`` (gives listing options)

::

    usage: retriever ls rdataset [-h] [-p P [P ...]] all

    positional arguments:
        all           display all the packages present in rdatasets

    optional arguments:
        -h, --help    show this help message and exit
        -p P [P ...]  display a list of all rdatasets present in the package(s)

**Examples**

This example will display all the Rdatasets present with their package name, dataset name and script name

$ ``retriever ls rdataset``

::

    List of all available Rdatasets

    Package: aer              Dataset: affairs                   Script Name: rdataset-aer-affairs
    Package: aer              Dataset: argentinacpi              Script Name: rdataset-aer-argentinacpi
    Package: aer              Dataset: bankwages                 Script Name: rdataset-aer-bankwages
    ...
    Package: vcd              Dataset: vonbort                   Script Name: rdataset-vcd-vonbort
    Package: vcd              Dataset: weldondice                Script Name: rdataset-vcd-weldondice
    Package: vcd              Dataset: womenqueue                Script Name: rdataset-vcd-womenqueue


This example will display all the Rdatasets present in the packages ``vcd`` and ``aer``

$ ``retriever ls rdataset -p vcd aer``

::

    List of all available Rdatasets in packages: ['vcd', 'aer']
    Package: vcd              Dataset: arthritis                 Script Name: rdataset-vcd-arthritis
    Package: vcd              Dataset: baseball                  Script Name: rdataset-vcd-baseball
    Package: vcd              Dataset: brokenmarriage            Script Name: rdataset-vcd-brokenmarriage
    ...
    Package: aer              Dataset: affairs                   Script Name: rdataset-aer-affairs
    Package: aer              Dataset: argentinacpi              Script Name: rdataset-aer-argentinacpi
    Package: aer              Dataset: bankwages                 Script Name: rdataset-aer-bankwages
    ...


This example will display all the Rdatasets present in the package ``vcd``

$ ``retriever ls rdataset -p vcd``

::

    List of all available Rdatasets in packages: ['vcd', 'aer']
    Package: vcd              Dataset: arthritis                 Script Name: rdataset-vcd-arthritis
    Package: vcd              Dataset: baseball                  Script Name: rdataset-vcd-baseball
    Package: vcd              Dataset: brokenmarriage            Script Name: rdataset-vcd-brokenmarriage
    ...


This example will display all the packages present in rdatasets

$ ``retriever ls rdataset all``

::

    List of all the packages present in Rdatasets

    aer         cluster   dragracer  fpp2           gt        islr     mass        multgee         plyr      robustbase  stevedata  
    asaur       count     drc        gap            histdata  kmsurv   mediation   nycflights13    pscl      rpart       survival   
    boot        daag      ecdat      geepack        hlmdiag   lattice  mi          openintro       psych     sandwich    texmex     
    cardata     datasets  evir       ggplot2        hsaur     lme4     mosaicdata  palmerpenguins  quantreg  sem         tidyr      
    causaldata  dplyr     forecast   ggplot2movies  hwde      lmec     mstate      plm             reshape2  stat2data   vcd 


Downloading the Rdatasets
-------------------------

The ``retriever download rdataset-<package>-<dataset>`` command downloads the Rdataset ``dataset`` which exists in the package ``package``.
You can also copy the script name from the output of ``retriever ls rdataset``.

**Example**

This example downloads the ``rdataset-vcd-bundesliga`` dataset.

$ ``retriever download rdataset-vcd-bundesliga``

::

    => Installing rdataset-vcd-bundesliga
    Downloading Bundesliga.csv: 60.0B [00:00, 117B/s]                                                                                                 
    Done!

The downloaded raw data files are stored in the ``raw_data`` directory in the ``~/.retriever`` directory.


Installing the Rdatasets
------------------------

The ``retriever install <engine> rdataset-<package>-<dataset>`` command downloads the raw data, creates the script for it and then installs
the Rdataset ``dataset`` present in the package ``package`` into the provided ``engine``.

**Example**

This example install the ``rdataset-aer-usmoney`` dataset into the ``postgres`` engine.

$ ``retriever install postgres rdataset-aer-usmoney``

::

    => Installing rdataset-aer-usmoney
    Downloading USMoney.csv: 1.00B [00:00, 2.52B/s]
    Processing... USMoney.csv
    Successfully wrote scripts to /home/user/.retriever/rdataset-scripts/usmoney.csv.json
    Updating script name to rdataset-aer-usmoney.json
    Updating the contents of script rdataset-aer-usmoney
    Successfully updated rdataset_aer_usmoney.json
    Updated the script rdataset-aer-usmoney
    Creating database rdataset_aer_usmoney...

    Installing rdataset_aer_usmoney.usmoney
    Progress: 100%|█████████████████████████████████████████████████████████████████████████████████████████████| 136/136 [00:00<00:00, 2225.09rows/s]
    Done!

The script created for the Socrata dataset is stored in the ``rdataset-scripts`` directory in the ``~/.retriever`` directory.


Python Interface in Data Retriever
==================================

Updating Rdatasets Catalog
--------------------------

The function ``update_rdataset_catalog`` creates/updates the ``datasets_url.json`` in the ``~/.retriever/rdataset-scripts`` directory,
which contains the information about all the Rdatasets.

.. code-block:: python

  >>> import retriever as rt
  >>> rt.update_rdataset_catalog()

.. note::

  The ``update_rdataset_catalog`` function has a default argument ``test`` which is set to ``False``.
  If ``test`` is set to ``True``, then the contents of the ``datasets_url.json`` file would be returned as
  a dict. 

Listing Rdatasets
-----------------

The function ``display_all_rdataset_names`` prints the package, dataset name and the script name for the Rdatasets present in the package(s) requested.
If no package is specified, it prints all the rdatasets, and if ``all`` is passed as the function argument then all the package names are displayed.

.. note::

  The function argument ``package_name`` takes a list as an input when you want to display rdatasets based on the packages.
  If you want to display all packages names, set ``package_name`` argument to ``all`` (refer to the example below).


.. code-block:: python

  >>> import retriever as rt
  >>>
  >>> # Display all Rdatasets
  >>> rt.display_all_rdataset_names()
  List of all available Rdatasets

  Package: aer              Dataset: affairs                   Script Name: rdataset-aer-affairs
  Package: aer              Dataset: argentinacpi              Script Name: rdataset-aer-argentinacpi
  Package: aer              Dataset: bankwages                 Script Name: rdataset-aer-bankwages
  ...
  Package: vcd              Dataset: vonbort                   Script Name: rdataset-vcd-vonbort
  Package: vcd              Dataset: weldondice                Script Name: rdataset-vcd-weldondice
  Package: vcd              Dataset: womenqueue                Script Name: rdataset-vcd-womenqueue
  >>>
  >>> # Display all the Rdatasets present in packages 'aer' and 'drc'
  >>> rt.display_all_rdataset_names(['aer', 'drc'])
  List of all available Rdatasets in packages: ['aer', 'drc']
  Package: aer              Dataset: affairs                   Script Name: rdataset-aer-affairs
  Package: aer              Dataset: argentinacpi              Script Name: rdataset-aer-argentinacpi
  Package: aer              Dataset: bankwages                 Script Name: rdataset-aer-bankwages
  ...
  Package: drc              Dataset: spinach                   Script Name: rdataset-drc-spinach
  Package: drc              Dataset: terbuthylazin             Script Name: rdataset-drc-terbuthylazin
  Package: drc              Dataset: vinclozolin               Script Name: rdataset-drc-vinclozolin
  >>>
  >>> # Display all the packages in Rdatasets
  >>> rt.display_all_rdataset_names('all')
  List of all the packages present in Rdatasets

  aer         cluster   dragracer  fpp2           gt        islr     mass        multgee         plyr      robustbase  stevedata  
  asaur       count     drc        gap            histdata  kmsurv   mediation   nycflights13    pscl      rpart       survival   
  boot        daag      ecdat      geepack        hlmdiag   lattice  mi          openintro       psych     sandwich    texmex     
  cardata     datasets  evir       ggplot2        hsaur     lme4     mosaicdata  palmerpenguins  quantreg  sem         tidyr      
  causaldata  dplyr     forecast   ggplot2movies  hwde      lmec     mstate      plm             reshape2  stat2data   vcd 


Updating the Contents of Rdataset Script
----------------------------------------

The function ``update_socrata_contents`` updates the contents of the socrata script created by ``create_socrata_dataset``.

The input arguments are:
  - data_obj: The dict which contains the following keys: ``csv``, ``doc`` and ``title``. 
  - package: The R package in which the dataset exists
  - dataset_name: The dataset name
  - json_file: The content of the script created

The function returns ``True, json_file`` if the data_obj dict is correct,
otherwise, it returns ``False, None``.

.. code-block:: python

  >>> import json
  >>> import retriever as rt
  >>> from retriever.lib.defaults import RDATASET_SCRIPT_WRITE_PATH
  >>> data_obj = {
  ...     'csv': 'https://vincentarelbundock.github.io/Rdatasets/csv/drc/metals.csv',   # csv file url
  ...     'doc': 'https://vincentarelbundock.github.io/Rdatasets/doc/drc/metals.html',  # documentation url
  ...     'title': 'Data from heavy metal mixture experiments',
  ... }
  >>> script_path = RDATASET_SCRIPT_WRITE_PATH
  >>> script_filename = f"rdataset_{package}_{dataset_name}" + '.json'
  >>> with open(f"{script_path}/{script_filename}", "r") as f:
  ...       json_file = json.load(f)
  >>> f.close()
  >>> package = 'drc'
  >>> dataset_name = 'metals'
  >>> json_file = rt.update_rdataset_contents(data_obj, package, dataset_name, json_file)



Updating and Renaming the Rdataset Script
-----------------------------------------

The function ``update_rdataset_script(data_obj, dataset_name, package, script_path)`` renames the script, 
calls the ``update_rdataset_contents``, and then writes the new content returned by ``update_rdataset_contents``

.. code-block:: python

  >>> import retriever as rt
  >>> from retriever.lib.defaults import RDATASET_SCRIPT_WRITE_PATH
  >>> data_obj = {
  ...     'csv': 'https://vincentarelbundock.github.io/Rdatasets/csv/drc/metals.csv',
  ...     'doc': 'https://vincentarelbundock.github.io/Rdatasets/doc/drc/metals.html',
  ...     'title': 'Data from heavy metal mixture experiments',
  ... }
  >>> script_path = RDATASET_SCRIPT_WRITE_PATH
  >>> package = 'drc'
  >>> dataset_name = 'metals'
  >>> rt.update_rdataset_script(data_obj, dataset_name, package, script_path)


Creating a Rdataset Script
--------------------------

The function ``create_rdataset(engine, name, resource, script_path=None)`` creates rdataset scripts
for retriever. This function downloads the raw data, creates the script, then updates it and at last,
it installs the dataset according to the engine using that script.

.. note::

  If the engine is ``download`` then the function just downloads the raw data files.
  But if the engine is other than ``download`` (e.g. ``postgres``), then it creates the script
  and then installs the dataset into the engine provided.

.. code-block:: python

  >>> import retriever as rt
  >>> from retriever.engines import choose_engine
  >>> from retriever.lib.defaults import RDATASET_SCRIPT_WRITE_PATH
  >>> 
  >>> # engine = choose_engine({'command': 'install', 'engine': 'postgres'}) 
  >>> # Every engine other than 'download' would download data, then create the script
  >>> if the script does not exists, and then installs the dataset into the engine
  >>> # Or
  >>> engine = choose_engine({'command': 'download'})
  >>> # The 'download' engine will just download the raw data files
  >>> script_path = RDATASET_SCRIPT_WRITE_PATH
  >>> package = 'drc'
  >>> dataset_name = 'metals'
  >>> rt.create_rdataset(engine, package, dataset_name, script_path)
  Downloading metals.csv: 3.00B [00:00, 7.24B/s]                                                                                                    
  >>> 


Downloading a Rdataset
----------------------

.. code-block:: python

  >>> import retriever as rt
  >>> rt.download('rdataset-drc-earthworms')


Installing a Rdataset
---------------------

.. code-block:: python

  >>> import retriever as rt
  >>> rt.install_postgres('rdataset-mass-galaxies')

