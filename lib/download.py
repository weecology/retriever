"""A function to begin dataset downloads in a separate thread."""

import sys
from time import time
from threading import Thread, Lock
import wx
from dbtk.lib.tools import final_cleanup


class DownloadThread(Thread):
    def __init__(self, engine, scripts):
        Thread.__init__(self)
        self.engine = engine
        self.scripts = scripts
        self.scriptnum = 0
        self.progress_max = 1
        self.daemon = True
        self.output_lock = Lock()
        self.output = []

    def run(self):
        try:
            self.download_scripts()
            self.scriptnum = self.progress_max + 1
        except:
            return
        
    def finished(self):
        return (self.scriptnum > self.progress_max)

    def download_scripts(self):
        engine = self.engine
        worker = self
        scripts = self.scripts
        
        start = time()
        
        class download_stdout:
            def write(self, s):
                if s and s != '\n':
                    worker.output_lock.acquire()
                    worker.output.append(s)
                    worker.output_lock.release()
                
        sys.stdout = download_stdout()
            
        worker.progress_max = len(scripts)            
                
        def start_download():
            worker.scriptnum = 0
            
            print "Connecting to database..."
            
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
                msg = "<b><font color='blue'>Downloading: " + script.name + "</font></b>"
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
                print "<b>Done!</b>"
                
            finish = time()
            
            time_diff = finish - start
            
            if time_diff > 3600:
                h = time_diff // 3600
                time_diff %= 3600
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
        
        start_download()
