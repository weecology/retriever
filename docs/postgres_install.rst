===============================
RDataRetriever with PostgreSQL
===============================

RDataRetriever supports different DBMS for storing of downloaded datasets through the Retriever R API. It supports PostgreSQL, MySQL, SQLite and MS Access.


Installation of PostgreSQL in Ubuntu
====================================

PostgreSQL installation command differs in the basis of Ubuntu version (Trusty 14.04, Xenial 16.04, Zesty 17.04). The following are the steps:

- Create the file /etc/apt/sources.list.d/pgdg.list, and add a line for the repository 

>>> deb http://apt.postgresql.org/pub/repos/apt/ <ubuntu_version>-pgdg main

For example:

>>> deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main

- Import the repository signing key, and update the package lists 

>>> wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

>>> sudo apt-get update 

- To install PostgreSQL on Ubuntu, use the apt-get (or other apt-driving) command: 

>>> apt-get install postgresql-<version>

Once it is installed, we will setup PostgreSQL by first running the postgres client as root:

>>> sudo -u postgres psql

Now, a role will be created using CREATE ROLE. A role is an entity that can own database objects and have database privileges. It can be given CREATEDB and CREATEROLE privileges. For example, the following command creates a role named ``newadmin`` with password ``abcdefgh``. It is equipped with privileges of creating a new role and creating a new database.

>>> create role newadmin with createrole createdb login password 'abcdefgh';

Next, exit the PostgreSQL client by the following command:

>>> \q

We will need to change the pg_hba.conf file to indicate that users will authenticate by md5 as opposed to peer authentication. To do this, first open the pg_hba.conf file by running the command:

>>> sudo nano /etc/postgresql/x.x/main/pg_hba.conf

Where x.x is the version installed, in this case x.x = 9.6

Change the line ``local all postgres peer`` to ``local all postgres md5``. Also, change the line ``local all all peer`` to ``local all all md5``. After making these changes, make sure to save the file.

Restart the postgresql client:

>>> sudo service postgresql restart

Now, we will be able to login to the postgres client with the newadmin user that we created by running the following command:

>>> psql -U newadmin -d postgres -h localhost -W

You will be prompted to enter a password, which is ``abcdefgh``. You can create a database (for instance: newdb) with the following command:

>>> createdb -U vmsadmin vms;

You will be again prompted for password. After the successful setup of PostgreSQL, it can now be used with R API for Retriever.

====================================
Using PostgreSQL with RDataRetriever
====================================

While using PostgreSQL as a connection type for ``rdataretriever::install`` function, a file named ``postgres.conn`` is needed. It contains information for establishing connection with the requested DBMS, in this case, PostgreSQL. Default location of the file is the directory, through which RStudio is running. If it saved in some other location, its path needs to be given to the install function.
In the above example, ``postgres.conn`` will look like below:


.. code-block:: python

  host localhost 
  port 5432 
  user newadmin
  password abcdefgh

Assuming it is saved in default directory, ``install`` function for ``airports`` dataset can be executed as follows:

>>> rdataretriever::install('airports',connection = 'postgres')




