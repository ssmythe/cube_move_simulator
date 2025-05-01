# tests/test_edge_map.py

import pytest
from cms.main import create_cube, parse_args
from cms.utils import build_edge_map


@pytest.mark.parametrize(
    "notation_order,color_order,expected_edges",
    [
        (
            "ULFRBD",
            "WOGRBY",
            {
                "UF": ("W", "G"),
                "UR": ("W", "R"),
                "UB": ("W", "B"),
                "UL": ("W", "O"),
                "DF": ("Y", "G"),
                "DR": ("Y", "R"),
                "DB": ("Y", "B"),
                "DL": ("Y", "O"),
                "FR": ("G", "R"),
                "FL": ("G", "O"),
                "BR": ("B", "R"),
                "BL": ("B", "O"),
            },
        ),
    ],
)
def test_build_edge_map_default_solved(notation_order, color_order, expected_edges):
    # Arrange
    args = parse_args(["-n", notation_order, "-c", color_order])
    cube = create_cube(args)

    # Act
    edge_map = build_edge_map(cube, args)

    # Assert
    for edge, expected_colors in expected_edges.items():
        assert edge in edge_map, f"Missing edge {edge}"
        assert edge_map[edge] == expected_colors, (
            f"Edge {edge} incorrect: {edge_map[edge]} != {expected_colors}"
        )
