# tests/test_scramble.py

import sys
import io
import pytest

from cms.main import main, parse_args, create_cube, display_full_state
from cms.utils import build_edge_map, display_edge_map, build_corner_map, display_corner_map

def capture_full_state_lines(cube, args):
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        display_full_state(cube, args)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue().rstrip("\n").splitlines()

@pytest.mark.parametrize("scramble", [
    "R",              # single move
    "R U R' U'",      # short sequence
])
def test_main_scramble_only(capsys, monkeypatch, scramble):
    # Run with just scramble
    monkeypatch.setattr(sys, "argv", ["prog", "-s", scramble])
    exit_code = main()
    assert exit_code == 0

    out = capsys.readouterr().out.rstrip("\n").splitlines()

    # Build expected: start solved, apply scramble, then display_full_state
    args = parse_args(["-s", scramble])
    cube = create_cube(args)
    # manually apply scramble in test
    for mv in scramble.split():
        cube.rotate(mv)

    expected = capture_full_state_lines(cube, args)
    assert out == expected

def test_main_scramble_then_moves(capsys, monkeypatch):
    # scramble then one move "F"
    scramble = "R U"
    mv = "F"
    monkeypatch.setattr(sys, "argv", ["prog", "-s", scramble, "-m", mv])
    exit_code = main()
    assert exit_code == 0

    out_lines = capsys.readouterr().out.rstrip("\n").splitlines()

    # initial scrambled state
    args0 = parse_args(["-s", scramble])
    cube0 = create_cube(args0)
    for sm in scramble.split():
        cube0.rotate(sm)
    init_lines = capture_full_state_lines(cube0, args0)

    # after one move
    args1 = parse_args(["-s", scramble])
    cube1 = create_cube(args1)
    for sm in scramble.split():
        cube1.rotate(sm)
    cube1.rotate(mv)
    after_lines = capture_full_state_lines(cube1, args1)

    # expected full sequence:
    expected = init_lines + ["", f"Move: {mv}"] + after_lines
    assert out_lines == expected
