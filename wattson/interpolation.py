from typing import Dict, Optional, TypeVar

TK = TypeVar("TK", int, float)
TV = TypeVar("TV", int, float)


def interpolate_from_table(
    table: Dict[TK, TV],
    x: TV,
) -> Optional[float]:
    """
    Linearly interpolate a value from a dictionary describing
    a piecewise linear function.

    :param table: A mapping of "X" values to "Y" values.
    :param x: The "X" value whose "Y" to find.
    :return: "Y" value corresponding to `value`,
             or None if `x` is out of range for the table.
    """
    sorted_xs = sorted(table)
    for i, table_x in enumerate(sorted_xs[:-1]):
        next_x = sorted_xs[i + 1]
        if table_x <= x <= next_x:
            low_y = table[table_x]
            high_y = table[next_x]
            x_range = next_x - table_x
            y_range = high_y - low_y
            return low_y + y_range * (x - table_x) / x_range
    return None
