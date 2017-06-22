"""Data Retriever

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""
from .lib import *
from retriever.lib.tools import set_proxy, create_dir


create_dir()
set_proxy()
