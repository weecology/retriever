import os
import sys
import urllib
import wx
from dbtk import REPOSITORY, VERSION

global abort
abort = False


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


def more_recent(latest, current):
    latest_parts = latest.split('.')
    current_parts = current.split('.')
    for n in range(len(latest_parts)):
        l = int(latest_parts[n])
        c = int(current_parts[n])
        if l > c:
            return True
        elif c > l:
            return False
    return False


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
    if more_recent(latest, VERSION):
        if running_from == "dbtk" or running_from[-4:] == '.exe':
            app = wx.PySimpleApp()
            msg = "You're running version " + VERSION + "."
            msg += '\n\n'
            msg += "Version " + latest + " is available. Do you want to upgrade?"
            choice = wx.MessageDialog(None, msg, "Update", wx.YES_NO)
            if choice.ShowModal() == wx.ID_YES:
                print "Updating to latest version. Please wait..."
                if running_from[-4:] == '.exe':
                    try:
                        if not "_old" in running_from:
                            os.rename(running_from,
                                      '.'.join(running_from.split('.')[:-1])
                                      + "_old." + running_from.split('.')[-1])
                    except:
                        pass
                    new_file = "windows/dbtk.exe"
                elif running_from == 'dbtk':
                    new_file = "linux/dbtk"
                else:
                    sys.quit()
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
