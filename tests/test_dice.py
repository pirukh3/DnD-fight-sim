"""Tests for the dice rolling module."""

from combat_sim.dice import (
    parse_dice_notation,
    roll,
    roll_d20,
    roll_dice,
    roll_notation,
)


def test_roll_within_range() -> None:
    """A single die roll should be between 1 and the number of sides."""
    for sides in [4, 6, 8, 10, 12, 20]:
        for _ in range(100):
            result = roll(sides)
            assert 1 <= result <= sides


def test_roll_d20_within_range() -> None:
    """d20 rolls should be between 1 and 20."""
    for _ in range(100):
        result = roll_d20()
        assert 1 <= result <= 20


def test_roll_dice_count() -> None:
    """roll_dice should return the correct number of results."""
    results = roll_dice(3, 6)
    assert len(results) == 3
    for r in results:
        assert 1 <= r <= 6


def test_parse_dice_notation_simple() -> None:
    """Parse a simple notation like '2d6'."""
    num, sides, mod = parse_dice_notation("2d6")
    assert num == 2
    assert sides == 6
    assert mod == 0


def test_parse_dice_notation_with_positive_modifier() -> None:
    """Parse notation with a positive modifier like '1d8+3'."""
    num, sides, mod = parse_dice_notation("1d8+3")
    assert num == 1
    assert sides == 8
    assert mod == 3


def test_parse_dice_notation_with_negative_modifier() -> None:
    """Parse notation with a negative modifier like '2d4-1'."""
    num, sides, mod = parse_dice_notation("2d4-1")
    assert num == 2
    assert sides == 4
    assert mod == -1


def test_roll_notation_returns_int() -> None:
    """roll_notation should return an integer."""
    result = roll_notation("2d6+3")
    assert isinstance(result, int)


def test_roll_notation_range() -> None:
    """roll_notation('1d6+2') should be between 3 and 8."""
    for _ in range(100):
        result = roll_notation("1d6+2")
        assert 3 <= result <= 8
