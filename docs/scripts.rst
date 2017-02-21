==========================================
Creating scripts for the Data Retriever
==========================================


Script Creation
---------------


The Data Retriever uses a simple CLI for developing new dataset scripts. This allows users with no programming experience to quickly add most standard datasets to the Retriever by specifying the names and locations of the tables along with additional information about the configuration of the data.
The script is saved as a JSON file, that follows the DataPackage_ standards.

.. _DataPackage: http://specs.frictionlessdata.io/data-packages/


To create a new script, try ``retriever new_json``, which starts the CLI tool for new script creation.

``Required``

#. **name:** A one word name for the dataset

``Strongly recommended``

#. **title:** Give the name of the dataset
#. **description:** A brief description of the dataset of ~25 words.
#. **citation:** Give a citation if available
#. **homepage:** A reference to the data or the home page
#. **keywords:** Helps in classifying the type of data (i.e using Taxon, Data Type, Spatial Scale, etc.)


``Mandatory for any table added; Add Table? (y/N)``

#. **table-name:** Name of the table, URL to the table
#. **table-url:** Name of the table, URL to the table

.. - TODO: Add license and comments option

Basic Scripts
-------------

The most basic scripts structure requires only some general metadata about the
dataset,i.e., the shortname of the database and table, and the location of the
table.

**Example of a basic script, example.script**

``Creating script from the CLI``

::

  name (a short unique identifier; only lowercase letters and - allowed): example-mammal
  title: Mammal Life History Database - Ernest, et al., 2003
  description:
  citation: S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.
  homepage (for the entire dataset):
  keywords (separated by ';'): mammals ; compilation

  Add Table? (y/N): y
  table-name: species
  table-url: http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt
  missingValues (separated by ';'):
  replace_columns (separated by ';'):
  delimiter:
  do_not_bulk_insert (bool = True/False):
  contains_pk (bool = True/False):
  escape_single_quotes (bool = True/False):
  escape_double_quotes (bool = True/False):
  fixed_width (bool = True/False):
  header_rows (int):
  Enter columns [format = name, type, (optional) size]:


  Add crosstab columns? (y,N): n

  Add Table? (y/N): n

``Created script``

::

  {
      "citation": "S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.",
      "description": "",
      "homepage": "",
      "keywords": [
          "Mammals",
          "Compilation"
      ],
      "name": "exMammal",
      "resources": [
          {
              "dialect": {},
              "name": "species",
              "schema": {
                  "fields": []
              },
              "url": "http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"
          }
      ],
      "retriever": "True",
      "retriever_minimum_version": "2.0.dev",
      "title": "Mammal Life History Database - Ernest, et al., 2003"
      "urls": {
          "species": "www.exampleurl.com"
      },
      "version": "1.0.0"
  }

Explanation for the keys:

- ``citation``: Citation for the dataset
- ``description``: Description for the dataset
- ``homepage``: Homepage or website where the data is hosted
- ``keywords``: Keywords/tags for the dataset (for searching and classification)
- ``name``: Shortname for the dataset. Unique, URL-identifiable
- ``resources``: List of tables within the dataset

  - ``dialect``: Metadata for retriever to process the table
  - ``name``: Name of the table
  - ``schema``: List of the columns in the table

    - ``fields``: (Optional) List of columns and their types and (optional) size values
    - ``ct_column``: (Optional) Cross-tab column with column names from dataset

  - ``url``: URL of the table

- ``retriever``: Auto generated tag for script identification
- ``retriever_minimum_version``: Minimum version that supports this script
- ``title``: Title/Name of the dataset
- ``urls``: dictionary of table names and the respective urls
- ``version``: "1.0.0"

Multiple Tables
---------------

A good example of data with multiple tables is Ecological Archives E091-124-D1, `McGlinn et al. 2010`_. ``plant-comp-ok`` Vascular plant composition data.
Since there are several csv files, we create a table for each of the files.

Assuming we want to call our dataset McGlinn2010, below is an example of the script that will handle this data

