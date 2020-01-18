"""Checks the repository for updates."""
import os
import requests
import imp
from tqdm import tqdm
from pkg_resources import parse_version
from retriever.lib.defaults import (REPOSITORY, RETRIEVER_REPOSITORY, SCRIPT_WRITE_PATH,
                                    HOME_DIR)
from retriever.lib.models import file_exists


def _download_from_repository(filepath, newpath, repo=REPOSITORY):
    """Download latest version of a file from the repository."""
    try:
        r = requests.get(repo + filepath, allow_redirects=True, stream=True)
        with open(newpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        r.close()
    except:
        raise


def check_for_updates(repo=REPOSITORY):
    """Check for updates to datasets.

    This updates the HOME_DIR scripts directory with the latest script versions
    """
    try:
        # open version.txt for current release branch and get script versions
        version_file = requests.get(repo + "version.txt").text
        version_file = version_file.splitlines()[1:]

        # read scripts from the repository and the checksums from the version.txt
        scripts = []
        for line in version_file:
            scripts.append(line.strip('\n').split(','))

        # create script directory if not available
        if not os.path.isdir(SCRIPT_WRITE_PATH):
            print('No scripts are currently available. Creating scripts folder...')
            os.makedirs(SCRIPT_WRITE_PATH)

        scripts_type = 'upstream'
        if repo == RETRIEVER_REPOSITORY:
            scripts_type = 'default'
        desc = 'Downloading {} scripts'.format(scripts_type)
        for script in tqdm(scripts, unit='files', desc=desc):
            script_name = script[0]
            if len(script) > 1:
                script_version = script[1]
            else:
                script_version = None

            script_home_path = os.path.normpath(
                os.path.join(HOME_DIR, "scripts", script_name))
            download_path = os.path.normpath(os.path.join(SCRIPT_WRITE_PATH, script_name))
            if not file_exists(script_home_path):
                _download_from_repository("scripts/" + script_name, download_path, repo)
            need_to_download = False
            try:
                file_object, pathname, desc = imp.find_module(
                    ''.join(script_name.split('.')[:-1]), [SCRIPT_WRITE_PATH])
                new_module = imp.load_module(script_name, file_object, pathname, desc)
                m = str(new_module.SCRIPT.version)
                need_to_download = parse_version(str(script_version)) > parse_version(m)
            except:
                pass
            if need_to_download:
                try:
                    os.remove(script_home_path)
                    _download_from_repository("scripts/" + script_name, download_path,
                                              repo)
                except Exception as e:
                    print(e)
    except:
        raise

    if repo == RETRIEVER_REPOSITORY:
        return
    check_for_updates(RETRIEVER_REPOSITORY)
