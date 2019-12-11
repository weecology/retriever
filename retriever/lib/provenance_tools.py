import os
import json
from importlib import util
from shutil import rmtree
from tempfile import mkdtemp
from zipfile import ZipFile

from retriever.lib.load_json import read_json


def get_metadata(path_to_archive):
    """
    Returns a dictionary after reading metadata.json file of a committed dataset
    """
    with ZipFile(os.path.normpath(path_to_archive), 'r') as archive:
        try:
            metadata = json.loads(archive.read('metadata.json').decode('utf-8'))
        except Exception as e:
            print(e)
            return None
    return metadata


def get_script_provenance(path_to_archive):
    """
    Reads script from archive.
    """
    with ZipFile(os.path.normpath(path_to_archive), 'r') as archive:
        try:
            commit_details = get_metadata(path_to_archive=path_to_archive)
            workdir = mkdtemp(dir=os.path.dirname(path_to_archive))
            archive.extract('/'.join(('script', commit_details['script_name'])), workdir)
            if commit_details['script_name'].endswith('.json'):
                script_object = read_json(
                    os.path.join(workdir, 'script',
                                 commit_details['script_name'].split('.')[0]))
            elif commit_details['script_name'].endswith('.py'):
                spec = util.spec_from_file_location(
                    "script_module",
                    os.path.join(workdir, 'script', commit_details['script_name']),
                )
                script_module = util.module_from_spec(spec)
                spec.loader.exec_module(script_module)
                script_object = script_module.SCRIPT
            rmtree(workdir)
            return script_object
        except Exception as e:
            print(e)
            return None
