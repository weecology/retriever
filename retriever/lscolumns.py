import sys
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
        for cols in [
                int((len(values) // float(i)) + 0.5) for i in range(1,
                                                                    len(values) + 1)
        ]:
            columns = get_columns(values, cols)
            widths = [max([len(c[0]) for c in column]) + spacing for column in columns]
            if sum(widths) < max_width:
                break
        if columns:
            for pos in range(len(columns[0])):
                for column, width in zip(columns, widths):
                    if len(column) > pos:
                        dataset = column[pos]
                        if dataset[1]:
                            print(dataset[0].ljust(width - 1), end=' ')
                        else:
                            print('\033[91m' + (dataset[0] + '*').ljust(width - 1) +
                                  '\033[0m',
                                  end=' ')
                print()

    else:
        # otherwise, just output each value, one per line
        for value in values:
            if value[1]:
                print(value[0])
            else:
                print('\033[91m' + value[0] + '*' + '\033[0m')
