from __future__ import print_function
from builtins import input
import os
import json
from time import sleep
from retriever import SCRIPT_LIST, HOME_DIR

short_names = [script.shortname.lower() for script in SCRIPT_LIST()]


def is_empty(val):
    """Check if a variable is an empty string or an empty list"""
    return val == "" or val == []


def clean_input(prompt="", split_char='', ignore_empty=False, dtype=None):
    """Clean the user-input from the CLI before adding it"""
    while True:
        val = input(prompt).strip()
        # split to list type if split_char specified
        if split_char != "":
            val = [v.strip() for v in val.split(split_char) if v.strip() != ""]
        # do not ignore empty input if not allowed
        if not ignore_empty and is_empty(val):
            print("\tError: empty input. Need one or more values.\n")
            continue
        # ensure correct input datatype if specified
        if not is_empty(val) and dtype is not None:
            try:
                if not type(eval(val)) == dtype:
                    print("\tError: input doesn't match required type ", dtype, "\n")
                    continue
            except:
                print("\tError: illegal argument. Input type should be ", dtype, "\n")
                continue
        break
    return val


def get_replace_columns(dialect):
    """Get list of tuples with old and new names for the columns in the table"""
    val = clean_input("replace_columns (separated by ';', with comma-separated values) (press return to skip): ",
                      split_char=';', ignore_empty=True)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['replace_columns'] = []
    for v in val:
        try:
            pair = v.split(',')
            dialect['replace_columns'].append((pair[0].strip(), pair[1].strip()))
        except IndexError:
            continue


def get_nulls(dialect):
    """Get list of strings that denote null in the dataset"""
    val = clean_input("nulls (separated by ';') (press return to skip): ",
                      split_char=';', ignore_empty=True)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['nulls'] = val
    # change list to single value if size == 1
    if len(dialect['nulls']) == 1:
        dialect['nulls'] = dialect['nulls'][0]


def get_delimiter(dialect):
    """Get the string delimiter for the dataset file(s)"""
    val = clean_input("delimiter (press return to skip): ", ignore_empty=True)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['delimiter'] = val


def get_do_not_bulk_insert(dialect):
    """Set do_not_bulk_insert property"""
    val = clean_input("do_not_bulk_insert (bool = True/False) (press return to skip): ",
                      ignore_empty=True, dtype=bool)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['do_not_bulk_insert'] = val


def get_contains_pk(dialect):
    """Set contains_pk property"""
    val = clean_input("contains_pk (bool = True/False) (press return to skip): ",
                      ignore_empty=True, dtype=bool)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['contains_pk'] = val


def get_escape_single_quotes(dialect):
    """Set escape_single_quotes property"""
    val = clean_input("escape_single_quotes (bool = True/False) (press return to skip): ",
                      ignore_empty=True, dtype=bool)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['escape_single_quotes'] = val


def get_escape_double_quotes(dialect):
    """Set escape_double_quotes property"""
    val = clean_input("escape_double_quotes (bool = True/False) (press return to skip): ",
                      ignore_empty=True, dtype=bool)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['escape_double_quotes'] = val


def get_fixed_width(dialect):
    """Set fixed_width property"""
    val = clean_input("fixed_width (bool = True/False) (press return to skip): ",
                      ignore_empty=True, dtype=bool)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['fixed_width'] = val


def get_header_rows(dialect):
    """Get number of rows considered as the header"""
    val = clean_input("header_rows (int) (press return to skip): ",
                      ignore_empty=True, dtype=int)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['header_rows'] = val


