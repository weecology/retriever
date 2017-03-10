from __future__ import print_function
from builtins import str
import os
from retriever.lib.models import Engine, no_cleanup
from retriever import DATA_DIR, current_platform


class engine(Engine):
    """Engine instance for Microsoft Access."""
    name = "Microsoft Access"
    instructions = """Create a database in Microsoft Access, close Access, then \nselect your database file using this dialog."""
    abbreviation = "msaccess"
    datatypes = {
        "auto": "AUTOINCREMENT",
        "int": "INTEGER",
        "bigint": "INTEGER",
        "double": "NUMERIC",
        "decimal": "NUMERIC",
        "char": "VARCHAR",
        "bool": "BIT",
    }
    required_opts = [("file",
                      "Enter the filename of your Access database",
                      os.path.join(DATA_DIR, "access.mdb"),
                      "Access databases (*.mdb, *.accdb)|*.mdb;*.accdb"),
                     ("table_name",
                      "Format of table name",
                      "[{db} {table}]"),
                     ]

    def convert_data_type(self, datatype):
        """MS Access can't handle complex Decimal types"""
        converted = Engine.convert_data_type(self, datatype)
        if "NUMERIC" in converted:
            converted = "NUMERIC"
        elif "VARCHAR" in converted:
            try:
                length = int(converted.split('(')[1].split(')')[0].split(',')[0])
                if length > 255:
                    converted = "TEXT"
            except:
                pass
        return converted

    def create_db(self):
        """MS Access doesn't create databases."""
        return None

    def drop_statement(self, objecttype, objectname):
        """Returns a drop table or database SQL statement."""
        dropstatement = "DROP %s %s" % (objecttype, objectname)
        return dropstatement

    def escape_single_quotes(self, value):
        """Escapes the single quotes in the value"""
        return value.replace("'", "''")

    def insert_data_from_file(self, filename):
        """Perform a bulk insert."""
        self.get_cursor()
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if ((self.table.cleanup.function == no_cleanup and not self.table.fixed_width and
             self.table.header_rows < 2)
            and (self.table.delimiter in ["\t", ","])
            and not ct
            and (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)
            ):
            print ("Inserting data from " + os.path.basename(filename) + "...")

            if self.table.delimiter == "\t":
                fmt = "TabDelimited"
            elif self.table.delimiter == ",":
                fmt = "CSVDelimited"

            if self.table.header_rows == 1:
                hdr = "Yes"
            else:
                hdr = "No"

            columns = self.table.get_insert_columns()

            need_to_delete = False
            add_to_record_id = 0

            if self.table.pk and not self.table.contains_pk:
                if '.' in os.path.basename(filename):
                    proper_name = filename.split('.')
                    newfilename = '.'.join((proper_name[0:-1]) if len(proper_name) > 0 else proper_name[0]
                                           ) + "_new." + filename.split(".")[-1]
                else:
                    newfilename = filename + "_new"

                if not os.path.isfile(newfilename):
                    print("Adding index to " + os.path.abspath(newfilename) + "...")
                    read = open(filename, "rb")
                    write = open(newfilename, "wb")
                    to_write = ""

                    for line in read:
                        to_write += str(id) + self.table.delimiter + line.replace("\n", "\r\n")
                        add_to_record_id += 1
                    self.table.record_id += add_to_record_id

                    write.write(to_write)
                    write.close()
                    read.close()
                    need_to_delete = True
                columns = "record_id, " + columns
            else:
                newfilename = filename

            newfilename = os.path.abspath(newfilename)
            filename_length = (len(os.path.basename(newfilename)) * -1) - 1
            filepath = newfilename[:filename_length]
            statement = """
INSERT INTO """ + self.table_name() + " (" + columns + """)
SELECT * FROM [""" + os.path.basename(newfilename) + ''']
IN "''' + filepath + '''" "Text;FMT=''' + fmt + ''';HDR=''' + hdr + ''';"'''

            try:
                self.execute(statement)
            except:
                print("Couldn't bulk insert. Trying manual insert.")
                self.connection.rollback()

                self.table.record_id -= add_to_record_id

                return Engine.insert_data_from_file(self, filename)

            if need_to_delete:
                os.remove(newfilename)

        else:
            return Engine.insert_data_from_file(self, filename)

    def table_exists(self, dbname, tablename):
        """Determine if the table already exists in the database"""
        if not hasattr(self, 'existing_table_names'):
            self.existing_table_names = set()
            for row in self.cursor.tables():
                tableinfo = row[2]
                if not tableinfo.startswith("MSys"):
                    # ignore system tables
                    database, table = tableinfo.split()
                    self.existing_table_names.add((database, table))
        return self.table_name(name=tablename, dbname=dbname).lower() in self.existing_table_names

    def get_connection(self):
        """Gets the db connection."""
        if current_platform != "windows":
            raise Exception("MS Access can only be used in Windows.")
        import pypyodbc as dbapi
        self.get_input()
        if not os.path.exists(self.opts['file']) and self.opts['file'].endswith('.mdb'):
            dbapi.win_create_mdb(self.opts['file'])
        connection_string = ("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" +
                             os.path.abspath(self.opts["file"]).replace("/", "//") + ";")
        return dbapi.connect(connection_string, autocommit=False)
