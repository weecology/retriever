"""Checks the repository for updates."""


import os
import sys
import urllib
import imp
from hashlib import md5
from inspect import getsourcelines
from threading import Thread
from retriever import REPOSITORY, VERSION, MASTER_BRANCH, REPO_URL, SCRIPT_WRITE_PATH, HOME_DIR
from retriever.lib.models import file_exists

global abort, executable_name
abort = False
executable_name = "retriever"


def download_from_repository(filepath, newpath, repo=REPOSITORY):
    """Downloads the latest version of a file from the repository."""
    try:
        filename = filepath.split('/')[-1]
        urllib.urlretrieve(repo + filepath, newpath)
    except:
        raise
        pass


def more_recent(latest, current):
    """Given two version number strings, returns True if the first is more recent."""
    latest_parts = latest.split('.')
    current_parts = current.split('.')
    for n in range(len(latest_parts)):
        l = latest_parts[n]
        if len(current_parts) < (n + 1):
            return (l != "rc")
        c = current_parts[n]
        if l > c:
            return True
        elif c > l:
            return False
    return (len(current_parts) > (n + 1) and current_parts[n + 1] == "rc")


def check_for_updates():
    """Check for updates to scripts and executable."""
    init = InitThread()
    init.run()

    print "\nThe retriever is up-to-date"


def update_progressbar(progress):
    """Show progressbar

    Takes a number between 0 and 1 to indicate progress from 0 to 100%.

    """
    # Try to set the bar_length according to the console size
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        bar_length = int(columns) - 35
        if(not (bar_length > 1)):
            bar_length = 20
    except:
        # Default value if determination of console size fails
        bar_length = 20
    block = int(round(bar_length*progress))
    text = "\rDownload Progress: [{0}] {1:.2f}%".format(
        "#"*block + "-"*(bar_length-block), progress*100)
    sys.stdout.write(text)
    sys.stdout.flush()


class InitThread(Thread):
    """This thread performs all of the necessary updates while the splash screen
    is shown.

    1. Check master/version.txt to get the latest version (Windows only).
    2. Prompt for update if necessary (Windows only).
    3. Download latest versions of scripts from current branch."""

    def run(self):
        try:
            running_from = os.path.basename(sys.argv[0])

            # NOTE: exe auto-update functionality has been temporarily disabled
            # since the binaries were moved to AWS.


            # open version.txt for current release branch and get script
            # versions
            version_file = urllib.urlopen(REPOSITORY + "version.txt")
            version_file.readline()

            # read scripts from the repository and the checksums from the
            # version.txt
            scripts = []
            print "Downloading scripts..."
            for line in version_file:
                scripts.append(line.strip('\n').split(','))

            total_script_count = len(scripts)

            # create script directory if not available
            if not os.path.isdir(SCRIPT_WRITE_PATH):
                os.makedirs(SCRIPT_WRITE_PATH)

            update_progressbar(0.0/float(total_script_count))
            for index, script in enumerate(scripts):
                script_name = script[0]
                if len(script) > 1:
                    script_version = script[1]
                else:
                    script_version = None

                path_script_name = os.path.normpath(os.path.join(HOME_DIR, "scripts", script_name))

                if not file_exists(path_script_name):
                    download_from_repository("scripts/" + script_name,
                                             os.path.normpath(os.path.join(SCRIPT_WRITE_PATH, script_name)))

                # check MD5sum based on the script version to download the right scripts
                # if the MD5sum doesn't match need_to_download is set to True
                need_to_download = False

                try:
                    file, pathname, desc = imp.find_module(''.join(script_name.split('.')[:-1]), ["scripts"])
                    new_module = imp.load_module(script_name, file, pathname, desc)
                    m = md5()
                    m.update(''.join(getsourcelines(new_module)[0]).replace("\r\n", "\n"))
                    m = m.hexdigest()
                    need_to_download = script_version != m
                except:
                    pass

                if need_to_download:
                    try:
                        os.remove(os.path.normpath(os.path.join(HOME_DIR,"scripts", script_name)))
                        download_from_repository("scripts/" + script_name,
                                                 os.path.normpath(os.path.join(SCRIPT_WRITE_PATH, script_name)))
                    except Exception as e:
                        print e
                        pass
                update_progressbar(float(index + 1)/float(total_script_count))
        except:
            raise
            return