def create_json():
    '''
    Creates datapackage.JSON script.
    http://specs.frictionlessdata.io/data-packages/#descriptor-datapackagejson
    Takes input from user via command line.

    Usage: retriever create_json
    '''
    contents = {}
    tableUrls = {}

    script_exists = True
    while script_exists:
        contents['name'] = clean_input("name (a short unique identifier; only lowercase letters and - allowed): ")
        script_exists = contents['name'].lower() in short_names
        if script_exists:
            print("Dataset already available. Check the list or try a different shortname")

    contents['title'] = clean_input("title: ", ignore_empty=True)
    contents['description'] = clean_input("description: ", ignore_empty=True)
    contents['citation'] = clean_input("citation: ", ignore_empty=True)
    contents['homepage'] = clean_input("homepage (for the entire dataset): ", ignore_empty=True)
    contents['keywords'] = clean_input("keywords (separated by ';'): ",
                                        split_char=';', ignore_empty=True)
    contents['resources'] = []
    contents['retriever'] = "True"
    contents['retriever_minimum_version'] = "2.0.dev"
    contents['version'] = "1.0.0";

    # Add tables -
    while True:
        addTable = clean_input("\nAdd Table? (y/N): ")
        if addTable.lower() in ["n", "no"]:
            break
        elif addTable.lower() not in ["y", "yes"]:
            print("Not a valid option\n")
            continue
        else:
            table = {}
            table['name'] = clean_input("table-name: ")
            table['url'] = clean_input("table-url: ")
            table['dialect'] = {}
            tableUrls[table['name']] = table['url']

            # get table properties (dialect)
            # refer retriever.lib.table.Table
            get_replace_columns(table['dialect'])
            get_nulls(table['dialect'])
            get_delimiter(table['dialect'])
            get_do_not_bulk_insert(table['dialect'])
            get_contains_pk(table['dialect'])
            get_escape_single_quotes(table['dialect'])
            get_escape_double_quotes(table['dialect'])
            get_fixed_width(table['dialect'])
            get_header_rows(table['dialect'])

            # set table schema
            table['schema'] = {}
            table['schema']["fields"] = []
            print("Enter columns [format = name, type, (optional) size] (press return to skip):\n\n")
            while True:
                # get column list (optional)
                try:
                    col_list = clean_input("", split_char = ',', ignore_empty = True)
                    if col_list == []:
                        break
                    elif type(col_list) != list:
                        raise Exception

                    col_list = [c.strip() for c in col_list]
                    col_obj = {}    # dict to store column data
                    col_obj["name"] = col_list[0]
                    col_obj["type"] = col_list[1]

                    if len(col_list) > 2:
                        if type(eval(col_list[2])) != int:
                            raise Exception
                        col_obj["size"] = col_list[2]
                    table["schema"]["fields"].append(col_obj)
                except:
                    print("Exception occured. Check the input format again.\n")
                    pass

            isCT = clean_input(
                "Add crosstab columns? (y,N): ", ignore_empty=True)
            if isCT.lower() in ["y", "yes"]:
                ct_column = clean_input("Crosstab column name: ")
                ct_names = []
                print("Enter names of crosstab column values (Press return after each name):\n")
                name = clean_input()
                while name != "":
                    ct_names.append(name)
                    name = clean_input()

                table['schema']['ct_column'] = ct_column
                table['schema']['ct_names'] = ct_names

            contents['resources'].append(table)  
    contents['urls'] = tableUrls
    file_name = contents['name'] + ".json"
    with open(os.path.join(HOME_DIR, 'scripts', file_name), 'w') as output_file:
        json_str = json.dumps(contents, output_file, sort_keys=True, indent=4,
                              separators=(',', ': '))
        output_file.write(json_str + '\n')
        print("\nScript written to " + file_name)
        output_file.close()


