Using the Command Line Interface
--------------------------------

The Retriever includes a command line interface to allow its
capabilities to be integrated into scientific workflows involving
non-Python programming languages. For example, the Retriever can easily
be called from R (or run as part of a pipe workflow including R) to
automate the downloading and installing of databases necessary for
analysis. This also makes it easier to use in batch processes or on
servers that don't have graphical capabilities.

After installing, run `retriever update` to download all of the
available dataset scripts. To see the full list of command line options
and datasets run `retriever --help`. The output will look like this:

    usage: retriever [-h] [-v] {install,update,gui,new,ls,help} ...

    positional arguments:
      {install,update,gui,new,ls,help}
                            sub-command help
        install             download and install dataset
        update              download updated versions of scripts
        gui                 launch retriever in graphical mode
        new                 create a new sample retriever script
        ls                  display a list all available dataset scripts
        help

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit

#### Standard Usage

To get the most recent versions of the data set scripts, run
`retriever update`

To install datasets, use `retriever install`:

    usage: retriever install [-h] [-e ENGINE] [-u [USER]] [-p [PASSWORD]]
                             [--host [HOST]] [-o [PORT]] [-d [DB]] [-f [FILE]]
                             [--compile] [--debug]
                             [dataset]

    positional arguments:
      dataset               dataset name

    optional arguments:
      -h, --help            show this help message and exit
      -e ENGINE, --engine ENGINE
                            engine (m=MySQL, p=PostgreSQL, s=SQLite, a=Microsoft
                            Access, c=CSV)
      -u [USER], --user [USER]
                            username for database connection, if applicable
      -p [PASSWORD], --password [PASSWORD]
                            password for database connection, if applicable
      --host [HOST]         host for engine, if applicable
      -o [PORT], --port [PORT]
                            port for engine, if applicable
      -d [DB], --db [DB]    database for engine, if applicable
      -f [FILE], --file [FILE]
                            file for engine, if applicable
      --compile             force re-compile of script before downloading
      --debug               run in debug mode

For example, to install the Breeding Bird Survey data into an sqlite
database named mydatabase.db you would use:

    retriever install BBS -e s -f mydatabase.db

You will be prompted for any necessary connection information that is
not provided.

To download all data for a given category (such as all data related to
BIRDS), you can use:

    retriever install birds -e s -f mydatabase.db

This is the same as `retriever install ___` for every dataset with the
BIRDS tag.

### Using the Command Line Interface from inside R

Because we have a command line interface, using the EcoData Retriever
with languages other than the one it is written in is easy. Using the
Retriever from inside of R just requires the use of the `system()`
function and your preferred approach for importing data.

#### Basics (Linux and Installations from Source)

In the simplest case, if you wanted to import the Gentry Forest Transect
Data the following command from inside of R will download the data,
convert it to a useable form, save it as comma delimited text files.

    system("retriever install Gentry -e c")

Then you can simply import the resulting files in the usual manner.

    count_data <- read.csv("Gentry_counts.csv")
    stem_data <- read.csv("Gentry_stems.csv")
    species_data <- read.csv("Gentry_species.csv")
    sites_data <- read.csv("Gentry_sites.csv")

Alternatively you can use a modified version of the `system()` function
to import into to the other database management systems and then
interact with them through packages like
[RSQLite](http://cran.r-project.org/web/packages/RSQLite/index.html) and
[RMySQL](http://cran.r-project.org/web/packages/RMySQL/index.html)

#### Windows

On Windows it is necessary for the working directory to be set to the
location of the retriever.exe file so that R knows where the Retriever
is located. So, if I placed the Retriever on my Desktop I would use the
commands:

    setwd("C:\Users\ethan\Desktop")
    system("retriever install Gentry -e c")

If you put a copy of the Retriever in the working directory for the
project then setting the working directory manually is not necessary.
