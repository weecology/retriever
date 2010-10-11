"""Database Toolkit Wizard

This module contains a list of all current DBTK scripts.

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

The main() function can be used for bootstrapping.

"""

import os
import sys
import urllib
import wx
from dbtk import DBTK_LIST, VERSION, REPOSITORY
from dbtk.lib.tools import AutoDbTk, DbTkList
from dbtk.ui.wizard import launch_wizard

DBTK_LIST = DBTK_LIST()

lists = []
lists.append(DbTkList("All Datasets", DBTK_LIST))

global abort
abort = False


def get_lists():
    # Check for .cat files
    files = os.listdir(os.getcwd())
    cat_files = [file for file in files if file[-4:] == ".cat"]
    for file in cat_files:
        cat = open(file, 'rb')
        scriptname = cat.readline().replace("\n", "")
        scripts = []
        for line in [line.replace("\n", "") for line in cat]:
            new_scripts = [script for script in DBTK_LIST
                           if script.shortname == line]
            for script in new_scripts:
                scripts.append(script)
        lists.append(DbTkList(scriptname, scripts))


    # Get list of additional datasets from dbtk.config file
    if os.path.isfile("scripts.config"):
        other_dbtks = []
        config = open("scripts.config", 'rb')
        for line in config:
            if line:
                line = line.strip('\n').strip('\r')
                values = line.split(', ')
                try:
                    dbname, tablename, url = (values[0], values[1], values[2])
                    other_dbtks.append(AutoDbTk(
                                                dbname + "." + tablename, 
                                                dbname, 
                                                tablename, 
                                                url))
                except:
                    pass

        if len(other_dbtks) > 0:
            lists.append(DbTkList("Custom", other_dbtks))
            for script in other_dbtks:
                lists[0].scripts.append(script)
                
    return lists


def download_from_repository(filepath):
    filename = filepath.split('/')[-1]
    if os.path.isfile(filename):
        os.remove(filename)
    latest = urllib.urlopen(REPOSITORY + filepath, 'rb')
    file_size = latest.info()['Content-Length']
    new_file = open(filename, 'wb')
    total_dl = 0
    while not abort:
        data = latest.read(1024)
        total_dl += len(data)
        print str(int(total_dl / float(file_size) * 100))
        if len(data) == 0:
            break
        new_file.write(data)
    new_file.close()
    latest.close()


def check_for_updates():
    running_from = os.path.basename(sys.argv[0])
    if os.path.isfile('dbtk_old.exe'):
        try:
            os.remove('dbtk_old.exe')
        except:
            pass
    version_file = urllib.urlopen(REPOSITORY + "version.txt")
    latest = version_file.readline().strip('\n').strip('\r')
    cats = version_file.readline().strip('\n').strip('\r').split(',')
    for cat in cats:
        if not os.path.isfile(cat + ".cat"):
            download_from_repository("cats/" + cat + ".cat")
    if latest != VERSION:
        if running_from in ['dbtk.exe']:
            app = wx.PySimpleApp()
            msg = "You're running version " + VERSION + "."
            msg += '\n\n'
            msg += "Version " + latest + " is available. Do you want to upgrade?"
            choice = wx.MessageDialog(None, msg, "Update", wx.YES_NO)
            if choice.ShowModal() == wx.ID_YES:
                print "Updating to latest version. Please wait..."
                if running_from == 'dbtk.exe':
                    try:
                        os.rename('dbtk.exe', 'dbtk_old.exe')
                    except:
                        pass
                    new_file = "windows/dbtk.exe"
                progress = wx.ProgressDialog("Update",
                                             "Updating to latest version. Please wait...",
                                             101,
                                             style=
                                             wx.PD_REMAINING_TIME |
                                             wx.PD_CAN_ABORT
                                             )
                class update_progress:
                    def __init__(self, parent):
                        self.parent = parent
                    def write(self, s):
                        try:
                            s = int(s)
                            if s < 1:
                                s = 1
                            (keepgoing, skip) = self.parent.Update(s)
                            if not keepgoing:
                                abort = True
                        except:
                            pass
                sys.stdout = update_progress(progress)
                download_from_repository(new_file)
                progress.Update(101, "Done!")
                sys.stdout = sys.__stdout__
                wx.MessageBox("Update complete. Please restart the program.")
                sys.exit()
            

def main():    
    check_for_updates()
    launch_wizard(get_lists())


if __name__ == "__main__":
    main()
