"""A function to begin dataset downloads in a separate thread."""

import sys
from time import time
import wx
from dbtk.lib.tools import final_cleanup

def download_scripts(worker, wizard):
    start = time()
    
    class download_stdout:
        def __init__(self, parent):
            self.parent = parent
        def write(self, s):
            worker.output.append(s)
            
    sys.stdout = download_stdout(wizard.DOWNLOAD)

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
        
    worker.progress_max = len(scripts)            
            
    def OnTimer(evt):
        worker.scriptnum = 0
        
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
            print "<font color='red'>There was an error with your database connection.</font>" 
            return
        
        
        # Download scripts
        errors = []
        for script in scripts:
            worker.scriptnum += 1
            msg = "<b><font color='blue'>Downloading " + script.name + "</font></b>"
            if len(scripts) > 0:
                msg += " (" + str(worker.scriptnum) + " of " + str(worker.progress_max) + ")"
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
            
        finish = time()
        
        time_diff = finish - start
        
        if time_diff > 360:
            h = time_diff // 360
            time_diff %= 360
        else:
            h = 0
        if time_diff > 60:
            m = time_diff // 60
            time_diff %= 60
        else:
            m = 0
        s = "%.2f" % (time_diff)
        if len(s.split('.')[0]) < 2:
            s = "0" + s
        
        print "<i>Elapsed time: %02d:%02d:%s</i>" % (h, m, s)
    
    OnTimer(None)
