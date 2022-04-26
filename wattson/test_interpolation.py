from wattson.interpolation import interpolate_from_table


def test_interpolation() -> None:
    tab = {0.0: -1.0, 1.0: 1.0}
    assert interpolate_from_table(tab, 0.5) == 0
    assert interpolate_from_table(tab, 0) == -1
    assert interpolate_from_table(tab, 1) == 1
    assert interpolate_from_table(tab, 1.1) is None
    assert interpolate_from_table(tab, -0.1) is None
