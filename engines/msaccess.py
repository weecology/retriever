import os
import platform
from retriever.lib.models import Engine, no_cleanup


class engine(Engine):
    """Engine instance for Microsoft Access."""
    name = "Microsoft Access"
    instructions = """Create a database in Microsoft Access, close Access, then \nselect your database file using this dialog."""
    abbreviation = "a"
    datatypes = ["AUTOINCREMENT",
                 "INTEGER",
                 "NUMERIC",
                 "NUMERIC",
                 "VARCHAR",
                 "BIT"]
    required_opts = [["file", 
                      "Enter the filename of your Access database: ",
                      "access.accdb",
                      "Access databases (*.mdb, *.accdb)|*.mdb;*.accdb"]]
                      
    def convert_data_type(self, datatype):
        """MS Access can't handle complex Decimal types"""
        converted = Engine.convert_data_type(self, datatype)
        if "NUMERIC" in converted:
            converted = "NUMERIC"
        elif "VARCHAR" in converted:
            length = int(converted.split('(')[1].split(')')[0].split(',')[0])
            if length > 255:
                converted = "TEXT"
        return converted
        
    def create_db(self):
        """MS Access doesn't create databases."""
        return None
        
    def drop_statement(self, objecttype, objectname):
        """Returns a drop table or database SQL statement."""
        dropstatement = "DROP %s %s" % (objecttype, objectname)
        return dropstatement

    def escape_single_quotes(self, line):
        return line.replace("'", "''")
        
    def format_column_name(self, column):
        return "[" + str(column) + "]"
        
    def insert_data_from_file(self, filename):
        """Perform a bulk insert."""
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if (self.table.cleanup.function == no_cleanup and not self.table.fixed_width and
            self.table.header_rows < 2) and (self.table.delimiter in ["\t", ","]) and not ct:  
            print ("Inserting data from " + os.path.basename(filename) + "...")
            
            if self.table.delimiter == "\t":
                fmt = "TabDelimited"
            elif self.table.delimiter == ",":
                fmt = "CSVDelimited"
                
            if self.table.header_rows == 1:
                hdr = "Yes"
            else:
                hdr = "No"

            columns = self.get_insert_columns()

            need_to_delete = False    
            if self.table.pk and not self.table.contains_pk:
                if '.' in os.path.basename(filename):
                    proper_name = filename.split('.')
                    print proper_name
                    newfilename = '.'.join((proper_name[0:-1]) if len(proper_name) > 0 else proper_name[0]
                                           ) + "_new." + filename.split(".")[-1]
                else:
                    newfilename = filename + "_new"
                if not os.path.isfile(newfilename):
                    print "Adding index to " + os.path.abspath(newfilename) + "..."
                    read = open(filename, "rb")
                    write = open(newfilename, "wb")
                    to_write = ""
                    id = self.table.record_id
                    for line in read:
                        to_write += str(id) + self.table.delimiter + line.replace("\n", "\r\n")
                        id += 1
                    self.table.record_id = id
                    write.write(to_write)
                    write.close()
                    read.close()
                    need_to_delete = True
                columns = "record_id, " + columns
            else:
                newfilename = filename
                        
            filename = os.path.abspath(newfilename)
            filename_length = (len(os.path.basename(filename)) * -1) - 1
            filepath = filename[0:filename_length]
            statement = """
INSERT INTO """ + self.tablename() + " (" + columns + """)
SELECT * FROM [""" + os.path.basename(filename) + ''']
IN "''' + filepath + '''" "Text;FMT=''' + fmt + ''';HDR=''' + hdr + ''';"'''
            
            try:
                self.cursor.execute(statement)
                self.connection.commit()
            except:
                print statement
                print "Couldn't bulk insert. Trying manual insert."
                self.connection.rollback()
                self.create_table()
                return Engine.insert_data_from_file(self, filename)
            
            if need_to_delete:
                os.remove(newfilename)
        else:
            return Engine.insert_data_from_file(self, filename)    
            
    def tablename(self):
        return "[" + self.db_name + " " + self.table.name + "]"
        
    def get_connection(self):
        """Gets the db connection."""
        p = platform.platform().lower()
        if "darwin" in p or not "win" in p:
            raise Exception("MS Access can only be used in Windows.")
        import pyodbc as dbapi
        self.get_input()
        connection_string = ("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="
                             + self.opts["file"].replace("/", "//") + ";")
        return dbapi.connect(connection_string, autocommit = False)
