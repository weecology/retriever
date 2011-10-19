import os
import platform
from retriever.lib.models import Engine, no_cleanup


class engine(Engine):
    """Engine instance for MySQL."""
    name = "MySQL"
    abbreviation = "m"
    datatypes = ["INT(5) NOT NULL AUTO_INCREMENT", 
                 "INT", 
                 "DOUBLE",
                 "DECIMAL", 
                 "VARCHAR", 
                 "BOOL"]
    required_opts = [["username", 
                      "Enter your MySQL username: ", 
                      "root"],
                     ["password", 
                      "Enter your password: ", 
                      ""],
                     ["hostname", 
                      "Enter your MySQL host or press Enter " +
                      "for the default (localhost): ", 
                      "localhost"],                     
                     ["port", 
                      "Enter your MySQL port or press Enter " +
                      "for the default (3306): ", 
                      3306]]
                      
    def create_db_statement(self):
        createstatement = "CREATE DATABASE IF NOT EXISTS " + self.db_name
        return createstatement
        
    def insert_data_from_file(self, filename):
        """Calls MySQL "LOAD DATA LOCAL INFILE" statement to perform a bulk 
        insert."""
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if self.table.cleanup.function == no_cleanup and not self.table.fixed_width and not ct:
            print ("Inserting data from " + os.path.basename(filename) + "...")
            
            columns = self.get_insert_columns()            
            statement = """        
LOAD DATA LOCAL INFILE '""" + filename.replace("\\", "\\\\") + """'
INTO TABLE """ + self.tablename() + """
FIELDS TERMINATED BY '""" + self.table.delimiter + """'
LINES TERMINATED BY '\\n'
IGNORE """ + str(self.table.header_rows) + """ LINES
(""" + columns + ")"
            
            self.cursor.execute(statement)
        else:
            return Engine.insert_data_from_file(self, filename)
        
    def table_exists(self, dbname, tablename):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM " + dbname + "." + tablename + " LIMIT 1")
            l = len(cursor.fetchall())
            connection.close()
            return l > 0
        except:
            return False
        
    def get_connection(self):
        """Gets the db connection."""
        import MySQLdb as dbapi
        self.get_input()
        return dbapi.connect(host = self.opts["hostname"],
                             port = int(self.opts["port"]),
                             user = self.opts["username"],
                             passwd = self.opts["password"])
