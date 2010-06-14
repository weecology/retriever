# Raw data cleanup library
# A series of functions to aid in common clean up tasks of ecological databases

# MySQL Empty Value Replacement
# MySQL replaces empty values in imported files with zeros when the column is
# numeric. This script takes a delimited text file as input and replaces all of
# the empty values with MySQL's NULL indicator /N.

# TO DO - add ability to select delimitor other than commas

def emptyvaltonull(infile, outfile):
    input_file = open(infile, 'r')
    output_file = open(outfile, 'w')

    line = input_file.readline()
    while line:
        if line[0] == ',':
            line = '\N'+line
        while line.find(",,") != -1:	
            line = line.replace(",,", ",\N,")
        output_file.write(line)
        line = input_file.readline()
    
    input_file.close()
    output_file.close()