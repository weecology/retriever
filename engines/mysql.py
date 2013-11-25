import os
import platform
from retriever.lib.models import Engine, no_cleanup


class engine(Engine):
    """Engine instance for MySQL."""
    name = "MySQL"
    abbreviation = "mysql"
    datatypes = {
                 "auto": "INT(5) NOT NULL AUTO_INCREMENT",
                 "int": "INT",
                 "bigint": "BIGINT",
                 "double": "DOUBLE",
                 "decimal": "DECIMAL",
                 "char": ("TEXT", "VARCHAR"),
                 "bool": "BOOL",
                 }
    max_int = 4294967295
    required_opts = [("user",
                      "Enter your MySQL username", 
                      "root"),
                     ("password",
                      "Enter your password", 
                      ""),
                     ("host",
                      "Enter your MySQL host", 
                      "localhost"),
                     ("port",
                      "Enter your MySQL port", 
                      3306),
                     ("database_name",
                      "Format of database name",
                      "{db}"),
                     ("table_name",
                      "Format of table name",
                      "{db}.{table}"),
                     ]
                      
    def create_db_statement(self):
        createstatement = "CREATE DATABASE IF NOT EXISTS " + self.database_name()
        return createstatement
        
    def insert_data_from_file(self, filename):
        """Calls MySQL "LOAD DATA LOCAL INFILE" statement to perform a bulk 
        insert."""
        self.get_cursor()
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if (self.table.cleanup.function == no_cleanup 
            and not self.table.fixed_width 
            and not ct
            and (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)
            ):
            print ("Inserting data from " + os.path.basename(filename) + "...")
            
            columns = self.table.get_insert_columns()
            statement = """        
LOAD DATA LOCAL INFILE '""" + filename.replace("\\", "\\\\") + """'
INTO TABLE """ + self.tablename() + """
FIELDS TERMINATED BY '""" + self.table.delimiter + """'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE """ + str(self.table.header_rows) + """ LINES
(""" + columns + ")"
            try:
                self.cursor.execute(statement)
            except Exception as e:
                print "Failed bulk insert (%s), inserting manually" % e
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)
        
    def table_exists(self, dbname, tablename):
        try:
            tablename = self.tablename(name=tablename, dbname=dbname)
            test_statement = "SELECT * FROM " + tablename + " LIMIT 1"
            self.cursor.execute(test_statement)
            l = len(cursor.fetchall())
            return l > 0
        except:
            return False
        
    def get_connection(self):
        """Gets the db connection."""
        args = {'host': self.opts['host'],
                'port': int(self.opts['port']),
                'user': self.opts['user'],
                'passwd': self.opts['password']}

        try:
            import pymysql as dbapi
            import pymysql.constants.CLIENT as client
            args['client_flag'] = client.LOCAL_FILES
        except ImportError:
            import MySQLdb as dbapi
            import MySQLdb.constants.CLIENT as client
            args['client_flag'] = client.LOCAL_FILES
        self.get_input()
        
        return dbapi.connect(**args)
