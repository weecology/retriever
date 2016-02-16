"""A function to begin dataset downloads in a separate thread."""

import sys
from time import time
from threading import Thread, Lock
import wx
from retriever.lib.tools import final_cleanup


class DownloadThread(Thread):

    def __init__(self, engine, script):
        Thread.__init__(self)
        self.engine = engine
        self.engine.disconnect()
        self.script = script
        self.daemon = True
        self.output_lock = Lock()
        self.output = []
        self.done = False

    def run(self):
        """Initiates the download"""
        try:
            self.engine.connect()
            self.download_script()
            self.done = True
            self.engine.disconnect()
        except:
            self.engine.disconnect()
            raise
            return

    def finished(self):
        """Returns True if the download is complete"""
        return self.done

    def download_script(self):
        engine = self.engine
        script = self.script
        worker = self

        start = time()

        class download_stdout:

            def write(self, s):
                if s and s != '\n':
                    worker.output_lock.acquire()
                    worker.output.append(s)
                    worker.output_lock.release()

        sys.stdout = download_stdout()

        print "Connecting to database..."

        # Connect
        try:
            engine.get_cursor()
        except Exception as e:
            print "<b><font color='red'>Error: There was an error with your database connection.<br />" + e.__str__() + "</font></b>"
            return

        # Download script
        error = False

        print "<b><font color='blue'>Downloading. . .</font></b>"
        try:
            script.download(engine)
        except Exception as e:
            error = True
            print "<b><font color='red'>Error: " + e.__str__() + "</font></b>"

        if not error:
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

            print "<b>Done!</b> <i>Elapsed time: %02d:%02d:%s</i>" % (h, m, s)
