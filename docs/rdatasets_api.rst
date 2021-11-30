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

The script created for the Rdataset is stored in the ``rdataset-scripts`` directory in the ``~/.retriever`` directory.


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

.. note::

  For downloading or installing the Rdatasets, the script name should follow the syntax given below.
  The script name should be ``rdataset-<package name>-<dataset name>``. The ``package name`` and ``dataset name``
  should be valid.

  Example:
    - Correct: ``rdataset-drc-earthworms``

    - Incorrect:  ``rdataset-drcearthworms``, ``rdatasetdrcearthworms``