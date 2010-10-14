"""Class models for dataset scripts from various locations. Scripts should
inherit from the most specific class available."""

from dbtk.lib.models import Database, Cleanup, correct_invalid_value


class DbTk:
    """This class represents a database toolkit script. Scripts should inherit
    from this class and execute their code in the download method."""
    name = ""
    shortname = ""
    url = ""
    ref = ""
    public = True
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
            return '/'.join(self.url.split('/')[0:-1]) + '/'
    def checkengine(self, engine=None):
        if not engine:
            opts = get_opts()
            engine = choose_engine(opts)
        engine.script = self            
        return engine
    
    
class EcologicalArchives(DbTk):
    """DbTk script template based on data files from Ecological Archives."""
    nulls = ['-999', '-999.9']
    def download(self, engine=None):
        DbTk.download(self, engine)
        self.engine.auto_create_table(self.tablename, url=self.url,
                                      cleanup=Cleanup(correct_invalid_value, 
                                          {"nulls":self.nulls})
                                      )
        self.engine.insert_data_from_url(self.url)
        return self.engine
        
        
TEMPLATES = [
             ("Ecological Archives", EcologicalArchives())
             ]
