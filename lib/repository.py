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
        def reporthook(a,b,c):
            print "%3.1f-%s" % (min(100, float(a * b) / c * 100), filename),
            sys.stdout.flush()
            print
        
        urllib.urlretrieve(repo + filepath, newpath, reporthook=reporthook)
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


def check_for_updates(graphical=False):
    """Check for updates to scripts and executable."""
    if graphical:
        import wx
        app = wx.App(False)

        from retriever.app.splash import Splash
        splash = Splash()
        #splash.Show()
        splash.SetText("\tLoading...")

        class update_progress:
            def __init__(self, parent):
                self.parent = parent
            def write(self, s):
                if s != "\n":
                    try:
                        self.parent.SetText('\t' + s)
                    except:
                        pass
            def flush(self):
                pass

        sys.stdout = update_progress(splash)

    init = InitThread()
    init.run()

    if graphical:
        splash.Hide()
        sys.stdout = sys.__stdout__
    print "retriever up to date"

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

            if False:#running_from[-4:] == ".exe":
                if os.path.isfile('retriever_old.exe') and running_from != 'retriever_old.exe':
                    try:
                        os.remove('retriever_old.exe')
                    except:
                        pass

                # Windows: open master branch version file to find out most recent executable version
                try:
                    version_file = urllib.urlopen(MASTER_BRANCH + "version.txt")
                except IOError:
                    print "Couldn't open version.txt from repository"
                    return

                latest = version_file.readline().strip('\n')

                if more_recent(latest, VERSION):
                    import wx

                    msg = "You're running version " + VERSION + "."
                    msg += '\n\n'
                    msg += "Version " + latest + " is available. Do you want to upgrade?"
                    choice = wx.MessageDialog(None, msg, "Update", wx.YES_NO)
                    if choice.ShowModal() == wx.ID_YES:
                        print "Updating to latest version. Please wait..."
                        try:
                            if not "_old" in running_from:
                                os.rename(running_from,
                                          '.'.join(running_from.split('.')[:-1])
                                          + "_old." + running_from.split('.')[-1])
                        except:
                            pass

                        download_from_repository("windows/" + executable_name + ".exe",
                                                 executable_name + ".exe",
                                                 repo=REPO_URL + latest + "/")

                        sys.stdout = sys.__stdout__

                        wx.MessageBox("Update complete. The program will now restart.")

                        os.execv(executable_name + ".exe", sys.argv)

                        sys.exit()

                version_file.close()

            # open version.txt for current release branch and get script versions
            version_file = urllib.urlopen(REPOSITORY + "version.txt")
            version_file.readline()
            
            # read scripts from the repository and the checksums from the version.txt
            scripts = []
            for line in version_file:
                scripts.append(line.strip('\n').split(','))

            # create script directory if not available
            if not os.path.isdir(SCRIPT_WRITE_PATH):
                os.makedirs(SCRIPT_WRITE_PATH)
            
            for script in scripts:
                script_name = script[0]
                if len(script) > 1:
                    script_version = script[1]
                else:
                    script_version = None

                path_script_name = os.path.normpath(os.path.join(HOME_DIR, "scripts", script_name))
 
                if not file_exists(path_script_name):
                    print "Downloading script: " + script_name
                    download_from_repository("scripts/" + script_name,
                                             os.path.normpath(os.path.join(SCRIPT_WRITE_PATH, script_name)))

                # check MD5sum based on the script version to download the right scripts
                # if MD5sum dont match; need_to_download is True
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
        except:
            raise
            return
