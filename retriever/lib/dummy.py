"""Dummy connection classes for connectionless engine instances

This module contains dummy classes required for non-db based children of the Engine class.
"""


class DummyConnection(object):
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
