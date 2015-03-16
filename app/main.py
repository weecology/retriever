"""EcoData Retriever UI

This module contains the UI elements of the EcoData Retriever platform.

The application can be started by running the launch_app function with a list
of Category objects.

"""

from retriever.app.app import App


def launch_app(lists):
    """Launches the application GUI."""
    print "Launching EcoData Retriever..."

    app = App(lists)
    app.MainLoop()
