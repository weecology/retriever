"""Datasets are defined as scripts and have unique properties.
The Module defines generic dataset properties and models the
functions available for inheritance by the scripts or datasets.
"""
from __future__ import print_function

from retriever.engines import choose_engine
from retriever.lib.models import *


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
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def download(self, engine=None, debug=False):
        """Defines the download processes for scripts that utilize the default
        pre processing steps provided by the retriever."""
        Script.download(self, engine, debug)
        # make file name mandatory for simplicity

        for i_table, table_obj in self.tables.items():

            url = table_obj.url
            if hasattr(self, "archived"):
                files = [table_obj.path]
                archive_type = self.archived
                keep_in_dir = False
                archivename = None
                if hasattr(self, "keep_in_dir"):
                    keep_in_dir = self.keep_in_dir
                if hasattr(self, "archivename"):
                    archivename = self.archivename
                self.engine.download_files_from_archive(url=url,
                                                        filenames=files,
                                                        filetype=archive_type,
                                                        keep_in_dir=keep_in_dir,
                                                        archivename=archivename)
                self.engine.auto_create_table(table_obj, filename=table_obj.path)
                self.engine.insert_data_from_file(self.engine.format_filename(table_obj.path))
            else:
                self.engine.auto_create_table(table_obj, url=url)
                self.engine.insert_data_from_url(url)


class HtmlTableTemplate(Script):
    """Script template for parsing data in HTML tables."""

    pass


TEMPLATES = {
    "default": BasicTextTemplate,
    "html_table": HtmlTableTemplate
}
