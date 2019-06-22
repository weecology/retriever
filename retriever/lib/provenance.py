import json
import os
import pkg_resources
from datetime import datetime, timezone
from zipfile import ZipFile

from retriever.engines import choose_engine
from retriever.lib.datasets import datasets
from retriever.lib.defaults import HOME_DIR, ENCODING
from retriever.lib.engine_tools import getmd5


def package_details():
    details = {}
    packages = pkg_resources.working_set
    for package in packages:
        package_name, version = str(package).split(" ")
        details[package_name] = version
    return details


def commit_info(dataset):
    """
    Generate info for a particular commit.
    """
    info = {
        "packages": package_details(),
        "time": datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S"),
        "version": dataset.version,
    }
    return info


def commit(dataset, commit_message='', path='.', quiet=False):
    """
    Commit dataset to a zipped file.
    """
    if isinstance(dataset, str):
        # if dataset is not a dataset script object find the right script
        dataset = [script for script in datasets() if script.name == dataset][0]
    paths_to_zip = {"script": dataset._file, "raw_data": []}
    raw_dir = os.path.join(HOME_DIR, "raw_data")
    data_exists = False
    if not quiet:
        print("Committing dataset {}".format(dataset.name))
    try:
        if dataset.name not in os.listdir(raw_dir):
            engine = choose_engine({"command": "download", "path": "./", "sub_dir": ""})
            dataset.download(engine=engine, debug=quiet)
            data_exists = True

        elif dataset.name in os.listdir(raw_dir):
            data_exists = True

        if data_exists:
            for root, _, files in os.walk(os.path.join(raw_dir, dataset.name)):
                for file in files:
                    paths_to_zip["raw_data"].append(os.path.join(root, file))

            info = commit_info(dataset)
            info["commit_message"] = commit_message
            info["script_name"] = os.path.basename(dataset._file)
            path_to_raw_data = os.path.join(HOME_DIR, "raw_data", dataset.name)
            if os.path.exists(path_to_raw_data):
                info["md5_dataset"] = getmd5(path_to_raw_data, "dir", encoding=ENCODING)
            info["md5_script"] = getmd5(
                dataset._file, data_type="file", encoding=ENCODING
            )
            zip_file_name = "{}-{}{}.zip".format(
                dataset.name, info["md5_dataset"][:3], info["md5_script"][:3]
            )

            zip_file_path = os.path.join(path, zip_file_name)
            with ZipFile(zip_file_path, "w") as zipped:
                zipped.write(
                    paths_to_zip["script"],
                    os.path.join("script", os.path.basename(paths_to_zip["script"])),
                )
                for data_file in paths_to_zip["raw_data"]:
                    zipped.write(data_file, data_file.replace(raw_dir, ""))
                with open("metadata.json", "w") as json_file:
                    json.dump(info, json_file, sort_keys=True, indent=4)
                zipped.write(os.path.abspath(json_file.name), "metadata.json")
                os.remove("metadata.json")
        if not quiet:
            print("Successfully committed.")
    except Exception as e:
        print(e)
        print("Dataset could not be committed.")
        return
