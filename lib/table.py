from retriever.lib.cleanup import *

class Table:
    """Information about a database table."""
    def __init__(self, name, **kwargs):
        self.name = name
        self.pk = True
        self.contains_pk = False
        self.delimiter = None
        self.header_rows = 1
        self.column_names_row = 1
        self.fixed_width = False
        self.cleanup = Cleanup()
        self.record_id = 0
        self.columns = []
        self.replace_columns = []
        self.escape_single_quotes=True
        self.escape_double_quotes=True
        for key, item in kwargs.items():
            setattr(self, key, item[0] if isinstance(item, tuple) else item)
