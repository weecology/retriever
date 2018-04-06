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

Now, a role will be created using CREATE ROLE. A role is an entity that can own database objects and have database privileges. It can be given CREATEDB and CREATEROLE privileges. For example, the following command creates a role named "newadmin" with password "abcdefgh". It is equipped with privileges of creating a new role and creating a new database.

>>> create role newadmin with createrole createdb login password 'abcdefgh';




