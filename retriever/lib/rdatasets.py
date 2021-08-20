import os
import json
import pandas as pd
from retriever import lscolumns

from retriever.lib.templates import BasicTextTemplate
from retriever.lib.defaults import RDATASETS_URL, RDATASET_PATH, RDATASET_SCRIPT_WRITE_PATH
from retriever.lib.create_scripts import create_package
from retriever.lib.scripts import reload_scripts


def update_rdataset_catalog(test=False):
    '''Updates the datasets_url.json from the github repo'''
    if not os.path.exists(RDATASET_SCRIPT_WRITE_PATH):
        os.makedirs(RDATASET_SCRIPT_WRITE_PATH)

    df = pd.read_csv(RDATASETS_URL)
    dataset_url = {}

    for i in range(len(df)):
        if df['Package'][i].lower() not in dataset_url.keys():
            dataset_url[df['Package'][i].lower()] = {}

        dataset_url[df['Package'][i].lower()][df['Item'][i].lower()] = {
            'csv': df['CSV'][i],
            'doc': df['Doc'][i],
            'title': df['Title'][i],
        }
    # for testing update_rdataset_catalog
    if test:
        return dataset_url
    else:
        json_data = dataset_url
        with open(RDATASET_PATH, 'w') as f:
            json.dump(json_data, f, sort_keys=True, indent=4)
        f.close()


def create_rdataset(engine, package, dataset_name, script_path=None):
    """Download files for RDatasets to the raw data directory"""
    if script_path is None:
        script_path = RDATASET_SCRIPT_WRITE_PATH

    update_rdataset_catalog()

    with open(RDATASET_PATH, 'r') as f:
        rdatasets = json.load(f)
    f.close()

    try:
        rpackage = rdatasets[package]
        try:
            data_obj = rpackage[dataset_name]
        except KeyError:
            print("Dataset '{}' not found in package '{}' RDatasets".format(
                dataset_name, package))
    except KeyError:
        print("Package '{}' not found in RDatasets".format(package))

    script_name = f"rdataset-{package}-{dataset_name}"
    filename = data_obj['csv'].split('/')[-1]
    engine.script = BasicTextTemplate(**{"name": script_name})

    if not engine.find_file(filename) or not engine.use_cache:
        engine.download_file(data_obj['csv'], filename)

    path = engine.format_filename(filename)
    engine.script = None

    if engine.opts["command"] == "download":
        engine.final_cleanup()
        return
    else:
        create_package(path, 'tabular', True, script_path)
        print("Updating script name to {}".format(script_name + ".json"))
        print("Updating the contents of script {}".format(script_name))
        update_rdataset_script(data_obj, dataset_name, package, script_path)
        print("Updated the script {}".format(script_name))
        reload_scripts()


def update_rdataset_script(data_obj, dataset_name, package, script_path):
    """Renames and updates the RDataset script"""
    filename = dataset_name + '.csv.json'
    script_filename = f"rdataset_{package}_{dataset_name}" + '.json'

    if filename in [
            file_i for file_i in os.listdir(script_path) if file_i.endswith(".json")
    ]:
        os.rename(f"{script_path}/{filename}", f"{script_path}/{script_filename}")
        with open(f"{script_path}/{script_filename}", "r") as f:
            json_file = json.load(f)
        f.close()

        result, json_file = update_rdataset_contents(data_obj, package, dataset_name,
                                                     json_file)

        if result:
            json_obj = json.dumps(json_file, sort_keys=True, indent=4)

            with open(f"{script_path}/{script_filename}", 'w') as f:
                f.write(json_obj)
            f.close()

            print("Successfully updated {}".format(script_filename))
        else:
            print(f"Could not update {script_filename} with the given data_obj")
    else:
        print("File {filename} does not exist in path {script_path}".format(
            filename=filename, script_path=script_path))


def update_rdataset_contents(data_obj, package, dataset_name, json_file):
    """Update the contents of json script"""
    if "archived" in json_file.keys():
        json_file.pop("archived")

    if ("resources" in json_file.keys()) and (len(json_file["resources"]) != 0) and (
            "path" in json_file["resources"][0].keys()):
        json_file["resources"][0].pop("path")

    keys = ['csv', 'doc', 'title']
    flag = True
    for key in keys:
        if key not in data_obj:
            flag = False
            break

    if flag:
        json_file["description"] = f"This is a rdataset from {package}"
        json_file["homepage"] = data_obj['doc']
        json_file["licenses"] = [{"name": "Public Domain"}]
        json_file["keywords"] = ['rdataset', f'{dataset_name}', f'{package}']
        json_file["name"] = f"rdataset-{package}-{dataset_name}"
        json_file["resources"][0]["url"] = data_obj['csv']
        json_file["rdatasets"] = "True"
        json_file["title"] = data_obj["title"]
        json_file["citation"] = ""
        json_file["package"] = package
        json_file["retriever_minimum_version"] = "3.0.1-dev"

        return True, json_file
    else:
        return False, None


def display_all_rdataset_names(package_name=None):
    """displays the list of rdataset names present in the package(s) provided"""
    update_rdataset_catalog()

    with open(RDATASET_PATH, 'r') as f:
        rdatasets = json.load(f)
    f.close()

    if not package_name:
        print("List of all available Rdatasets\n")
        for package in rdatasets.keys():
            for dataset in rdatasets[package].keys():
                script_name = f"rdataset-{package}-{dataset}"
                print(
                    f"Package: {package:<16} Dataset: {dataset:<25} Script Name: {script_name:<10}"
                )

    elif package_name == 'all':
        print("List of all the packages present in Rdatasets\n")
        packages = [(package, True) for package in rdatasets.keys()]
        lscolumns.printls(packages)

    else:
        print(f"List of all available Rdatasets in packages: {package_name}")
        for package in package_name:
            try:
                dataset_names = rdatasets[package].keys()
                for dataset in dataset_names:
                    script_name = f"rdataset-{package}-{dataset}"
                    print(
                        f"Package: {package:<16} Dataset: {dataset:<25} Script Name: {script_name:<10}"
                    )
            except KeyError:
                print(f"No package named \'{package}\' found in Rdatasets")


def get_rdataset_names():
    """returns a list of all the available RDataset names present"""
    update_rdataset_catalog()

    with open(RDATASET_PATH, 'r') as f:
        rdatasets = json.load(f)
    f.close()

    scripts = []
    for package in rdatasets.keys():
        for dataset in rdatasets[package].keys():
            script_name = f"rdataset-{package}-{dataset}"
            scripts.append(script_name)

    return sorted(scripts)
