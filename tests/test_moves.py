# tests/test_moves.py

import sys
import io


from cms.main import main, parse_args, create_cube
from cms.utils import (
    build_edge_map,
    display_edge_map,
    build_corner_map,
    display_corner_map,
)

def capture_full_state_lines(cube, args):
    """
    Helper to capture the lines printed by:
       print(cube)
       display_edge_map(...)
       display_corner_map(...)
    """
    buf = io.StringIO()
    # swap in our buffer
    old = sys.stdout
    sys.stdout = buf
    try:
        # 1) cube ASCII
        print(cube)
        # 2) edges
        display_edge_map(build_edge_map(cube, args))
        # 3) corners
        display_corner_map(build_corner_map(cube, args))
    finally:
        sys.stdout = old
    return buf.getvalue().rstrip("\n").splitlines()


def test_main_no_moves_prints_full_state(capsys, monkeypatch):
    # No args: should print cube + edges + corners
    monkeypatch.setattr(sys, "argv", ["prog"])
    exit_code = main()
    assert exit_code == 0

    out_lines = capsys.readouterr().out.rstrip("\n").splitlines()

    args = parse_args([])
    cube = create_cube(args)
    expected = capture_full_state_lines(cube, args)

    assert out_lines == expected


def test_main_single_move_prints_initial_and_each_step(capsys, monkeypatch):
    # Simulate one move: R
    monkeypatch.setattr(sys, "argv", ["prog", "-m", "R"])
    exit_code = main()
    assert exit_code == 0

    # Capture actual output lines
    out_lines = capsys.readouterr().out.rstrip("\n").splitlines()

    # 1) Initial full state (cube + edges + corners)
    args0 = parse_args([])
    cube0 = create_cube(args0)
    initial_lines = capture_full_state_lines(cube0, args0)

    # 2) Full state AFTER the single R move
    args1 = parse_args([])
    cube1 = create_cube(args1)
    cube1.rotate("R")
    after_lines = capture_full_state_lines(cube1, args1)

    # Build exactly what we expect main() to emit:
    #   [initial lines]
    #   ""            ← blank line from print("\nMove: R")
    #   "Move: R"
    #   [after lines]
    expected = initial_lines + ["", "Move: R"] + after_lines

    assert out_lines == expected
