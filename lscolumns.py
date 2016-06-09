from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import zip
from builtins import range
import sys
from retriever.term_size import get_terminal_size


def get_columns(values, cols):
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
    if sys.stdout.isatty() and max_width is None:
        cols, lines = get_terminal_size()
        max_width = cols

    if max_width:
        # if output to terminal or max_width is specified, use column output

        for cols in [int((len(values) // float(i)) + 0.5) for i in range(1, len(values) + 1)]:
            columns = get_columns(values, cols)
            widths = [max([len(c) for c in column]) +
                      spacing for column in columns]
            if sum(widths) < max_width:
                break

        for pos in range(len(columns[0])):
            for column, width in zip(columns, widths):
                if len(column) > pos:
                    print(column[pos].ljust(width - 1), end=' ')
            print()

    else:
        # otherwise, just output each value, one per line
        for value in values:
            print(value)
