"""Checks the repository for updates."""

import os
import sys
import urllib
import imp
import wx
from dbtk import REPOSITORY, VERSION
from dbtk.lib.models import file_exists

global abort
abort = False


def download_from_repository(filepath, newpath):
    """Downloads the latest version of a file from the repository."""
    filename = filepath.split('/')[-1]
    latest = urllib.urlopen(REPOSITORY + filepath, 'rb')
    file_size = latest.info()['Content-Length']
    new_file = open(os.path.join(os.getcwd(), newpath), 'wb')
    total_dl = 0
    while not abort:
        data = latest.read(1024)
        total_dl += len(data)
        if file_size > 102400:
            print str(int(total_dl / float(file_size) * 100)) + "-" + filename
        if len(data) == 0:
            break
        new_file.write(data)
    new_file.close()
    latest.close()


def more_recent(latest, current):
    """Given two version number strings, returns True if the first is more recent."""
    latest_parts = latest.split('.')
    current_parts = current.split('.')
    for n in range(len(latest_parts)):
        if len(current_parts) < (n + 1):
            return True
        l = int(latest_parts[n])
        c = int(current_parts[n])        
        if l > c:
            return True
        elif c > l:
            return False
    return False


def check_for_updates():
    """Check for updates to categories, scripts, and executable."""
    app = wx.PySimpleApp()
    progress = wx.ProgressDialog("Update",
                                 "Checking for updates. Please wait...",
                                 101,
                                 style=
                                 wx.PD_REMAINING_TIME |
                                 wx.PD_CAN_ABORT |
                                 wx.PD_SMOOTH |
                                 wx.PD_AUTO_HIDE
                                 )
    class update_progress:
        def __init__(self, parent):
            self.parent = parent
        def write(self, s):
            try:
                filename = s.split('-')[1]
                msg = "Downloading " + filename + "..."
                s = int(s.split('-')[0])
                if s < 1:
                    s = 1
                (keepgoing, skip) = self.parent.Update(s, msg)
                if not keepgoing:
                    abort = True
            except:
                pass
    sys.stdout = update_progress(progress)    
    running_from = os.path.basename(sys.argv[0])
    
    if os.path.isfile('dbtk_old.exe') and running_from != 'dbtk_old.exe':
        try:
            os.remove('dbtk_old.exe')
        except:
            pass
    
    try:
        version_file = urllib.urlopen(REPOSITORY + "version.txt")
    except IOError:
        return
        
    latest = version_file.readline().strip('\n')
    cats = version_file.readline().strip('\n').split(',')
    scripts = []
    for line in version_file:
        scripts.append(line.strip('\n').split(','))
    
    # get category files
    if not os.path.isdir("categories"):
        os.mkdir("categories")    
    for cat in cats:
        if not file_exists(os.path.join("categories", cat + ".cat")):
            download_from_repository("categories/" + cat + ".cat", 
                                     "categories/" + cat + ".cat")
    
    # get script files
    if not os.path.isdir("scripts"):
        os.mkdir("scripts")
    for script in scripts:
        script_name = script[0]
        if len(script) > 1:
            script_version = script[1]
        else:
            script_version = None

        # Only download if software version is at least script version
        if not more_recent(script[1], VERSION):
            if not file_exists(os.path.join("scripts", script_name + ".py")):
                # File doesn't exist: download it
                print "DOESNT EXIST" + script_name
                download_from_repository("scripts/" + script_name + ".py",
                                         "scripts/" + script_name + ".py")
            elif script_version:
                # File exists: import and check version
                file, pathname, desc = imp.find_module(script_name, ["scripts"])
                need_to_download = False
                try:
                    new_module = imp.load_module(script_name, file, pathname, desc)
                    need_to_download = more_recent(script_version, new_module.VERSION)
                except:            
                    pass
                    
                if need_to_download:
                    try:
                        os.remove(os.path.join("scripts", script_name + ".py"))
                        download_from_repository("scripts/" + script_name + ".py",
                                                 "scripts/" + script_name + ".py")
                    except:
                        pass
        
    if more_recent(latest, VERSION):
        if running_from[-4:] == ".exe":
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
                    
                download_from_repository("windows/dbtk.exe", "dbtk.exe")

                progress.Update(101)
                sys.stdout = sys.__stdout__

                wx.MessageBox("Update complete. The program will now restart.")

                os.execv('dbtk.exe', sys.argv)
                
                sys.exit()
                
    progress.Update(101)
    progress.Destroy()
    sys.stdout = sys.__stdout__
