from __future__ import print_function
from builtins import input
import os
import json
import yaml
from time import sleep
JSON_SCRIPTS_DIR = "scripts/"
NEW_JSON_SCRIPTS_DIR = "json_scripts/"

def create_json():

    contents = {}

    contents['title'] = input("Title/Name: ")
    contents['name'] = input("Shortname (unique identifier for script: ")
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


def edit_dict(obj, tabwidth=0):

    for (key, val) in obj.items():
        print('\n'+"  "*tabwidth+"->"+key+" : \n")
        if type(val) == list:
            for v in val:
                print("  "*tabwidth+str(v)+'\n')
        elif type(val) == dict:
            for item in val.items():
                print("  "*tabwidth+str(item)+'\n')
        else:
            print("  "*tabwidth+str(val)+'\n')

        while True:
            try:
                if isinstance(val,dict):
                    print("\n\t'"+key+"' has the following keys:\n"+str(obj[key].keys())+"\n")
                    do_edit = input("Edit the values for these sub-keys of "+key+"? (y/N): ")

                    if do_edit.lower() in ['y', 'yes']:
                        edit_dict(obj[key], tabwidth+1)

                    print("Select one of the following for the key '"+key+"': \n")
                    print("1. Add an item")
                    print("2. Modify an item")
                    print("3. Delete an item")
                    print("4. Remove from script")
                    print("5. Continue (no changes)\n")

                    selection = input("\nYour choice: ")

                    if selection == '1':
                        add_key = input('Enter new key: ')
                        add_val = input('Enter new value: ')
                        obj[key][add_key] = add_val

                    elif selection == '2':
                        mod_key = input('Enter the key: ')
                        if mod_key not in val:
                            raise Exception("Invalid input! Key not found.")
                        mod_val = input('Enter new value: ')
                        obj[key][mod_key] = mod_val

                    elif selection == '3':
                        del_key = input('Enter key to be deleted: ')
                        if del_key not in val:
                            print("Invalid key: Not found")
                            continue
                        print("Removed "+str(del_key) + " : " + str(obj[key].pop(del_key)))

                    elif selection == '4':
                        do_remove = input("Are you sure (Yes, completely remove this entry)? (y/n): ")
                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed "+key+" from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)
                    elif selection == '5' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")

                elif isinstance(val,list):

                    for i in range(len(val)):
                        print(str(val[i]))
                        if isinstance(val[i], dict):
                            print("\n\t'"+key+"' has the following dict:\n"+str(val[i])+"\n")
                            do_edit = input("Edit the dict in '"+key+"'? (y/N): ")

                            if do_edit.lower() in ['y', 'yes']:
                                edit_dict(obj[key][i], tabwidth+2)

                    print("Select one of the following for the key '"+key+"': \n")
                    print("1. Add an item")
                    print("2. Delete an item")
                    print("3. Remove from script")
                    print("4. Continue (no changes)\n")

                    selection = input("\nYour choice: ")

                    if selection == '1':
                        add_val = input('Enter new value: ')
                        obj[key].append(add_val)

                    elif selection == '2':
                        del_val = input('Enter value to be deleted: ')
                        print("Removed "+str(obj[key].pop(del_key)))

                    elif selection == '3':
                        do_remove = input("Are you sure (Yes, completely remove this entry)? (y/n): ")
                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed "+key+" from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)

                    elif selection == '4' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")


                else:
                    print("Select one of the following for the key '"+key+"': \n")
                    print("1. Modify value")
                    print("2. Remove from script")
                    print("3. Continue (no changes)\n")

                    selection = input("\nYour choice: ")

                    if selection == '1':
                        new_val = input('Enter new value: ')
                        obj[key] = new_val

                    elif selection == '2':
                        do_remove = input("Are you sure (Yes, completely remove this entry)? (y/n): ")
                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed "+key+" from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)
                    elif selection == '3' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")
                break
            except RuntimeError:
                continue


def edit_json(json_file):

    contents = yaml.load(open(JSON_SCRIPTS_DIR+json_file+'.json','r'))
    edit_dict(contents, 1)

    file_name = contents['name'] + ".json"
    with open(NEW_JSON_SCRIPTS_DIR + file_name, 'w') as output_file:
        json.dump(contents, output_file, sort_keys=True, indent=4,
            separators=(',', ': '))
        output_file.write('\n')
        print("\nScript written to "+file_name)
        output_file.close()

