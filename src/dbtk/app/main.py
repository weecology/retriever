"""Database Toolkit UI

This module contains the UI elements of the database toolkit platform. 

The application can be started by running the launch_app function with a list
of DbTkList objects.

"""

from dbtk.app.app import App


def launch_app(lists):
    """Launches the application GUI."""
    print "Launching Database Toolkit..."                    
    
    app = App(lists)
    app.MainLoop()
