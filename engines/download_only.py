import os
import platform
import shutil
import inspect
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
        for file_name in os.listdir(data_dir):
            print file_name
            shutil.copy(os.path.join(data_dir, file_name), './')


# replace all other methods with a function that does nothing
def dummy_method(self, *args, **kwargs):
    pass
methods = inspect.getmembers(engine, predicate=inspect.ismethod)
keep_methods = {'table_exists',
                'get_connection',
                'final_cleanup',
                }
for name, method in methods:
    if (not name in keep_methods
        and not 'download' in name
        and not 'filename' in name
        and not 'dir' in name):
        
        setattr(engine, name, dummy_method)