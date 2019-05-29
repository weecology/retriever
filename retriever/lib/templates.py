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
                 version="", encoding="utf-8", message="", **kwargs):

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
        if len(self.urls) == 1:
            return self.urls[list(self.urls.keys())[0]]
        return None

    def checkengine(self, engine=None):
        """Returns the required engine instance"""
        if engine is None:
            opts = {}
            engine = choose_engine(opts)
        engine.get_input()
        engine.script = self
        engine.set_engine_encoding()
        return engine

    def matches_terms(self, terms):
        try:
            search_string = ' '.join([self.name,
                                      self.description,
                                      self.name] + self.keywords).upper()

            for term in terms:
                if not term.upper() in search_string:
                    return False
            return True
        except BaseException:
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

        for _, table_obj in self.tables.items():
            # if the table has no url, use the script's url
            if hasattr(table_obj, "url") and table_obj.url:
                url = table_obj.url
            elif self.url:
                url = self.url

            # Extract compressed source files
            if hasattr(self, "archived"):
                self.process_archived_data(table_obj, url)

            # Create tables
            if hasattr(table_obj, "format") and table_obj.format == "tabular":
                self.process_tables(table_obj, url)
            elif hasattr(self.engine, "spatial_support"):
                if self.engine.spatial_support:
                    self.process_tables(table_obj, url)
                else:
                    print("Engine {eng} does not support spatial "
                          "processing".format(eng=self.engine.name))
                    return

            # insert data procedures
            if hasattr(table_obj, "dataset_type"):
                if table_obj.dataset_type in ["RasterDataset", "VectorDataset"]:
                    self.process_spatial_insert(table_obj)
                    continue

                # assume tabular
                self.process_tabular_insert(table_obj, url)
            self.engine.disconnect_files()

    def process_tabular_insert(self, table_obj, url):
        if hasattr(self, "archived"):
            self.engine.insert_data_from_file(
                self.engine.format_filename(table_obj.path))
        else:
            self.engine.insert_data_from_url(url)

    def process_spatial_insert(self, table_obj):
        if table_obj.dataset_type == "RasterDataset":
            self.engine.insert_raster(self.engine.format_filename(table_obj.path))
        elif table_obj.dataset_type == "VectorDataset":
            self.engine.insert_vector(self.engine.format_filename(table_obj.path))

    def process_tables(self, table_obj, url):
        if hasattr(self, "archived"):
            self.engine.auto_create_table(table_obj, filename=table_obj.path)
        else:
            self.engine.auto_create_table(table_obj, url=url)

    def process_archived_data(self, table_obj, url):
        """Pre-process archived files.

        Extract the files from the archived source based on
        the specifications. Either extact a single file or the
        entire files.
        """
        archive_type = self.archived
        keep_in_dir = False
        archive_name = None

        if hasattr(self, "extract_all"):
            if self.extract_all:
                files = None
        else:
            files = [table_obj.path]
        if hasattr(self, "keep_in_dir"):
            keep_in_dir = self.keep_in_dir
        if hasattr(self, "archive_name"):
            archive_name = self.archive_name

        self.engine.download_files_from_archive(url=url, file_names=files,
                                                archive_type=archive_type,
                                                keep_in_dir=keep_in_dir,
                                                archive_name=archive_name)


class HtmlTableTemplate(Script):
    """Script template for parsing data in HTML tables."""

    pass


TEMPLATES = {
    "default": BasicTextTemplate,
    "html_table": HtmlTableTemplate
}
