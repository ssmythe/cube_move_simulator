# tests/test_facelet_edge_map.py

import pytest
from cms.main import parse_args, create_cube
from cms.utils import build_edge_map

# physical solved‐cube edges (independent of how you label it)
SOLVED_EDGES = {
    "UF": ("W","G"), "UR": ("W","R"), "UB": ("W","B"), "UL": ("W","O"),
    "DF": ("Y","G"), "DR": ("Y","R"), "DB": ("Y","B"), "DL": ("Y","O"),
    "FR": ("G","R"), "FL": ("G","O"), "BR": ("B","R"), "BL": ("B","O"),
}

@pytest.mark.parametrize(
    "notation,color,facelet_str",
    [
        # default physical mapping: ULFRBD + WOGRBY
        (
            "ULFRBD", "WOGRBY",
            # U…9, L…9, F…9, R…9, B…9, D…9
            "W"*9 + "O"*9 + "G"*9 + "R"*9 + "B"*9 + "Y"*9
        ),
        # same physical cube, but labeled URFDLB + WRGYOB
        (
            "URFDLB", "WRGYOB",
            # now the *first* 9 are U→W,
            # the *second* 9 are R→R,
            # the *third* 9 are F→G,
            # the *fourth* 9 are D→Y,
            # the *fifth* 9 are L→O,
            # the *sixth* 9 are B→B
            "W"*9 + "R"*9 + "G"*9 + "Y"*9 + "O"*9 + "B"*9
        ),
    ],
)
def test_facelet_edge_map_both_notations(notation, color, facelet_str):
    args = parse_args([
        "-n", notation,
        "-c", color,
        "-f", facelet_str,
    ])
    cube = create_cube(args)
    edge_map = build_edge_map(cube, args)

    assert edge_map == SOLVED_EDGES
