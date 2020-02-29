import os
import platform

from retriever.lib.defaults import DATA_DIR
from retriever.lib.models import Engine


class engine(Engine):
    """Engine instance for Microsoft Access."""

    name = "Microsoft Access"
    instructions = ("Create a database in Microsoft Access, close Access."
                    "\nThen select your database file using this dialog.")
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
    insert_limit = 1000
    required_opts = [
        (
            "file",
            "Enter the filename of your Access database",
            "access.mdb",
            "Access databases (*.mdb, *.accdb)|*.mdb;*.accdb",
        ),
        ("table_name", "Format of table name", "[{db} {table}]"),
        ("data_dir", "Install directory", DATA_DIR),
    ]
    placeholder = "?"

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
            except BaseException:
                pass
        return converted

    def create_db(self):
        """MS Access doesn't create databases."""
        return None

    def drop_statement(self, object_type, object_name):
        """Returns a drop table or database SQL statement."""
        drop_statement = "DROP %s %s" % (object_type, object_name)
        return drop_statement

    def insert_data_from_file(self, filename):
        """Perform a bulk insert."""
        self.get_cursor()
        if self.check_bulk_insert() and self.table.header_rows < 2 and (
                self.table.delimiter in ["\t", ","]):
            print("Inserting data from " + os.path.basename(filename) + "...")

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
                    len_name = len(proper_name)
                    newfilename = '.'.join(
                        proper_name[0:-1] if len_name > 0 else proper_name[0]
                    ) + "_new." + filename.split(".")[-1]
                else:
                    newfilename = filename + "_new"

                if not os.path.isfile(newfilename):
                    print("Adding index to " + os.path.abspath(newfilename) + "...")
                    read = open(filename, "rb")
                    write = open(newfilename, "wb")
                    to_write = ""

                    for line in read:
                        line = line.strip()
                        to_write += str(id) + self.table.delimiter + line
                        add_to_record_id += 1
                    self.table.record_id += add_to_record_id

                    write.write(to_write + os.linesep)
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
                return True
            except BaseException:
                print("Couldn't bulk insert. Trying manual insert.")
                self.connection.rollback()
                self.table.record_id -= add_to_record_id
                return None
            finally:
                if need_to_delete:
                    os.remove(newfilename)

        return Engine.insert_data_from_file(self, filename)

    def get_connection(self):
        """Gets the db connection."""
        current_platform = platform.system().lower()
        if current_platform != "windows":
            raise Exception("MS Access can only be used in Windows.")
        import pypyodbc as dbapi  # pylint: disable=E0401

        self.get_input()
        file_name = self.opts["file"]
        file_dir = self.opts["data_dir"]
        ms_file = os.path.join(file_dir, file_name)

        if not os.path.exists(ms_file) and ms_file.endswith('.mdb'):
            dbapi.win_create_mdb(ms_file)
        connection_string = ("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" +
                             os.path.abspath(ms_file).replace("/", "//") + ";")
        return dbapi.connect(connection_string, autocommit=False)
