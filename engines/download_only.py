import os
import platform
import shutil
import inspect
from retriever.lib.engine import filename_from_url
from retriever.lib.models import Engine, no_cleanup
from retriever import DATA_DIR, HOME_DIR

class DummyConnection:
    def cursor(self):
        pass
    def commit(self):
        pass
    def rollback(self):
        pass
    def close(self):
        pass

class DummyCursor(DummyConnection):
    pass


class engine(Engine):
    """Engine instance for writing data to a CSV file."""
    name = "Download Only"
    abbreviation = "download"
    required_opts = [("path",
                      "File path to copy data files",
                      "./"),
                     ]

    def table_exists(self, dbname, tablename):
        try:
            tablename = self.table_name(name=tablename, dbname=dbname)
            return os.path.exists(tablename)
        except:
            return False

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()

    def final_cleanup(self):
        data_dir = self.format_data_dir()
        if hasattr(self, "all_files"):
            for file_name in self.all_files:
                file_path, file_name_nopath = os.path.split(file_name)
                full_path = os.path.join(self.opts['path'], file_name_nopath)
                if file_path == DATA_DIR:
                    print ("%s is already in the working directory" % file_name_nopath)
                    print("Keeping existing copy.")
                elif os.path.exists(full_path):
                    print ("File already exists at specified location")
                else:
                    if os.path.isdir(self.opts['path']):
                        print("Copying %s from %s" % (file_name_nopath, file_path))
                        try:
                            shutil.copy(file_name, self.opts['path'])
                        except:
                            print("Couldn't copy file to %s" % self.opts['path'])
                    else:
                        try:
                            print("Creating directory %s" % self.opts['path'])
                            os.mkdir(self.opts['path'])
                            print("Copying %s from %s" % (file_name_nopath, file_path))
                            shutil.copy(file_name, self.opts['path'])
                        except:
                            print("Couldn't create directory %s" % self.opts['path'])
        self.all_files = set()

    def auto_create_table(self, table, url=None, filename=None, pk=None):
        if url and not filename:
            filename = filename_from_url(url)

        if url and not self.find_file(filename):
            # If the file doesn't exist, download it
            self.download_file(url, filename)

    def insert_data_from_url(self, url):
        filename = filename_from_url(url)
        find = self.find_file(filename)
        if not find:
            self.create_raw_data_dir()
            self.download_file(url, filename)

    def find_file(self, filename):
        result = Engine.find_file(self, filename)
        if not hasattr(self, "all_files"): self.all_files = set()
        if result: self.all_files.add(result)
        return result

    def register_files(self, filenames):
        """Identify a list of files to be moved by the download

        When downloading archives with multiple files the engine needs to be
        informed of all of the file names so that it can move them.

        """
        full_filenames = {self.find_file(filename) for filename in filenames}
        self.all_files = self.all_files.union(full_filenames)


# replace all other methods with a function that does nothing
def dummy_method(self, *args, **kwargs):
    pass
methods = inspect.getmembers(engine, predicate=inspect.ismethod)
keep_methods = {'table_exists',
                'get_connection',
                'final_cleanup',
                'auto_create_table',
                'insert_data_from_url',
                }
remove_methods = ['insert_data_from_file']
for name, method in methods:
    if (not name in keep_methods
        and not 'download' in name
        and not 'file' in name
        and not 'dir' in name):

        setattr(engine, name, dummy_method)
for name in remove_methods:
    setattr(engine, name, dummy_method)

