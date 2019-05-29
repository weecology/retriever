"""Module to create scripts"""
import collections
import os
import json

from retriever.lib.engine import Engine
from retriever.lib.models import Table
from retriever.lib.datapackage import clean_input
from retriever.lib.tools import open_fw


def get_directory(path):
    """Returns absolute directory path for a path."""
    path = os.path.expanduser(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def create_package(path, data_type, file_flag, out_path, skip_lines=None):
    """Creates package for a path

    path: string path to files to be processed
    data_type: string data type of the files to be processed
    file_flag: boolean for whether the files are processed as files or directories
    out_path: string path to write scripts out to
    skip_lines: int number of lines to skip
    """
    path = os.path.expanduser(os.path.normpath(path))
    skip_lines = skip_lines[0] if skip_lines else 1
    if not os.path.exists(path):
        print("Please enter a valid path.")
        return

    if not out_path and out_path == "":
        out_path = os.path.join(get_directory(path), "scripts")

    if data_type.lower() == "vector":
        create_vector_datapackage()
    elif data_type.lower() == "raster":
        create_raster_datapackage()
    elif data_type.lower() == "tabular":
        create_tabular_datapackage(path, file_flag, out_path, skip_lines)


def create_raster_datapackage():
    """Creates raster package for a path"""
    pass


def create_tabular_datapackage(path, file_flag, out_path, skip_lines):
    """Creates tabular package for a path"""
    if file_flag:
        process_singles(path, out_path, skip_lines)
    else:
        process_dirs(path, out_path, skip_lines)


def create_vector_datapackage():
    """Creates vector package for a path"""
    pass


def create_resources(file, skip_lines):
    """Creates resources for the script or errors out if not possible"""
    engine = Engine()
    table = engine.auto_create_table(
        Table(str(file), header_rows=skip_lines), filename=file, make=False
    )
    clean_table = table.__dict__
    resource_dict = {}
    path_to_table = os.path.basename(clean_table["name"])
    resource_dict["name"] = os.path.splitext(path_to_table)[0]
    resource_dict["schema"] = {}
    resource_dict["dialect"] = {}
    resource_dict["schema"]["fields"] = []
    for cname, ctuple in clean_table["columns"]:
        resource_dict["schema"]["fields"].append({"name": cname, "type": ctuple[0]})
    resource_dict["url"] = "FILL"
    return resource_dict


def create_script_dict(allpacks, path, file, skip_lines):
    """Create script dict or skips file if resources cannot be made"""
    allpacks["name"] = "FILL"
    allpacks["title"] = "FILL"
    allpacks["description"] = "FILL"
    allpacks["citation"] = "FILL"
    allpacks["licenses"] = [{"name": "FILL"}]
    allpacks["keywords"] = []
    allpacks["homepage"] = "FILL"
    allpacks["version"] = "1.0.0"
    try:
        resources = create_resources(os.path.join(path, file), skip_lines)
    except:
        print("Skipped file: " + file)
        return
    allpacks.setdefault("resources", []).append(resources)
    allpacks["retriever"] = "True"
    allpacks["retriever_minimum_version"] = "2.1.0"

    return allpacks


def process_dirs(sub_dirs_path, out_path, skip_lines):
    """Creates a script for each directory

    If there are subdirectories in a directory, a script is created for each
    subdirectory.
    If there are no subdirectories in a directory, a script is created for the
    directory with the resources being the files in the directory.
    If there are subdirectories and files in a directory, a script is created
    for each subdirectory, and a script is created for the main directory with
    the resources being the files in the directory.
    """
    for path, _, files in os.walk(sub_dirs_path):
        allpacks = collections.OrderedDict()
        for file_n in files:
            if file_n:
                try_create_dict = create_script_dict(allpacks, path, file_n, skip_lines)
                if try_create_dict:
                    allpacks = try_create_dict
        write_out_scripts(allpacks, path, out_path)


def process_singles(single_files_path, out_path, skip_lines):
    """Creates a script for each file

    If the filepath is a file, creates a single script for that file.
    If the filepath is a directory, creates a single script for each file in the
    directory.
    """
    if os.path.isdir(single_files_path):
        for path, _, files in os.walk(single_files_path):
            for file_n in files:
                allpacks = collections.OrderedDict()
                if file_n:
                    allpacks = create_script_dict(allpacks, path, file_n, skip_lines)
                    filepath = os.path.join(path, file_n)
                    write_out_scripts(allpacks, filepath, out_path)
    else:
        directory = os.path.dirname(single_files_path)
        file_name = os.path.basename(single_files_path)
        allpacks = collections.OrderedDict()
        allpacks = create_script_dict(allpacks, directory, file_name, skip_lines)
        write_out_scripts(allpacks, single_files_path, out_path)


def write_out_scripts(script_dict, path, out_path):
    """Writes scripts out to a given path"""
    file_name = os.path.basename(path).split(".")[0] + ".json"
    path_dir = get_directory(os.path.expanduser(path))
    if out_path is not None:
        path_dir = os.path.expanduser(out_path)
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
    write_path = os.path.join(path_dir, file_name)

    if not (script_dict and "resources" in script_dict):
        print(write_path + " creation skipped because resources were empty.")
        return
    if os.path.exists(write_path):
        choice = clean_input(
            write_path + " already exists. Overwrite the script? [y/n]"
        )
        if choice == "n":
            print(write_path + " creation skipped.")
            return
    try:
        with open_fw(write_path) as output_path:
            sourted_dict = collections.OrderedDict(sorted(script_dict.items()))
            jsonstr = json.dumps(sourted_dict, sort_keys=True, indent=4)
            output_path.write(jsonstr)
            print("Successfully wrote scripts to " + os.path.abspath(write_path))
            output_path.close()
    except Exception as e:
        print(write_path + " could not be created. {}".format(e.message))