.. _`McGlinn et al. 2010`: http://esapubs.org/archive/ecol/E091/124/

::

  ...
    "name": "McGlinn2010",
    "resources": [
        {
            "dialect": {},
            "name": "pres",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E091/124/TGPP_pres.csv"
        },
        {
            "dialect": {},
            "name": "cover",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E091/124/TGPP_cover.csv"
        },
        {
            "dialect": {},
            "name": "richness",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E091/124/TGPP_rich.csv"
        },
        {
            "dialect": {},
            "name": "species",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv"
        },
        {
            "dialect": {},
            "name": "environment",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E091/124/TGPP_env.csv"
        },
        {
            "dialect": {},
            "name": "climate",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E091/124/TGPP_clim.csv"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "2.0.dev",
    "title": "Vascular plant composition - McGlinn, et al., 2010",
    "urls": {
        "climate": "http://esapubs.org/archive/ecol/E091/124/TGPP_clim.csv",
        "cover": "http://esapubs.org/archive/ecol/E091/124/TGPP_cover.csv",
        "environment": "http://esapubs.org/archive/ecol/E091/124/TGPP_env.csv",
        "pres": "http://esapubs.org/archive/ecol/E091/124/TGPP_pres.csv",
        "richness": "http://esapubs.org/archive/ecol/E091/124/TGPP_rich.csv",
        "species": "http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv"
    }
    ...

Null Values
-----------

The Retriever can replace non-standard null values by providing a semi-colon separated list of those null values
after the table in which the null values occur.

::

  ...
  Table name: species
  Table URL: http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt
  nulls (separated by ';'): -999 ; 'NA'
  ...

For example, the `Adler et al. 2010`_. ``mapped-plant-quads-ks`` script uses -9999 to indicate null values.

.. _`Adler et al. 2010`: http://esapubs.org/archive/ecol/E088/161/

::

  ...
        {
            "dialect": {},
            "name": "quadrat_info",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E088/161/quadrat_info.csv"
        },
        {
            "dialect": {
                "missingValues": [
                    "NA"
                ]
            },
  ...


Headers
-------

If the first row of a table is the headers then naming the columns will, be default, be handled automatically.
If you want to rename an existing header row for some reason, e.g.,
it includes reserved keywords for a database management system,
you can do so by adding a list of semi-colon separated column names,
with the new columns provided after a comma for each such column.

::

  ...
  Add Table? (y/N): y
  Table name: species
  Table URL: http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv
  replace_columns (separated by ';', with comma-separated values): jan, january ; feb, february ; mar, march
  ...


The ``mapped-plant-quads-ks`` script for the `Adler et al. 2007`_. dataset from Ecological Archives
includes this functionality:


.. _`Adler et al. 2007`: http://esapubs.org/archive/ecol/E088/161/

::

  ...
   "name": "mapped-plant-quads-ks",
    "resources": [
        {
            "dialect": {},
            "name": "main",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E088/161/allrecords.csv"
        },
        {
            "dialect": {},
            "name": "quadrat_info",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E088/161/quadrat_info.csv"
        },
        {
            "dialect": {
                "missingValues": [
                    "NA"
                ]
            },
            "name": "quadrat_inventory",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E088/161/quadrat_inventory.csv"
        },
        {
            "dialect": {},
            "name": "species",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E088/161/species_list.csv"
        },
        {
            "dialect": {
                "missingValues": [
                    "NA"
                ],
                "replace_columns": [
                    [
                        "jan",
                        "january"
                    ],
                    [
                        "feb",
                        "february"
                    ],
                    [
                        "mar",
                        "march"
                    ],
                    [
                        "apr",
                        "april"
                    ],
                    [
                        "jun",
                        "june"
                    ],
                    [
                        "jul",
                        "july"
                    ],
                    [
                        "aug",
                        "august"
                    ],
                    [
                        "sep",
                        "september"
                    ],
                    [
                        "oct",
                        "october"
                    ],
                    [
                        "nov",
                        "november"
                    ],
                    [
                        "dec",
                        "december"
                    ]
                ]
            },
            "name": "monthly_temp",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E088/161/monthly_temp.csv"
        },
    ...


Full control over column names and data types
---------------------------------------------

By default the Retriever automatically detects both column names and data types, but you can also exercise complete
control over the structure of the resulting database by adding column names and types.
These values are stored in the ``fields`` array of the ``schema`` dict of the JSON script.

::

  ...
  Enter columns [format = name, type, (optional) size]:

  count, int
  name, char, 40
  year, int
  ...

The Smith et al. Masses of Mammals ``mammal-masses`` dataset script includes this type of functionality.

::

  ...
     "name": "mammal-masses",
    "resources": [
        {
            "dialect": {
                "missingValues": [
                    -999
                ],
                "header_rows": 0
            },
            "name": "MammalMasses",
            "schema": {
                "fields": [
                    {
                        "name": "record_id",
                        "type": "pk-auto"
                    },
                    {
                        "name": "continent",
                        "size": "20",
                        "type": "char"
                    },
                    {
                        "name": "status",
                        "size": "20",
                        "type": "char"
                    },
                    {
                        "name": "sporder",
                        "size": "20",
                        "type": "char"
                    },
                    {
                        "name": "family",
                        "size": "20",
                        "type": "char"
                    },
                    {
                        "name": "genus",
                        "size": "20",
                        "type": "char"
                    },
                    {
                        "name": "species",
                        "size": "20",
                        "type": "char"
                    },
                    {
                        "name": "log_mass_g",
                        "type": "double"
                    },
                    {
                        "name": "comb_mass_g",
                        "type": "double"
                    },
                    {
                        "name": "reference",
                        "type": "char"
                    }
                ]
            },
            "url": "http://www.esapubs.org/Archive/ecol/E084/094/MOMv3.3.txt"
        }
    ],
    "retriever": "True",
    "retriever_minimum_version": "2.0.dev",
    "title": "Masses of Mammals (Smith et al. 2003)",
  ...

Restructuring cross-tab data
----------------------------

It is common in ecology to see data where the rows indicate one level of grouping (e.g., by site),
the columns indicate another level of grouping (e.g., by species), and the values in each cell indicate
the value for the group indicated by the row and column (e.g., the abundance of species x at site y).
This is referred as cross-tab data and cannot be easily handled by database management systems,
which are based on a one record per line structure. The Retriever can restructure this type of
data into the appropriate form.
In scripts this involves telling the retriever the name of the column to store the data in
and the names of the columns to be restructured.

::

  ...
  Add crosstab columns? (y,N): y
  Crosstab column name: <name of column to store cross-tab data>
  Enter names of crosstab column values (Press return after each name):

  ct column 1
  ct column 2
  ct column 3
  ...

The `Moral et al 2010 script`_. ``mt-st-helens-veg`` takes advantage of this functionality.

.. _`Moral et al 2010 script`: http://esapubs.org/archive/ecol/E091/152/

::

  ...
  "name": "mt-st-helens-veg",
    "resources": [
        {
            "dialect": {
                "delimiter": ","
            },
            "name": "species_plot_year",
            "schema": {
                "ct_column": "species",
                "ct_names": [
                    "Abilas",
                    "Abipro",
                    "Achmil",
                    "Achocc",
                    "Agoaur",
                    "Agrexa",
                    "Agrpal",
                    "Agrsca",
                    "Alnvir",
                    "Anamar",
                    "Antmic",
                    "Antros",
                    "Aqifor",
                    "Arcnev",
                    "Arnlat",
                    "Astled",
                    "Athdis",
                    "Blespi",
                    "Brocar",
                    "Brosit",
                    "Carmer",
                    "Carmic",
                    "Carpac",
                    "Carpay",
                    "Carpha",
                    "Carros",
                    "Carspe",
                    "Casmin",
                    "Chaang",
                    "Cirarv",
                    "Cisumb",
                    "Crycas",
                    "Danint",
                    "Descae",
                    "Elyely",
                    "Epiana",
                    "Eriova",
                    "Eripyr",
                    "Fesocc",
                    "Fravir",
                    "Gencal",
                    "Hiealb",
                    "Hiegra",
                    "Hyprad",
                    "Junmer",
                    "Junpar",
                    "Juncom",
                    "Leppun",
                    "Lommar",
                    "Luepec",
                    "Luihyp",
                    "Luplat",
                    "Luplep",
                    "Luzpar",
                    "Maiste",
                    "Pencar",
                    "Pencon",
                    "Penser",
                    "Phahas",
                    "Phlalp",
                    "Phldif",
                    "Phyemp",
                    "Pincon",
                    "Poasec",
                    "Poldav",
                    "Polmin",
                    "Pollon",
                    "Poljun",
                    "Popbal",
                    "Potarg",
                    "Psemen",
                    "Raccan",
                    "Rumace",
                    "Salsit",
                    "Saxfer",
                    "Senspp",
                    "Sibpro",
                    "Sorsit",
                    "Spiden",
                    "Trispi",
                    "Tsumer",
                    "Vacmem",
                    "Vervir",
                    "Vioadu",
                    "Xerten"
                ],
                "fields": [
                    {
                        "name": "record_id",
                        "type": "pk-auto"
                    },
                    {
                        "name": "plot_id_year",
                        "size": "20",
                        "type": "char"
                    },
                    {
                        "name": "plot_name",
                        "size": "4",
                        "type": "char"
                    },
                    {
                        "name": "plot_number",
                        "type": "int"
                    },
                    {
                        "name": "year",
                        "type": "int"
                    },
                    {
                        "name": "count",
                        "type": "ct-double"
                    }
                ]
            },
            "url": "http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_PLOT_YEAR.csv"
        },
  ...



Script Editing
--------------
**Note:** Any time a script gets updated, the minor version number must be incremented from within the script. 

The JSON scripts created using the retriever CLI can also be edited using the CLI.

To edit a script, use the ``retriever edit_json`` command, followed by the script's shortname;

For example, editing the ``mammal-life-hist`` (Mammal Life History Database - Ernest, et al., 2003)
dataset, the editing tool will ask a series a questions for each of the keys and values of the script,
and act according to the input.


The tool describes the values you want to edit.
In the script below the first keyword is citation, ``citation ( <class 'str'> )``
and it is of class string or expects a string.

::

  dev@retriever:~$ retriever edit_json mammal-life-hist

    ->citation ( <class 'str'> ) :

    S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402

    Select one of the following for the key 'citation'

    1. Modify value
    2. Remove from script
    3. Continue (no changes)


    Your choice: 3

      ->homepage ( <class 'str'> ) :

      http://esapubs.org/archive/ecol/E084/093/


    Select one of the following for the key 'homepage':

    1. Modify value
    2. Remove from script
    3. Continue (no changes)


    Your choice: 3

      ->description ( <class 'str'> ) :

      The purpose of this data set was to compile general life history characteristics for a variety of mammalian
      species to perform comparative life history analyses among different taxa and different body size groups.


    Select one of the following for the key 'description':

    1. Modify value
    2. Remove from script
    3. Continue (no changes)


    Your choice: 3

      ->retriever_minimum_version ( <class 'str'> ) :

      2.0.dev


    Select one of the following for the key 'retriever_minimum_version':

    1. Modify value
    2. Remove from script
    3. Continue (no changes)


    Your choice: 3

      ->version ( <class 'str'> ) :

      1.1.0


    Select one of the following for the key 'version':

    1. Modify value
    2. Remove from script
    3. Continue (no changes)


    Your choice: 3

      ->resources ( <class 'list'> ) :

      {'dialect': {}, 'schema': {}, 'name': 'species', 'url': 'http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt'}


    1 .  {'dialect': {}, 'schema': {}, 'name': 'species', 'url': 'http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt'}

    Edit this dict in 'resources'? (y/N): n
    Select one of the following for the key 'resources':

    1. Add an item
    2. Delete an item
    3. Remove from script
    4. Continue (no changes)
    ...
