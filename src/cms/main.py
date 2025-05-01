# src/cms/main.py

import argparse
from magiccube import Cube
import sys
from cms.utils import (
    build_edge_map,
    display_edge_map,
    build_corner_map,
    display_corner_map,
)


REQUIRED_NOTATION_LETTERS = set("ULFRBD")
REQUIRED_COLOR_LETTERS = set("WOGRBY")


def create_solved_cube(notation_order="ULFRBD", color_order="WOGRBY"):
    """
    Create a solved Cube based on notation order and color order.
    """

    # Map face to color
    center_colors = dict(zip(notation_order.upper(), color_order.upper()))

    # Faces in MagicCube's internal order: U, L, F, R, B, D
    faces_order = ["U", "L", "F", "R", "B", "D"]

    facelet_str = ""

    for face in faces_order:
        color = center_colors[face]
        facelet_str += color * 9  # 9 stickers per face

    # Create the cube and set the facelets
    cube = Cube()
    cube.set(facelet_str)

    return cube


def create_cube(args):
    if args.facelet_notation:
        s = args.facelet_notation
        not_order = args.notation_order.upper()
        # split into six 9-char chunks according to the user’s notation‐order
        chunks = {face: s[i * 9 : (i + 1) * 9] for i, face in enumerate(not_order)}
        # reassemble in MagicCube’s internal ULFRBD order
        internal = ["U", "L", "F", "R", "B", "D"]
        normalized = "".join(chunks[f] for f in internal)

        cube = Cube()
        cube.set(normalized)
        return cube

    # no facelets ⇒ build a fresh solved cube
    return create_solved_cube(args.notation_order, args.color_order)


def validate_facelet_notation(facelet: str) -> None:
    """Raises ValueError if the facelet string is invalid."""
    if len(facelet) != 54:
        raise ValueError(
            f"Facelet notation must be exactly 54 characters long. Got length {len(facelet)}."
        )


def validate_notation_order(order: str) -> None:
    """Raises ValueError if the notation order is invalid."""
    order_upper = order.upper()
    if len(order_upper) != 6 or set(order_upper) != REQUIRED_NOTATION_LETTERS:
        raise ValueError(
            f"Notation order must be exactly 6 characters long and a permutation of U, L, F, R, B, D. Got: '{order}'"
        )


def validate_color_order(order: str) -> None:
    """Raises ValueError if the color order is invalid."""
    order_upper = order.upper()
    if len(order_upper) != 6 or set(order_upper) != REQUIRED_COLOR_LETTERS:
        raise ValueError(
            f"Color order must be exactly 6 characters long and a permutation of W, O, G, R, B, Y. Got: '{order}'"
        )


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Rubik's Cube Notation Parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-f",
        "--facelet-notation",
        required=False,
        default=None,
        help="54-character facelet string (optional)",
    )

    parser.add_argument(
        "-n",
        "--notation-order",
        default="ULFRBD",
        help="Set the notation order (must be a permutation of 'U', 'L', 'F', 'R', 'B', 'D')",
    )

    parser.add_argument(
        "-c",
        "--color-order",
        default="WOGRBY",
        help="6-character color sequence for solved cube faces in notation-order",
    )

    parser.add_argument(
        "-m",
        "--moves",
        default=None,
        help="Optional space-separated moves, e.g. \"R U R' U'\"",
    )
    parser.add_argument(
        "-s",
        "--scramble",
        default=None,
        help="Optional space-separated scramble moves to apply to a solved cube before anything else",
    )
    args = parser.parse_args(argv)

    try:
        if args.facelet_notation:
            validate_facelet_notation(args.facelet_notation)
        validate_notation_order(args.notation_order)
        validate_color_order(args.color_order)
    except ValueError as e:
        parser.error(str(e))

    return args


def display_full_state(cube, args):
    """
    Print the cube, its edge map, and its corner map.
    """
    print(cube)
    edges = build_edge_map(cube, args)
    display_edge_map(edges)
    corners = build_corner_map(cube, args)
    display_corner_map(corners)


def main():
    try:
        args = parse_args()
        cube = create_cube(args)

        # 1) apply any scramble moves first
        if args.scramble:
            for sm in args.scramble.split():
                cube.rotate(sm)

        # 2) display the (possibly scrambled) initial state
        display_full_state(cube, args)
        if args.moves:
            for mv in args.moves.split():
                print(f"\nMove: {mv}")
                cube.rotate(mv)
                display_full_state(cube, args)

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
