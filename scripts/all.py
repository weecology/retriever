"""Importing MODULE_LIST from this module gives a list of all dataset scripts."""

__all__ = [
           "bbs",
           "CRC_avianbodymass",
           "EA_avianbodysize2007",
           "EA_ernest2003",
           "EA_pantheria",
           "EA_portal_mammals",
           "gentry",
           ]

MODULE_LIST = [
               __import__("scripts." + module, fromlist="scripts")
               for module in __all__
               ]