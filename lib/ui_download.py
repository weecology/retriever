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
        
            
    def OnTimer(evt):
        timer.Stop()
        
        scriptnum = 0
        
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
            msg = "<b><font color='blue'>Downloading " + script.name + "</font></b>"
            if len(scripts) > 0:
                msg += " (" + str(scriptnum) + " of " + str(len(scripts)) + ")"
            msg += " . . ."
            print msg
            try:
                script.download(engine)
            except Exception as e:
                errors.append("There was an error downloading " + 
                              script.name + ".")
                print "<font color='red'>Error: " + e.__str__() + "</font>"
                
        final_cleanup(engine)
        
        if errors:
            error_txt = "<b><font color='red'>The following errors occurred:</font></b>"
            error_txt += "<ul>"
            for error in errors:
                error_txt += "<li><font color='red'>" + error + "</font></li>"
            error_txt += "</ul>"
            print error_txt
        else:
            print "<b>Your downloads were completed successfully.</b>"
        
        wizard.FindWindowById(wx.ID_CANCEL).Disable()
        wizard.FindWindowById(wx.ID_FORWARD).Enable()
    
    timer = wx.Timer(wizard, -1)
    wizard.Bind(wx.EVT_TIMER, OnTimer, timer)
    timer.Start(1)
