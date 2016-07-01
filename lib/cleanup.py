from builtins import object


def floatable(value):
    """Check if a value can be converted to a float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def correct_invalid_value(value, args):
    """This cleanup function replaces null indicators with None."""
    try:
        if value in [item for item in args["nulls"]]:
            return None
        if float(value) in [float(item) for item in args["nulls"] if floatable(item)]:
            return None
        return value
    except:
        return value


def no_cleanup(value, args):
    """Default cleanup function, returns the unchanged value."""
    return value


class Cleanup(object):
    """This class represents a custom cleanup function and a dictionary of
    arguments to be passed to that function."""

    def __init__(self, function=no_cleanup, **kwargs):
        self.function = function
        self.args = kwargs
