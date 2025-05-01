import pytest
from cms.main import (
    validate_facelet_notation,
    validate_notation_order,
    validate_color_order,
)


@pytest.mark.parametrize(
    "valid_facelet",
    [
        "W" * 54,  # 54 whites
        "WOGRBY" * 9,  # correct, 6 * 9 = 54
        "ABCDEFGHIJKLMNO" * 3 + "PQRSTUVWX",  # correct 54
    ],
)
def test_valid_facelet_notation_cases(valid_facelet):
    validate_facelet_notation(valid_facelet)


@pytest.mark.parametrize(
    "invalid_facelet",
    [
        "",  # empty
        "W" * 53,  # too short
        "W" * 55,  # too long
        "123",  # way too short
        "WOGRBY",  # too short
    ],
)
def test_invalid_facelet_notation_cases(invalid_facelet):
    with pytest.raises(ValueError):
        validate_facelet_notation(invalid_facelet)


@pytest.mark.parametrize(
    "valid_notation_order",
    [
        "ULFRBD",
        "URFDLB",
        "DLBURF",
        "BDFLUR",
        "lfurbd",  # lowercase should be accepted
    ],
)
def test_valid_notation_order_cases(valid_notation_order):
    validate_notation_order(valid_notation_order)


@pytest.mark.parametrize(
    "invalid_notation_order",
    [
        "UUUUUU",  # repeated letters
        "ULFRB",  # too short
        "ULFRBDU",  # too long
        "ABCDEF",  # wrong letters
        "ULFRB1",  # non-letter character
        "ULFRBG",  # wrong letter (G instead of D)
    ],
)
def test_invalid_notation_order_cases(invalid_notation_order):
    with pytest.raises(ValueError):
        validate_notation_order(invalid_notation_order)


@pytest.mark.parametrize(
    "valid_color_order",
    [
        "WOGRBY",
        "WORBYG",
        "YBGRWO",
        "gowrby",  # lowercase accepted
    ],
)
def test_valid_color_order_cases(valid_color_order):
    validate_color_order(valid_color_order)


@pytest.mark.parametrize(
    "invalid_color_order",
    [
        "WWWWWW",  # repeated letters
        "WOGRB",  # too short
        "WOGRBYG",  # too long
        "ABCDEF",  # wrong letters
        "WOGRB1",  # non-letter character
        "WOGRBZ",  # invalid letter Z
    ],
)
def test_invalid_color_order_cases(invalid_color_order):
    with pytest.raises(ValueError):
        validate_color_order(invalid_color_order)
