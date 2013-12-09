---
layout: page
title: "Writing scripts for the EcoData Retriever"
comments: false
sharing: false
footer: true
---

Text Based Scripts
------------------

The EcoData Retriever includes a simple text file format for adding new
datasets. This allows users with no programming experience to quickly
add most standard datasets to the Retriever by specifying the names and
locations of the tables along with additional information about the
configuration of the data. Running custom scripts that are not part of
the Retriever is as easy as adding them to the directory where the
Retriever is being run, or to a subdirectory named \`\`scripts\`\`.

### Basic Scripts

The most basic scripts require only some general metadata about the
dataset, the name of the database and table, and the location of the
table. The basic script structure is as follows:

    name: Name of the dataset
    description: A brief description of the dataset of ~25 words.
    shortname: A one word name for the dataset
    table: Name of the table, URL to the table

The names before the colons tell the Retriever what information is
provided to the right of the colon. The text in *italics* should be
replaced with that for the dataset you are adding. For example, the
script for adding Morgan Ernest's mammalian life history dataset from
Ecological Archives is simply:

    # basic information about the script
    name: Mammal Life History Database - Ernest, et al., 2003
    shortname: MammalLH
    description: S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.
    tags: Taxon > Mammals, Data Type > Compilation

    # tables
    table: species, http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt
            

-   The first line of the script is the full name of the dataset
-   The second line gives a description of the dataset, in this case the
    full citation
-   The third line gives a short name for the database to be used in
    cases where a brief, typically single word description is required,
    such as for [installing from the command line](cli.html)
-   The forth line provides some optional tags to help with filtering
    the data
-   The last line gives the name for each table (there is only one table
    in this case), and its URL

### Multiple Tables

Adding datasets with multiple tables is handled simply by adding more
`table: ` lines to the script. For example, the script for adding
McGlinn et al. 2010 from Ecological Archives is:

    name: Vascular plant composition - McGlinn, et al., 2010
    description: Daniel J. McGlinn, Peter G. Earls, and Michael W. Palmer. 2010. A 12-year study on the scaling of vascular plant composition in an Oklahoma tallgrass prairie. Ecology 91:1872.
    shortname: McGlinn2010
    tags: Taxon > Plants, Spatial Scale > Local, Data Type > Time Series, Data Type > Observational

    table: pres, http://esapubs.org/archive/ecol/E091/124/TGPP_pres.csv
    table: cover, http://esapubs.org/archive/ecol/E091/124/TGPP_cover.csv
    table: richness, http://esapubs.org/archive/ecol/E091/124/TGPP_rich.csv
    table: species, http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv
    table: environment, http://esapubs.org/archive/ecol/E091/124/TGPP_env.csv
    table: climate, http://esapubs.org/archive/ecol/E091/124/TGPP_clim.csv

### Null Values

The Retriever can replace non-standard null values by adding an
additional line to the script with a comma separated list of those null
values after the table in which the null values occur

    table: name, url
    *nulls: -999, 'NA'

For example, the Capellini et al. 2010 script uses -9999 to indicate
null values.

    # Capellini et al. 2010, Ecological Archives, Retriever Script
    name: Phylogeny and metabolic rates in mammals (Ecological Archives 2010)
    description: Isabella Capellini, Chris Venditti, and Robert A. Barton. 2010. Phylogeny and metabolic rates in mammals. Ecology 20:2783-2793.
    shortname: MammalMR2010
    tags: Taxon > Mammals, Data Type > Compilation

    table: MammalMR2010, http://www.esapubs.org/archive/ecol/E091/198/data.txt
    *nulls: -9999

### Headers

If the first row of a table is the headers then naming the columns will,
be default, be handled automatically. If you want to rename an existing
header row for some reason, e.g., it includes reserved keywords for a
database management system, you can do so by adding a `replace: ` line
above the tables whose headings should be changed.

    table: name of table not requiring heading modification, URL
    replace: heading in datafile, new heading; another heading in datafile, new heading
    table: name of table to be modified, url
    table: name of second table to be modified in the same manner, url

The script for the Adler et al. 2007 dataset from Ecological Archives
includes this functionality.

    name: Kansas plant quadrats (Ecological Archives 2007)
    description: Peter B. Adler, William R. Tyburczy, and William K. Lauenroth. 2007. Long-term mapped quadrats from Kansas prairie: demographic information for herbaceaous plants. Ecology 88:2673.
    shortname: Adler2007
    tags: Taxon > Plants, Spatial Scale > Local, Data Type > Time Series, Data Type > Observational
    url: http://esapubs.org/archive/ecol/E088/161/

    table: main, http://esapubs.org/archive/ecol/E088/161/allrecords.csv
    table: quadrat_info, http://esapubs.org/archive/ecol/E088/161/quadrat_info.csv
    table: quadrat_inventory, http://esapubs.org/archive/ecol/E088/161/quadrat_inventory.csv
    *nulls: 'NA'
    table: species, http://esapubs.org/archive/ecol/E088/161/species_list.csv

    replace: jan, january; feb, february; mar, march; apr, april; jun, june; jul, july; aug, august; sep, september; oct, october; nov, november; dec, december
    table: monthly_temp, http://esapubs.org/archive/ecol/E088/161/monthly_temp.csv
    *nulls: 'NA'
    table: monthly_ppt, http://esapubs.org/archive/ecol/E088/161/monthly_ppt.csv
    *nulls: 'NA'

### Full control over column names and data types

By default the Retriever automatically detects both column names and
data types, but you can also exercise complete over the structure of the
resulting database by adding `column*: ` lines after a table.

    table: name, url
    *column: Name for 1st column, type, type details (e.g. max string length)
    *column: Name for 2nd column, type, type details

The Smith et al. Masses of Mammals dataset script includes this type of
functionality.

    name: Masses of Mammals (Ecological Archives 2003)
    description: Felisa A. Smith, S. Kathleen Lyons, S. K. Morgan Ernest, Kate E. Jones, Dawn M. Kaufman, Tamar Dayan, Pablo A. Marquet, James H. Brown, and John P. Haskell. 2003. Body mass of late Quaternary mammals. Ecology 84:3403.
    shortname: MoM2003
    tags: Taxon > Mammals, Data Type > Compilation
    url: http://www.esapubs.org/archive/ecol/E084/094/

    table: MOM, http://www.esapubs.org/Archive/ecol/E084/094/MOMv3.3.txt
    *nulls: -999
    *column: record_id, pk-auto
    *column: continent, char, 20
    *column: status, char, 20
    *column: sporder, char, 20
    *column: family, char, 20
    *column: genus, char, 20
    *column: species, char, 20
    *column: log_mass_g, double
    *column: comb_mass_g, double
    *column: reference, char

### Restructuring cross-tab data

It is common in ecology to see where the rows indicated one level of
grouping (e.g., by site) and the columns indicate another level of
grouping (e.g., by species) and the values in each cell indicate the
value for the group indicated by the row and column (e.g., the abundance
of species x at site y). This is referred as cross-tab data and cannot
be easily handled by database systems, which are based on a one record
per line structure. The Retriever can restructure this type of data into
the appropriate form. In scripts this involves telling the retriever the
name of the column to store the data in and the names of the columns to
be restructured.

    table: name, url
    *column: name of regular column, type
    *column: another regular column name, type
    *ct_column: name of column to store cross-tab data
    *ct_names: name of crosstab column 1, name of CT col 2, name of CT col 3

The del Moral Mount St. Helens script takes advantage of this
functionality.

    name: Vegetation plots - del Moral, 2010
    description: Roger del Moral. 2010. Thirty years of permanent vegetation plots, Mount St. Helens, Washington. Ecology 91:2185.
    shortname: DelMoral2010
    tags: Taxon > Plants, Spatial Scale > Local, Data Type > Time Series, Data Type > Observational

    table: species_plot_year, http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_PLOT_YEAR.csv
    *delimiter: ','
    *column: record_id, pk-auto
    *column: plot_id_year, char, 20
    *column: plot_name, char, 4
    *column: plot_number, int
    *column: year, int
    *column: count, ct-double
    *ct_column: species
    *ct_names: Abilas,Abipro,Achmil,Achocc,Agoaur,Agrexa,Agrpal,Agrsca,Alnvir,Anamar,Antmic,Antros,Aqifor,Arcnev,Arnlat,Astled,Athdis,Blespi,Brocar,Brosit,Carmer,Carmic,Carpac,Carpay,Carpha,Carros,Carspe,Casmin,Chaang,Cirarv,Cisumb,Crycas,Danint,Descae,Elyely,Epiana,Eriova,Eripyr,Fesocc,Fravir,Gencal,Hiealb,Hiegra,Hyprad,Junmer,Junpar,Juncom,Leppun,Lommar,Luepec,Luihyp,Luplat,Luplep,Luzpar,Maiste,Pencar,Pencon,Penser,Phahas,Phlalp,Phldif,Phyemp,Pincon,Poasec,Poldav,Polmin,Pollon,Poljun,Popbal,Potarg,Psemen,Raccan,Rumace,Salsit,Saxfer,Senspp,Sibpro,Sorsit,Spiden,Trispi,Tsumer,Vacmem,Vervir,Vioadu,Xerten

    table: structure_plot_year, http://esapubs.org/archive/ecol/E091/152/MSH_STRUCTURE_PLOT_YEAR.csv
    table: species, http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_DESCRIPTORS.csv
    *escape_single_quotes: True
    table: plots, http://esapubs.org/archive/ecol/E091/152/MSH_PLOT_DESCRIPTORS.csv
