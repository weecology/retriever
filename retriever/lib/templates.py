"""Class models for dataset scripts from various locations. Scripts should
inherit from the most specific class available."""
from __future__ import print_function
from builtins import object
import os
import shutil
from retriever import DATA_DIR
from retriever.lib.models import *
from retriever.lib.tools import choose_engine


class Script(object):
    """This class represents a database toolkit script. Scripts should inherit
    from this class and execute their code in the download method."""

    def __init__(self, name="", description="", shortname="", urls=dict(),
                 tables=dict(), ref="", public=True, addendum=None, citation="Not currently available",
                 retriever_minimum_version="", version="", **kwargs):
        self.name = name
        self.shortname = shortname
        self.filename = __name__
        self.description = description
        self.urls = urls
        self.tables = tables
        self.ref = ref
        self.public = public
        self.addendum = addendum
        self.citation = citation
        self.tags = []
        self.retriever_minimum_version = retriever_minimum_version
        self.version = version
        for key, item in list(kwargs.items()):
            setattr(self, key, item[0] if isinstance(item, tuple) else item)

    def __str__(self):
        desc = self.name
        if self.reference_url():
            desc += "\n" + self.reference_url()
        return desc

    def download(self, engine=None, debug=False):
        self.engine = self.checkengine(engine)
        self.engine.debug = debug
        self.engine.db_name = self.shortname
        self.engine.create_db()

    def reference_url(self):
        if self.ref:
            return self.ref
        else:
            if len(self.urls) == 1:
                return self.urls[list(self.urls.keys())[0]]
            else:
                return None

    def checkengine(self, engine=None):
        if engine is None:
            opts = {}
            engine = choose_engine(opts)
        engine.get_input()
        engine.script = self
        return engine

    def exists(self, engine=None):
        if engine:
            return engine.exists(self)
        else:
            return False

    def matches_terms(self, terms):
        try:
            search_string = ' '.join([
                    self.name,
                    self.description,
                    self.shortname
                ] + self.tags).upper()

            for term in terms:
                if not term.upper() in search_string:
                    return False
            return True
        except:
            return False


class BasicTextTemplate(Script):
    """Script template based on data files from Ecological Archives."""

    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        for key in list(self.urls.keys()):
            if key not in list(self.tables.keys()):
                self.tables[key] = Table(key, cleanup=Cleanup(correct_invalid_value,
                                                              nulls=[-999]))

        for key, value in list(self.urls.items()):
            self.engine.auto_create_table(self.tables[key], url=value)
            self.engine.insert_data_from_url(value)
            self.tables[key].record_id = 0
        return self.engine

    def reference_url(self):
        if self.ref:
            return self.ref
        else:
            if len(self.urls) == 1:
                return '/'.join(self.urls[list(self.urls.keys())[0]].split('/')[0:-1]) + '/'


class DownloadOnlyTemplate(Script):
    """Script template for non-tabular data that are only for download"""

    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)

    def download(self, engine=None, debug=False):
        if engine.name != "Download Only":
            raise Exception("This dataset contains only non-tabular data files, and can only be used with the 'download only' engine.\nTry 'retriever download datasetname instead.")
        Script.download(self, engine, debug)

        for filename, url in self.urls.items():
            self.engine.download_file(url, filename)
            if os.path.exists(self.engine.format_filename(filename)):
                shutil.copy(self.engine.format_filename(filename), DATA_DIR)
            else:
                print("{} was not downloaded".format(filename))
                print("A file with the same name may be in your working directory")


class HtmlTableTemplate(Script):
    """Script template for parsing data in HTML tables"""
    pass


TEMPLATES = [
    ("Basic Text", BasicTextTemplate),
    ("HTML Table", HtmlTableTemplate),
]
