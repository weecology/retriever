import os
import json

import requests
from tqdm import tqdm
from urllib.error import HTTPError

from retriever.lib.create_scripts import create_package
from retriever.lib.defaults import SOCRATA_BASE_URL, SOCRATA_SCRIPT_WRITE_PATH
from retriever.lib.scripts import reload_scripts
from retriever.lib.templates import BasicTextTemplate


def url_response(url, params):
    """Returns the GET response for the given url and params"""
    return requests.get(
        url,
        params,
        headers={
            'user-agent':
                'Weecology/Data-Retriever Package Manager: http://www.data-retriever.org/'
        },
        allow_redirects=True)


def socrata_autocomplete_search(dataset):
    """Returns the list of dataset names after autocompletion"""
    names = []
    query = " ".join(dataset)
    url = SOCRATA_BASE_URL + '/autocomplete'
    params = {'q': query}
    try:
        response = url_response(url, params)

        if response.status_code == 404:
            print("Socrata is unable to fetch dataset names currently")
            return None
        else:
            datasets = response.json()

            for i in range(len(datasets["results"])):
                names.append(datasets["results"][i]["title"])

    except HTTPError as e:
        print("HTTPError :", e)
        return None

    return names


def socrata_dataset_info(dataset_name):
    """Returns the dataset information of the dataset name provided"""
    resources = []
    url = SOCRATA_BASE_URL
    params = {'names': dataset_name}
    try:
        response = url_response(url, params)

        if response.status_code == 404:
            print("Socrata is unable to fetch the metadata of {dataset_name}".format(
                dataset_name=dataset_name))
            return None
        else:
            data = response.json()
            result = data["results"]

            for i in range(len(result)):
                resources.append({
                    "name": result[i]["resource"]["name"],
                    "id": result[i]["resource"]["id"],
                    "type": {
                        result[i]["resource"]["type"]:
                            result[i]["resource"]["lens_view_type"]
                    },
                    "description": result[i]["resource"]["description"],
                    "domain": result[i]["metadata"]["domain"],
                    "link": result[i]["link"]
                })

    except HTTPError as e:
        print("HTTPError : ", e)
        return None

    return resources


def find_socrata_dataset_by_id(dataset_id):
    """Returns metadata for the following dataset id"""
    resource = {}
    url = SOCRATA_BASE_URL
    params = {"ids": dataset_id}
    try:
        response = url_response(url, params)

        if response.status_code == 400:
            print(response.json()["error"])
            return {}
        elif response.status_code == 200:
            data = response.json()

            if len(data["results"]):
                metadata = data["results"][0]

                if (metadata["resource"]["lens_view_type"] !=
                        "tabular") or (metadata["resource"]["type"] == "map"):
                    resource["error"] = "Dataset cannot be downloaded using Socrata API"
                    resource["datatype"] = [
                        metadata["resource"]["type"],
                        metadata["resource"]["lens_view_type"]
                    ]

                elif len(metadata["resource"]["columns_name"]) == 0:
                    print("Cannot download the dataset using {}".format(dataset_id))
                    print("Try downloading using its parent id : {}".format(
                        metadata["resource"]["parent_fxf"][0]))
                    return resource

                else:
                    resource["name"] = metadata["resource"]["name"]
                    resource["id"] = metadata["resource"]["id"]
                    resource["description"] = metadata["resource"]["description"]
                    resource["datatype"] = metadata["resource"]["lens_view_type"]
                    resource["keywords"] = list(
                        set(metadata["classification"]["categories"] +
                            metadata["classification"]["tags"])) + ["socrata"]
                    resource["domain"] = metadata["metadata"]["domain"]
                    resource["homepage"] = metadata["link"]
            else:
                print("No socrata dataset exists for the id : {dataset_id}".format(
                    dataset_id=dataset_id))

    except HTTPError as e:
        print("HTTPError : ", e)
        return {}

    return resource


def update_socrata_contents(json_file, script_name, url, resource):
    """Update the contents of the json script"""
    if "archived" in json_file.keys():
        json_file.pop("archived")
    if all([
            "resources" in json_file.keys(),
            len(json_file["resources"]), "path" in json_file["resources"][0].keys()
    ]):
        json_file["resources"][0].pop("path")

    keys = ["name", "id", "description", "datatype", "keywords", "domain", "homepage"]
    flag = True
    for key in keys:
        if key not in resource:
            flag = False
            break

    if flag:
        json_file["description"] = resource["description"]
        json_file["homepage"] = resource["homepage"]
        json_file["licenses"] = [{"name": "Public Domain"}]
        json_file["keywords"] = resource["keywords"]
        json_file["name"] = script_name
        json_file["resources"][0]["name"] = script_name.replace("-", "_")
        json_file["resources"][0]["url"] = url
        json_file["socrata"] = "True"
        json_file["title"] = resource["name"]
        json_file["citation"] = ""
        json_file["retriever_minimum_version"] = "3.0.1-dev"

        return True, json_file
    else:
        return False, None


def update_socrata_script(script_name, filename, url, resource, script_path):
    """Renames the script name and the contents of the script"""
    filename = filename.replace("-", "_") + ".json"
    script_filename = script_name.replace("-", "_") + ".json"

    if filename in [
            file_i for file_i in os.listdir(script_path) if file_i.endswith(".json")
    ]:
        os.rename(f"{script_path}/{filename}", f"{script_path}/{script_filename}")
        with open(f"{script_path}/{script_filename}", "r") as f:
            json_file = json.load(f)
        f.close()

        result, json_file = update_socrata_contents(json_file, script_name, url, resource)
        if result:
            json_object = json.dumps(json_file, sort_keys=True, indent=4)

            with open(f"{script_path}/{script_filename}", "w") as f:
                f.write(json_object)
            f.close()

            print("Successfully updated {script_filename}".format(
                script_filename=script_filename))
        else:
            print("Could not update {script_filename} with the given resource".format(
                script_filename=script_filename))
    else:
        print("File {filename} does not exist in path {script_path}".format(
            filename=filename, script_path=script_path))


def create_socrata_dataset(engine, name, resource, script_path=None):
    """Downloads raw data and creates a script for the socrata dataset"""
    if script_path is None:
        script_path = SOCRATA_SCRIPT_WRITE_PATH
    filename = resource["id"] + '.csv'
    engine.script = BasicTextTemplate(**{"name": name})
    url = 'https://' + resource["domain"] + '/resource/' + filename

    if not engine.find_file(filename) or not engine.use_cache:
        path = engine.format_filename(filename)
        engine.create_raw_data_dir()
        progbar = tqdm(
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            desc='Downloading {}'.format(filename),
        )
        result = engine.download_from_socrata(url, path, progbar)
        if not result:
            print("Unable to download the dataset using Socrata API")

    elif engine.find_file(filename):
        path = engine.format_filename(filename)

    engine.script = None

    if engine.opts["command"] == "download":
        engine.final_cleanup()
        return
    else:
        if not os.path.exists(script_path):
            os.makedirs(script_path)
        file = name.replace("-", "_")
        if str(file + ".json") in [
                file_i for file_i in os.listdir(script_path) if file_i.endswith(".json")
        ]:
            print(f"Dataset {name} already exists as {file}.json in {script_path}")
        else:
            create_package(path, "tabular", True, script_path)
            print("Updating script name to {}".format(name + ".json"))
            print("Updating the contents of script {}".format(name))
            update_socrata_script(name, filename, url, resource, script_path)
            reload_scripts()
