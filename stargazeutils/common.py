from datetime import datetime
from decimal import Decimal
from typing import List

EPOCH = datetime.utcfromtimestamp(0)
DATETIME_FMT = "%a %m-%d %I:%M %p"
MARKET_CONTRACT = "stars1fvhcnyddukcqfnt7nlwv3thm5we22lyxyxylr9h77cvgkcn43xfsvgv0pl"


def timestamp_from_str(ts):
    """Returns a timestamp with milliseconds as a datetime timestamp."""
    return datetime.utcfromtimestamp(float(Decimal(ts) / 1000000000))


def print_table(
    table: List[List], header: str = None, footer: str = None, delimiter="|"
):
    """Prints an array of arrays as a table. The rows
    should be the same length or this method may yield
    unexpected results.

    :param rows: The rows of data
    """
    if header is not None:
        print(header)

    col_count = len(table[0])
    max_widths = []
    for col_i in range(col_count):
        max_widths.append(len(max([str(row[col_i]) for row in table], key=len)))

    for row in table:
        row_str = ""
        for i, col in enumerate(row):
            row_str += f" {delimiter} " + str(col).ljust(max_widths[i])
        print(row_str)

    if footer is not None:
        print(footer)


def export_table_csv(table: List[List], filename: str):
    with open(filename, "w") as f:
        for row in table:
            f.write('"' + '","'.join([str(c) for c in row]) + '"\n')
