from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from builtins import range
from builtins import zip

from retriever.term_size import get_terminal_size


def get_columns(values, cols):
    """Returns number of columns to display."""
    columns = []
    col_size = len(values) // cols
    extra = len(values) % cols
    n = 0
    for i in range(cols):
        s = col_size
        if i + 1 <= extra:
            s += 1
        this_column = values[n:n + s]
        columns.append(this_column)
        n += s
    return columns


def printls(values, max_width=None, spacing=2):
    """"Customized print for ls values on terminal.

    Use current terminal size to fit the results of ls.
    """
    if sys.stdout.isatty() and max_width is None:
        cols, _ = get_terminal_size()
        max_width = cols

    if max_width:
        # if output to terminal or max_width is specified, use column output
        columns = None
        for cols in [int((len(values) // float(i)) + 0.5) for i in range(1, len(values) + 1)]:
            columns = get_columns(values, cols)
            widths = [max([len(c) for c in column]) +
                      spacing for column in columns]
            if sum(widths) < max_width:
                break
        if columns:
            for pos in range(len(columns[0])):
                for column, width in zip(columns, widths):
                    if len(column) > pos:
                        print(column[pos].ljust(width - 1), end=' ')
                print()

    else:
        # otherwise, just output each value, one per line
        for value in values:
            print(value)
