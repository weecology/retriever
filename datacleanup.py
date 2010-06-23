"""Raw data cleanup library
A series of functions to aid in common clean up tasks of ecological databases

MySQL Empty Value Replacement
MySQL replaces empty values in imported files with zeros when the column is
numeric. This script takes a delimited text file as input and replaces all of
the empty values with MySQL's NULL indicator /N.

"""

# TO DO - write tests

def emptyvaltonull(datain):
    """Convert empty fields in comma delimited text to MySQL NULL indicator /N
    
    Keyword arguments:
    datain = a list of strings where each string is one line of the datafile
              
    """
    # TO DO - test new implementation
    # TO DO - add ability to select delimiter other than commas

    dataout = [];
    line = datain.readline()
    while line:
        if line[0] == ',':
            line = '\N'+line
        while line.find(",,") != -1:	
            line = line.replace(",,", ",\N,")
        dataout.append(line)
        line = datain.readline()
    return dataout

def correct_invalid_value(datain):
    try:
        val = int(float(datain))        
        if val == -999:            
            return None
        else:
            return datain
    except ValueError:
        return datain