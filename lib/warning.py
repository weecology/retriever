from builtins import object
class Warning(object):

    def __init__(self, location, warning):
        self.location = location
        self.warning = warning

    def __str__(self):
        return 'WARNING (%s): %s' % (self.location, self.warning)
