"""A function to begin dataset downloads in a separate thread."""

import sys
import wx
from dbtk.lib.tools import final_cleanup

def download_scripts(wizard):
    wizard.FindWindowById(wx.ID_FORWARD).Disable()
    wizard.FindWindowById(wx.ID_BACKWARD).Disable()

    # Get a list of scripts to be downloaded
    scripts = []
    checked_scripts = wizard.DATASET.scriptlist.GetCheckedStrings()
    for script in wizard.dbtk_list:
        dl = False
        if len(wizard.dbtk_list) > 1:
            if script.name in checked_scripts:
                dl = True
        else:
            dl = True
        if dl:
            scripts.append(script)
            
    # Find the script with the longest name to set size of progress dialog        
    longestname = 20
    for script in scripts:
        if len(script.name) > longestname:
            longestname = len(script.name)
    
    # Create a frame to contain the progress dialog
    class Frame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="")
            self.progressMax = 100
            self.count = 0
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
            self.timer.Start(1)
            
        def OnTimer(self, evt):
            self.timer.Stop()
            
            scriptnum = 0
    
            # Allow exception handling for "skip" and "cancel" buttons
            class UserSkipped(Exception):
                pass
            class UserAborted(Exception):
                pass
            
            print "Connecting to database . . ."
                    
            # Get options from wizard
            engine = wizard.CONNECTION.engine
            options = wizard.CONNECTION.option
            engine.keep_raw_data = wizard.CHOOSEDB.keepdata.Value
            engine.use_local = wizard.CHOOSEDB.uselocal.Value
            engine.RAW_DATA_LOCATION = wizard.CHOOSEDB.raw_data_dir.Value
            opts = dict()
            for key in options.keys():
                opts[key] = options[key].GetValue()
            engine.opts = opts
            
            # Connect
            try:
                engine.get_cursor()
            except Exception as e:
                wx.MessageBox("There was an error with your database" 
                              + " connection. \n\n" +
                              e.__str__())
                app.Exit()
                return
            
            oldstdout = sys.stdout
            #sys.stdout = update_dialog(self)
            
            # Download scripts
            errors = []
            for script in scripts:
                scriptnum += 1
                msg = "Downloading " + script.name
                if len(scripts) > 0:
                    msg += " (" + str(scriptnum) + " of " + str(len(scripts)) + ")"
                msg += " . . ."
                print msg
                try:
                    script.download(engine)
                except Exception as e:
                    errors.append("There was an error downloading " + 
                                  script.name + ".")
                    wx.MessageBox(e.__str__(), "Error")
                    app.Exit()
                    raise
                    
            final_cleanup(engine)
            
            if errors:
                errors = "The following errors occurred:<ul>"
                for error in errors:
                    errors += "<li>" + error + "</li>"
                errors += "</ul>"
                print errors
            else:
                print "Your downloads were completed successfully."
            
            wizard.FindWindowById(wx.ID_CANCEL).Disable()
            wizard.FindWindowById(wx.ID_FORWARD).Enable()
            
                
    frame = Frame()
    frame.Show(False)
