"""Raw data cleanup library
A series of functions to aid in common clean up tasks of ecological databases

MySQL Empty Value Replacement
MySQL replaces empty values in imported files with zeros when the column is
numeric. This script takes a delimited text file as input and replaces all of
the empty values with MySQL's NULL indicator /N.

"""

# TO DO - write tests

def correct_invalid_value(datain, db, table):
    try:
        if set([datain]).issubset(table.nullindicators):            
            return None
        else:
            return datain
    except ValueError:
        return datain