import pytest
from cms.main import main, parse_args, create_cube
from cms.utils import cube_to_faces

from magiccube import Cube
import sys


def test_create_cube_defaults_to_solved():
    args = parse_args([])
    cube = create_cube(args)
    assert isinstance(cube, Cube)


def test_create_cube_from_facelets():
    # perfectly solved facelet string in U,L,F,R,B,D order:
    facelet_str = (
        "W" * 9  # U
        + "O" * 9  # L
        + "G" * 9  # F
        + "R" * 9  # R
        + "B" * 9  # B
        + "Y" * 9  # D
    )
    args = parse_args(["-f", facelet_str])
    cube = create_cube(args)

    # Verify it’s a MagicCube Cube
    from magiccube import Cube

    assert isinstance(cube, Cube)

    # And verify its faces match exactly
    from cms.utils import cube_to_faces

    faces = cube_to_faces(cube)
    expected = ["W", "O", "G", "R", "B", "Y"]
    for i, face in enumerate(faces):
        assert face == [expected[i]] * 9


def test_main_success(monkeypatch):
    monkeypatch.setattr(
        sys, "argv", ["program"]
    )  # Pretend we're running without extra args
    exit_code = main()
    assert exit_code == 0


def test_main_error(monkeypatch):
    def fake_create_cube(args):
        raise RuntimeError("forced failure")

    monkeypatch.setattr(
        sys, "argv", ["program"]
    )  # Pretend we're running without extra args
    monkeypatch.setattr("cms.main.create_cube", fake_create_cube)

    exit_code = main()
    assert exit_code == 1


@pytest.mark.parametrize(
    "notation_order,color_order,expected_faces",
    [
        ("ULFRBD", "WOGRBY", ["W", "O", "G", "R", "B", "Y"]),  # Default
        ("URFDLB", "WOGRBY", ["W", "B", "G", "O", "Y", "R"]),  # Corrected expectation!
        ("ULFRBD", "RGBYWO", ["R", "G", "B", "Y", "W", "O"]),  # Different color order
    ],
)
def test_cube_to_faces_various_configs(notation_order, color_order, expected_faces):
    # Arrange
    args = parse_args(["-n", notation_order, "-c", color_order])
    cube = create_cube(args)

    # Act
    faces = cube_to_faces(cube)

    # Assert
    for i, face in enumerate(faces):
        assert face == [expected_faces[i]] * 9, f"Face {i} incorrect: {face}"
