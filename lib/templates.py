"""Class models for dataset scripts from various locations. Scripts should
inherit from the most specific class available."""

from retriever.lib.models import Database, Table, Cleanup, correct_invalid_value
from retriever.lib.tools import get_opts, choose_engine


class Script:
    """This class represents a database toolkit script. Scripts should inherit
    from this class and execute their code in the download method."""
    def __init__(self, name="", description="", shortname="", urls=dict(), 
                 tables=dict(), ref="", public=True, addendum=None, **kwargs):
        self.name = name
        self.shortname = shortname
        self.description = description
        self.urls = urls
        self.tables = tables
        self.ref = ref
        self.public = public
        self.addendum = addendum
        self.tags = []
        for key, item in kwargs.items():
            setattr(self, key, item[0] if isinstance(item, tuple) else item)
            
    def __str__(self):
        desc = self.name
        if self.reference_url():
            desc += "\n" + self.reference_url()
        return desc
        
    def download(self, engine=None):
        self.engine = self.checkengine(engine)
        db = Database()
        db.dbname = self.shortname
        self.engine.db = db
        self.engine.get_cursor()
        self.engine.create_db()
        
    def reference_url(self):
        if self.ref:
            return self.ref
        else:
            if len(self.urls) == 1:
                return self.urls[self.urls.keys()[0]]
            else:
                return None
                
    def checkengine(self, engine=None):
        if not engine:
            opts = get_opts()
            engine = choose_engine(opts)
        engine.script = self            
        return engine
        
    def exists(self, engine=None):
        return all([engine.table_exists(self.shortname, key) 
                    for key in self.urls.keys() if key])
    
    
class BasicTextTemplate(Script):
    """Script template based on data files from Ecological Archives."""
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        
    def download(self, engine=None):
        Script.download(self, engine)
        
        for key in self.urls.keys():
            if not key in self.tables.keys():
                self.tables[key] = Table(key, cleanup=Cleanup(correct_invalid_value,
                                                              nulls=[-999]))
        
        for key, value in self.urls.items():
            self.engine.auto_create_table(self.tables[key], url=value)
            self.engine.insert_data_from_url(value)
            self.tables[key].record_id = 0
        return self.engine
        
    def reference_url(self):
        if self.ref:
            return self.ref
        else:
            if len(self.urls) == 1:
                return '/'.join(self.urls[self.urls.keys()[0]].split('/')[0:-1]) + '/'
        
        
TEMPLATES = [
             ("Basic Text", BasicTextTemplate)
             ]
