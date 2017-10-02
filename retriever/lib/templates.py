"""Datasets are defined as scripts and have unique properties.
The Module defines generic dataset properties and models the
functions available for inheritance by the scripts or datasets.
"""
from __future__ import print_function

import shutil

from retriever.lib.models import *
from retriever.engines import choose_engine
from retriever.lib.defaults import DATA_DIR


class Script(object):
    """This class defines the properties of a generic dataset.

    Each Dataset inherits attributes from this class to define
    it's Unique functionality.
    """

    def __init__(self, title="", description="", name="", urls=dict(),
                 tables=dict(), ref="", public=True, addendum=None,
                 citation="Not currently available",
                 licenses=[{'name': None}],
                 retriever_minimum_version="",
                 version="", encoding="", message="", **kwargs):

        self.title = title
        self.name = name
        self.filename = __name__
        self.description = description
        self.urls = urls
        self.tables = tables
        self.ref = ref
        self.public = public
        self.addendum = addendum
        self.citation = citation
        self.licenses = licenses
        self.keywords = []
        self.retriever_minimum_version = retriever_minimum_version
        self.encoding = encoding
        self.version = version
        self.message = message
        for key, item in list(kwargs.items()):
            setattr(self, key, item[0] if isinstance(item, tuple) else item)

    def __str__(self):
        desc = self.name
        if self.reference_url():
            desc += "\n" + self.reference_url()
        return desc

    def download(self, engine=None, debug=False):
        """Generic function to prepare for installation or download."""
        self.engine = self.checkengine(engine)
        self.engine.debug = debug
        self.engine.db_name = self.name
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
        """Returns the required engine instance"""
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
            search_string = ' '.join([self.name,
                                      self.description,
                                      self.name] + self.keywords).upper()

            for term in terms:
                if not term.upper() in search_string:
                    return False
            return True
        except:
            return False


class BasicTextTemplate(Script):
    """Defines the pre processing required for scripts.

    Scripts that need pre processing should use the download function
    from this class.
    Scripts that require extra tune up, should override this class.
    """

    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)

    def download(self, engine=None, debug=False):
        """Defines the download processes for scripts that utilize the default
        pre processing steps provided by the retriever."""
        Script.download(self, engine, debug)

        for key in list(self.urls.keys()):
            if key not in list(self.tables.keys()):
                self.tables[key] = Table(key, cleanup=Cleanup(correct_invalid_value,
                                                              missing_values=[-999]))

        for key, value in list(self.urls.items()):
            self.engine.auto_create_table(self.tables[key], url=value)
            self.engine.insert_data_from_url(value)
            self.tables[key].record_id = 0
        self.print_message()
        return self.engine

    def reference_url(self):
        if self.ref:
            return self.ref
        else:
            if len(self.urls) == 1:
                return '/'.join(self.urls[list(self.urls.keys())[0]].split('/')[0:-1]) + '/'

    def print_message(self):
        if self.message:
            print(self.message)


class DownloadOnlyTemplate(Script):
    """Script template for non-tabular data that are only for download."""

    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)

    def download(self, engine=None, debug=False):
        if engine.name != "Download Only":
            raise Exception(
                "This dataset contains only non-tabular data files, "
                "and can only be used with the 'download only' engine."
                "\nTry 'retriever download [dataset name] instead.")
        Script.download(self, engine, debug)

        for filename, url in self.urls.items():
            self.engine.download_file(url, filename)
            if os.path.exists(self.engine.format_filename(filename)):
                shutil.copy(self.engine.format_filename(filename), DATA_DIR)
            else:
                print("{} was not downloaded".format(filename))
                print("A file with the same name may be in your working directory")


class HtmlTableTemplate(Script):
    """Script template for parsing data in HTML tables."""

    pass


TEMPLATES = [
    ("Basic Text", BasicTextTemplate),
    ("HTML Table", HtmlTableTemplate),
]
