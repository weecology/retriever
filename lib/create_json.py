from __future__ import print_function
from builtins import input
import os
import json
# JSON_SCRIPTS_DIR = "../scripts/"
JSON_SCRIPTS_DIR = ""

def create_datapackage_json():

    contents = {}

    contents['title'] = input("Title/Name: ")
    contents['name'] = input("Shortname (unique identifier for script0: ")
    contents['description'] = input("Description: ")
    contents['citation'] = input("Citation: ")
    contents['homepage'] = input("Site/Homepage of dataset: ")
    contents['keywords'] = input("Tags (separated by commas): ")
    contents['resources'] = []

    #Add tables -
    while True:
        addTable = input("\nAdd Table? (y/N): ")
        if addTable.lower() in ["n", "no"]:
            break
        elif addTable.lower() not in ["y", "yes"]:
            print("Not a valid option\n")
            continue
        else:
            table = {}

            table['name'] = input("Table name: ")


            table['dialect'] = {}
            d_opts = ['nulls (separated by \';\')',                 #list of str
             'replace_columns (separated by \';\')',                #list of tuples
             'delimiter',                                           #str
             'do_not_bulk_insert (bool = True/False)',              #bool
             'contains_pk (bool = True/False)',                     #bool
             'escape_single_quotes (bool = True/False)',            #bool
             'header_rows (int)']                                   #int

            for i in range(0, len(d_opts)):
                val = input(d_opts[i]+": ")
                key = [k.strip() for k in d_opts[i].split(" ")][0]

                if val != "":

                    if i<3:
                        while True:
                            if val == "":       #User wants to skip
                                break

                            values = [v.strip() for v in val.split(";")]
                            values = [v for v in values if v!=""]

                            if len(values) == 0:
                                print("Empty list. Try again\n")
                                val = input(d_opts[i]+": ")
                                continue

                            for i in range(0,len(values)):
                                try:
                                    values[i] = eval(values[i])
                                except:
                                    values[i] = str(values[i])

                            if len(values) == 1:
                                table['dialect'][key] = values[0]           # not a list type for a single value (bool,int, etc)
                            else:
                                table['dialect'][key] = values
                            break

                    elif i<6:
                        while True:
                            try:
                                if val == "":       #User wants to skip
                                    break
                                elif type(eval(val)) == bool:
                                    table['dialect'][key] = val
                                    break
                                else:
                                    print("\nWrong type. Either leave blank or try again.\n")
                            except:
                                print("Exception occured. Try Again.\n")
                                val = input(d_opts[i]+": ")

                    else:
                        while True:
                            try:
                                if val == "":       #User wants to skip
                                    break
                                elif type(eval(val)) == int:
                                    table['dialect'][key] = val
                                    break
                                else:
                                    print("\nWrong type. Either leave blank or try again.\n")
                            except:
                                print("Exception occured. Try Again.\n")
                                val = input(d_opts[i]+": ")


            table['schema'] = {}
            table['schema']["fields"] = []
            print("Enter columns [format = name, type, (optional) size]:\n")
            col = input()
            while col != "":
                try:
                    col_list = [c.strip() for c in col.split(",")]
                    col_list = [v for v in col_list if v!=""]

                    col_obj = {}
                    col_obj["name"] = col_list[0]
                    col_obj["type"] = col_list[1]

                    if len(col_list) > 2:
                        if type(eval(col_list[2])) != int:
                            raise
                        col_obj["size"] = col_list[2]
                    table["schema"]["fields"].append(col_obj)

                except:
                    print("Exception occured. Check the input format again.\n")
                    pass

                col = input()


            isCT = input("Add crosstab columns? (y,N): ")
            if isCT.lower() in ["y", "Y"]:
                ct_column = input("Crosstab column name: ")
                while ct_column == "":
                    print("Empty column name. Try again.\n")
                    ct_column = input("Crosstab column name: ")
                ct_names = []
                print("Enter names of crosstab column values (Press return after each name)")
                name = input()
                while name != "":
                    ct_names.append(name)
                    name = input()

                table['schema']['ct_column'] = ct_column
                table['schema']['ct_names'] = ct_names

            contents['resources'].append(table)

    file_name = contents['name'] + ".json"
    with open(JSON_SCRIPTS_DIR + file_name, 'w') as output_file:
        json.dump(contents, output_file, sort_keys=True, indent=4,
            separators=(',', ': '))
        output_file.write('\n')
        print("\nScript written to "+file_name)
        output_file.close()
