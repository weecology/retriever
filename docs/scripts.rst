=====================================================
Creating scripts for the EcoData Retriever
=====================================================


Script Creation
---------------


The EcoData Retriever uses a simple CLI for developing new dataset scripts. This allows users with no programming experience to quickly add most standard datasets to the Retriever by specifying the names and locations of the tables along with additional information about the configuration of the data.
To create a new script, try ``retriever new_json``, which starts the CLI tool for new script creation.

``Required``

#. **Shortname:** A one word name for the dataset

``Strongly recommended``

#. **Name/Title:** Give the name of the dataset
#. **Description:** A brief description of the dataset of ~25 words.
#. **Citation:** Give a citation if available
#. **Homepage:** A reference to the data or the home page
#. **Tags:** Helps in classifying the type of data (i.e using Taxon, Data Type, Spatial Scale, etc.)

``optional``

#. **Table Name:** Name of the table, URL to the table
#. **Table URL:** Name of the table, URL to the table

.. - TODO: Add license and comments option

Basic Scripts
-------------

The most basic scripts structure requires only some general metadata about the dataset,i.e., the shortname of the database and table, and the location of the table as below.

::

  Shortname:
  Table Name:
  Table URL:

Example of a basic script, example.script
-----------------------------------------


``Creating script from the CLI``
::

  Shortname (Give a unique identifier for script): exMammal
  Title/Name: Mammal Life History Database - Ernest, et al., 2003
  Description:
  Citation: S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.
  Site/Homepage of dataset:
  Tags (separated by ';'): Mammals ; Compilation

  Add Table? (y/N): y
  Table name: species
  Table URL: http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt
  nulls (separated by ';'):
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
      "title": "Mammal Life History Database - Ernest, et al., 2003"
  }

Explanation for the keys:

- ``citation``: Citation for the dataset
- ``description``: Description for the dataset
- ``homepage``: Homepage or website where the data is hosted
- ``keywords``: Keywords/tags to search the among scripts and classify
- ``name``: Shortname for the dataset. Unique, URL-identifiable
- ``resources``: List of tables within the dataset

  - ``dialect``: Metadata for retriever to process the table
  - ``name``: Name of the table
  - ``schema``: List of the columns in the table

    - ``fields``: (Optional) List of columns and their types and (optional) size values
    - ``ct_column``: (Optional) Cross-tab column with column names from dataset

  - ``url``: URL of the table

- ``title``: Title/Name of the dataset

Multiple Tables
---------------

A good example of data with multiple tables is Ecological Archives E091-124-D1, `McGlinn et al. 2010`_. Vascular plant composition data.
Since there are several csv files, we create a table for each of the files.

Assuming we want to call our database McGlinn2010, below is an example of the script that will handle this data

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

The Retriever can replace non-standard null values by providing a semi-colon separated list of those null values after the table in which the null values occur.

::

  ...
  Table name: species
  Table URL: http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt
  nulls (separated by ';'): -999 ; 'NA'
  ...

For example, the `Capellini et al. 2010`_. script uses -9999 to indicate null values.

.. _`Capellini et al. 2010`: http://esapubs.org/archive/ecol/E088/161/

