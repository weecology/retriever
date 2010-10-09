import os
import platform
from dbtk.lib.models import Engine, no_cleanup

class engine(Engine):
    """Engine instance for PostgreSQL."""
    name = "PostgreSQL"
    abbreviation = "p"
    datatypes = ["serial", 
                 "integer", 
                 "double precision",
                 "decimal", 
                 "varchar", 
                 "bit"]    
    required_opts = [["username", 
                      "Enter your PostgreSQL username: ", 
                      "postgres"],
                     ["password", 
                      "Enter your password: ", ""],
                     ["hostname", 
                      "Enter your PostgreSQL host or press Enter " +
                      "for the default (localhost): ", "localhost"],
                     ["sqlport", "Enter your PostgreSQL port or press" + 
                      "Enter for the default (5432): ", 5432],
                     ["database", 
                      "Enter your PostgreSQL database name or press " +
                      "Enter for the default (postgres): ", "postgres"]]            
    def create_db_statement(self):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        return Engine.create_db_statement(self).replace("DATABASE", "SCHEMA")
    def create_db(self):
        try:
            Engine.create_db(self)
        except:
            self.connection.rollback()
            pass
    def create_table(self):
        """PostgreSQL needs to commit operations individually."""
        Engine.create_table(self)
        self.connection.commit()
    def drop_statement(self, objecttype, objectname):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        statement = Engine.drop_statement(self, objecttype, objectname) 
        statement += " CASCADE;"
        return statement.replace(" DATABASE ", " SCHEMA ")    
    def insert_data_from_file(self, filename):
        """Use PostgreSQL's "COPY FROM" statement to perform a bulk insert."""
        if ([self.table.cleanup.function, self.table.delimiter, 
             self.table.header_rows] == [no_cleanup, ",", 1]):        
            print ("Inserting data from " + os.path.basename(filename) 
                   + " . . .")
                
            columns = self.get_insert_columns()    
            filename = os.path.abspath(filename)
            statement = """
COPY """ + self.tablename() + " (" + columns + """)
FROM '""" + filename.replace("\\", "\\\\") + """'
WITH DELIMITER ','
CSV HEADER"""
            try:
                self.cursor.execute(statement)
                self.connection.commit()
            except:
                self.connection.rollback()
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)                
    def get_cursor(self):
        """Gets the db connection and cursor."""
        import psycopg2 as dbapi    
        self.get_input()            
        self.connection = dbapi.connect(host = self.opts["hostname"],
                                        port = int(self.opts["sqlport"]),
                                        user = self.opts["username"],
                                        password = self.opts["password"],
                                        database = self.opts["database"])        
        self.cursor = self.connection.cursor()    

