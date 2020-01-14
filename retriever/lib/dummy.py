"""Dummy connection classes for connectionless engine instances

This module contains dummy classes required for non-db based children of the Engine class.
"""


class DummyConnection():
    """Dummy connection class"""

    def cursor(self):
        """Dummy cursor function"""

    def commit(self):
        """Dummy commit"""

    def rollback(self):
        """Dummy rollback"""

    def close(self):
        """Dummy close connection"""


class DummyCursor(DummyConnection):
    """Dummy connection cursor"""
