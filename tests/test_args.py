# tests/test_args.py

import pytest
from pytest import raises
from cms.main import parse_args


def test_facelet_notation_defaults_to_none():
    args = parse_args([])
    assert args.facelet_notation is None


def test_facelet_notation_default_parsing():
    args = parse_args(["-f", "W" * 54])  # <- Added dummy facelet
    assert args.facelet_notation == "W" * 54


def test_default_notation_order():
    args = parse_args(["-f", "W" * 54])  # <- Added dummy facelet
    assert args.notation_order == "ULFRBD"


def test_custom_notation_order_short_flag():
    args = parse_args(["-n", "URFDLB"])
    assert args.notation_order == "URFDLB", (
        "Notation order should update to 'URFDLB' with -n flag"
    )


def test_custom_notation_order_long_flag():
    args = parse_args(["--notation-order", "DLBURF"])
    assert args.notation_order == "DLBURF", (
        "Notation order should update to 'DLBURF' with --notation-order flag"
    )


def test_invalid_notation_order_repeated_letter():
    with pytest.raises(SystemExit):
        parse_args(["-n", "UUUUUU"])  # Invalid: repeated letters


def test_invalid_notation_order_wrong_letters():
    with pytest.raises(SystemExit):
        parse_args(["-n", "ABCDEF"])  # Invalid: wrong letters


def test_invalid_notation_order_missing_letter():
    with pytest.raises(SystemExit):
        parse_args(["-n", "ULFRB"])  # Invalid: missing D