::

  ...
  "name": "MammalMR2010",
  "resources": [
      {
          "dialect": {
              "nulls": [
                  -9999
              ]
          },
  ...


Headers
-------

If the first row of a table is the headers then naming the columns will, be default, be handled automatically.
If you want to rename an existing header row for some reason, e.g., it includes reserved keywords for a database management system, you can do so by adding a list of semi-colon separated column names, with the new columns provided after a comma for each such column.

::

  ...
  Add Table? (y/N): y
  Table name: species
  Table URL: http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv
  replace_columns (separated by ';', with comma-separated values): jan, january ; feb, february ; mar, march
  ...


The script for the `Adler et al. 2007`_. dataset from Ecological Archives includes this functionality:


.. _`Adler et al. 2007`: http://esapubs.org/archive/ecol/E088/161/

::

  ...
  "name": "Adler2007",
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
              "nulls": [
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
              "nulls": [
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
    ...


Full control over column names and data types
---------------------------------------------

By default the Retriever automatically detects both column names and data types, but you can also exercise complete control over the structure of the resulting database by adding column names and types.
These values are stored in the ``fields`` array of the ``schema`` dict of the JSON script.

::

  ...
  Enter columns [format = name, type, (optional) size]:

  count, int
  name, char, 40
  year, int
  ...

The Smith et al. Masses of Mammals dataset script includes this type of functionality.

::

  ...
  "name": "MoM2003",
  "resources": [
      {
          "dialect": {
              "nulls": [
                  -999
              ]
          },
          "name": "MOM",
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
  "title": "Masses of Mammals (Ecological Archives 2003)",
  ...

Restructuring cross-tab data
----------------------------

It is common in ecology to see data where the rows indicate one level of grouping (e.g., by site), the columns indicate another level of grouping (e.g., by species), and the values in each cell indicate the value for the group indicated by the row and column (e.g., the abundance of species x at site y). This is referred as cross-tab data and cannot be easily handled by database management systems, which are based on a one record per line structure. The Retriever can restructure this type of data into the appropriate form. In scripts this involves telling the retriever the name of the column to store the data in and the names of the columns to be restructured.

::

  ...
  Add crosstab columns? (y,N): y
  Crosstab column name: <name of column to store cross-tab data>
  Enter names of crosstab column values (Press return after each name):

  ct column 1
  ct column 2
  ct column 3
  ...

The `del Moral script`_. takes advantage of this functionality.

.. _`del Moral script`: https://github.com/weecology/retriever/blob/master/scripts/EA_del_moral_2010.script

::

  ...
  "name": "DelMoral2010",
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
  ...



Script Editing
--------------

The JSON scripts created using the retriever CLI can also be edited using the CLI.

To edit a script, use the ``retriever edit_json`` command, followed by the script's shortname;

For example, editing the ``MammalLH`` (Mammal Life History Database - Ernest, et al., 2003) dataset, the editing tool will ask a series a questions for each of the keys and values of the script, and act according to the input.

::

  dev@retriever:~$ retriever edit_json MammalLH


  ->description ( <type 'str'> ) :

  The purpose of this data set was to compile general life history characteristics for a variety of mammalian species to perform comparative life history analyses among different taxa and different body size groups.


  Select one of the following for the key 'description':

  1. Modify value
  2. Remove from script
  3. Continue (no changes)


  Your choice: 3

  ->title ( <type 'str'> ) :

  Mammal Life History Database - Ernest, et al., 2003


  Select one of the following for the key 'title':

  1. Modify value
  2. Remove from script
  3. Continue (no changes)


  Your choice: 3

  ->citation ( <type 'str'> ) :

  S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.


  Select one of the following for the key 'citation':

  1. Modify value
  2. Remove from script
  3. Continue (no changes)


  Your choice: 3

  ->urls ( <type 'dict'> ) :

  ('species', 'http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt')


  'urls' has the following keys:
  ['species']

  Edit the values for these sub-keys of urls? (y/N): n
  Select one of the following for the key 'urls':

  1. Add an item
  2. Modify an item
  3. Delete an item
  4. Remove from script
  5. Continue (no changes)


  Your choice: 5

  ->keywords ( <type 'list'> ) :

  Taxon > Mammals


  Data Type > Compilation


  1 .  Taxon > Mammals
  2 .  Data Type > Compilation
  Select one of the following for the key 'keywords':

  1. Add an item
  2. Delete an item
  3. Remove from script
  4. Continue (no changes)


  Your choice: 4

  ->homepage ( <type 'str'> ) :

  http://esapubs.org/archive/ecol/E084/093/


  Select one of the following for the key 'homepage':

  1. Modify value
  2. Remove from script
  3. Continue (no changes)


  Your choice: 3

  ->resources ( <type 'list'> ) :

  {'url': 'http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt', 'dialect': {}, 'name': 'species', 'schema': {}}


  1 .  {'url': 'http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt', 'dialect': {}, 'name': 'species', 'schema': {}}
  Edit the dict in 'resources'? (y/N): y

     ->url ( <type 'str'> ) :

     http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt


  Select one of the following for the key 'url':

  1. Modify value
  2. Remove from script
  3. Continue (no changes)


  Your choice: 3

     ->dialect ( <type 'dict'> ) :

  'dialect' has the following keys:
  []

  Edit the values for these sub-keys of dialect? (y/N): n
  Select one of the following for the key 'dialect':

  1. Add an item
  2. Modify an item
  3. Delete an item
  4. Remove from script
  5. Continue (no changes)


  Your choice: 5

     ->name ( <type 'str'> ) :

     species


  Select one of the following for the key 'name':

  1. Modify value
  2. Remove from script
  3. Continue (no changes)


  Your choice: 3

     ->schema ( <type 'dict'> ) :

  'schema' has the following keys:
  []

  Edit the values for these sub-keys of schema? (y/N): n
  Select one of the following for the key 'schema':

  1. Add an item
  2. Modify an item
  3. Delete an item
  4. Remove from script
  5. Continue (no changes)


  Your choice: 3
  Enter key to be deleted:
  Invalid key: Not found
  'schema' has the following keys:
  []

  Edit the values for these sub-keys of schema? (y/N): n
  Select one of the following for the key 'schema':

  1. Add an item
  2. Modify an item
  3. Delete an item
  4. Remove from script
  5. Continue (no changes)


  Your choice: 5
  Select one of the following for the key 'resources':

  1. Add an item
  2. Delete an item
  3. Remove from script
  4. Continue (no changes)


  Your choice: 4

  ->name ( <type 'str'> ) :

  MammalLH


  Select one of the following for the key 'name':

  1. Modify value
  2. Remove from script
  3. Continue (no changes)


  Your choice: 3


  Script written to /home/dev/.retriever/scripts/MammalLH.json