def edit_dict(obj, tabwidth=0):
    '''
    Recursive helper function for edit_json() to edit a datapackage.JSON script file.
    '''
    for (key, val) in obj.items():
        print('\n' + "  " * tabwidth + "->" + key + " (", type(val), ") :\n")
        if type(val) == list:
            for v in val:
                print("  " * tabwidth + str(v) + '\n\n')
        elif type(val) == dict:
            for item in val.items():
                print("  " * tabwidth + str(item) + '\n\n')
        else:
            print("  " * tabwidth + str(val) + '\n\n')

        while True:
            try:
                if isinstance(val, dict):
                    if val != {}:
                        print("    '" + key + "' has the following keys:\n" +
                              str(obj[key].keys()) + "\n")
                        do_edit = clean_input(
                            "Edit the values for these sub-keys of " + key + "? (y/N): ")

                        if do_edit.lower() in ['y', 'yes']:
                            edit_dict(obj[key], tabwidth + 1)

                    print("Select one of the following for the key '" + key + "': \n")
                    print("1. Add an item")
                    print("2. Modify an item")
                    print("3. Delete an item")
                    print("4. Remove from script")
                    print("5. Continue (no changes)\n")

                    selection = clean_input("\nYour choice: ")

                    if selection == '1':
                        add_key = clean_input('Enter new key: ')
                        add_val = clean_input('Enter new value: ')
                        obj[key][add_key] = add_val

                    elif selection == '2':
                        mod_key = clean_input('Enter the key: ')
                        if mod_key not in val:
                            print("Invalid input! Key not found.")
                            continue
                        mod_val = clean_input('Enter new value: ')
                        obj[key][mod_key] = mod_val

                    elif selection == '3':
                        del_key = clean_input('Enter key to be deleted: ')
                        if del_key not in val:
                            print("Invalid key: Not found")
                            continue
                        print("Removed " + str(del_key) +
                              " : " + str(obj[key].pop(del_key)))

                    elif selection == '4':
                        do_remove = clean_input(
                            "Are you sure (completely remove this entry)? (y/n): ")

                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed " + key + " from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)
                    elif selection == '5' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")

                elif isinstance(val, list):

                    for i in range(len(val)):
                        print(i + 1, '. ', str(val[i]))
                        if isinstance(val[i], dict):
                            do_edit = clean_input(
                                "\nEdit this dict in '" + key + "'? (y/N): ")

                            if do_edit.lower() in ['y', 'yes']:
                                edit_dict(obj[key][i], tabwidth + 2)

                    print("Select one of the following for the key '" + key + "': \n")
                    print("1. Add an item")
                    print("2. Delete an item")
                    print("3. Remove from script")
                    print("4. Continue (no changes)\n")

                    selection = clean_input("\nYour choice: ")

                    if selection == '1':
                        add_val = clean_input('Enter new value: ')
                        obj[key].append(add_val)

                    elif selection == '2':
                        del_val = clean_input('Enter value to be deleted: ')

                        if del_val not in obj[key]:
                            print("Invalid value: Not found.")
                            continue
                        print("Removed " + str(obj[key].pop(del_key)))

                    elif selection == '3':
                        do_remove = clean_input(
                            "Are you sure (completely remove this entry)? (y/n): ")

                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed " + key + " from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)

                    elif selection == '4' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")

                else:
                    print("Select one of the following for the key '" + key + "': \n")
                    print("1. Modify value")
                    print("2. Remove from script")
                    print("3. Continue (no changes)\n")

                    selection = clean_input("\nYour choice: ")

                    if selection == '1':
                        new_val = clean_input('Enter new value: ')
                        obj[key] = new_val

                    elif selection == '2':
                        do_remove = clean_input(
                            "Are you sure (completely remove this entry)? (y/n): ")

                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed " + key + " from script.\n")
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
    '''
    Edits existing datapackage.JSON script.

    Usage: retriever edit_json <script_name>
    Note: Name of script is the dataset shortname.
    '''
    try:
        contents = json.load(
            open(os.path.join(HOME_DIR, 'scripts', json_file), 'r'))
    except FileNotFoundError:
        print("Script not found.")
        return

    edit_dict(contents, 1)

    file_name = contents['name'] + ".json"
    with open(os.path.join(HOME_DIR, 'scripts', file_name), 'w') as output_file:
        json_str = json.dumps(contents, output_file, sort_keys=True, indent=4,
                              separators=(',', ': '))
        output_file.write(json_str + '\n')
        print("\nScript written to " +
              os.path.join(HOME_DIR, 'scripts', file_name))
        output_file.close()
