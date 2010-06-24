"""Database Toolkit for Breeding Bird Survey 

See dbtk_tools.py for usage

"""

from dbtk_tools import *
import datacleanup

# Variables to get text file/create database
db = Database()
db.dbname = "BBS"
db.opts = get_opts()
db.engine = choose_engine(db)
db.cursor = get_cursor(db)
create_database(db)

table = Table()
table.tablename = ""
table.pk = "species_id"
table.source = open_url(table, "")
table.cleanup = datacleanup.correct_invalid_value

table.columns=[]
create_table(db, table)