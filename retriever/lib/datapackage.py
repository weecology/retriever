from __future__ import print_function

from builtins import input


def is_empty(val):
    """Check if a variable is an empty string or an empty list."""
    return val in ('', [])


def clean_input(prompt="", split_char='', ignore_empty=False, dtype=None):
    """Clean the user-input from the CLI before adding it."""
    while True:
        val = input(prompt).strip()
        # split to list type if split_char specified
        if split_char != "":
            val = [v.strip() for v in val.split(split_char) if v.strip() != ""]
        # do not ignore empty input if not allowed
        if not ignore_empty and is_empty(val):
            print("\tError: empty input. Need one or more values.\n")
            continue
        # ensure correct input datatype if specified
        if not is_empty(val) and dtype is not None:
            try:
                if not type(eval(val)) == dtype:  # pylint: disable=C0123,W0123
                    print("\tError: input doesn't match required type ", dtype, "\n")
                    continue
            except:
                print("\tError: illegal argument. Input type should be ", dtype, "\n")
                continue
        break
    return val
