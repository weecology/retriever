"""Database Toolkit

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""

VERSION = '0.2'

scripts = [
           "bbs",
           "CRC_avianbodymass",
           "EA_avianbodysize2007",
           "EA_ernest2003",
           "EA_pantheria",
           "EA_portal_mammals",
           "gentry",
           ]
           
engines = [
           "mysql",
           "postgres",
           "sqlite",
           "msaccess",
           ]

def DBTK_LIST():    
    SCRIPT_MODULE_LIST = [
                          __import__("dbtk.scripts." + module, fromlist="scripts")
                          for module in scripts
                          ]

    return [module.main() for module in SCRIPT_MODULE_LIST]
    
def ENGINE_LIST():
    ENGINE_MODULE_LIST = [
                          __import__("dbtk.engines." + module, fromlist="engines")
                          for module in engines
                          ]
                          
    return [module.engine() for module in ENGINE_MODULE_LIST]
