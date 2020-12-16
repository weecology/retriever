======================
Spatial database setup
======================

Supporting installation of spatial data into `Postgres DBMS`.

1. **Install Postgres**

  For Mac the easiest way to get started with PostgreSQL is with `Postgres.app`_.

  For Debain and Ubuntu, install `PostgresSQL and PostGis` please ref to `Postgres installation`_.

  Otherwise you can try package installers for WINDOWS, MAC, Linux and MacOS from the main `PostgreSQL download`_ page

  For simplicity, use `.pgpass` file(`pgpass.conf` file for Microsoft Windows) to avoid supplying the password every time
  as decribed in `Passwordless configuration`_.

  After installation, Make sure you have the paths to these tools added to your system's `PATHS`.

  Note: Older version of this `raster2pgsql` was a python script that you had to download and manually include in Postgres's directory.
  Please consult an operating system expert for help on how to change or add the `PATH` variables.

  **For example, this could be a sample of paths exported on Mac:**

.. code-block::

  #~/.bash_profile file, Postgres PATHS and tools .
  export PATH="/Applications/Postgres.app/Contents/MacOS/bin:${PATH}"
  export PATH="$PATH:/Applications/Postgres.app/Contents/Versions/10/bin"


2. **Enable PostGIS extensions**

  If you have Postgres set up, enable `PostGIS extensions`.
  This is done by using either `Postgres CLI` or `GUI(PgAdmin)` and run
  **For psql CLI**

.. note::
    PostGIS excluded the raster types and functions from the main extension as of version 3.x;
    A separate CREATE EXTENSION postgis_raster; is then needed to get raster support.

    Versions 2.x have full raster support as part of the main extension environment,
    so CREATE EXTENSION postgis; is all that you need`

.. code-block::

  psql -d yourdatabase -c "CREATE EXTENSION postgis;"
  psql -d yourdatabase -c "CREATE EXTENSION postgis_topology;"

  **For GUI(PgAdmin)**

.. code-block::

  `CREATE EXTENSION postgis;`
  `CREATE EXTENSION postgis_topology`

For more details refer to the `Postgis docs`_.


.. _PostgreSQL download: https://www.postgresql.org/download/
.. _Postgres.app: https://postgresapp.com/
.. _Postgres installation: https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS21UbuntuPGSQL93Apt
.. _Postgis docs: https://postgis.net/docs/postgis_installation.html#install_short_version
.. _Passwordless configuration: developer.html#passwordless-configuration
