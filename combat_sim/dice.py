"""Dice rolling utilities for DnD combat simulation."""

import random


def roll(sides: int) -> int:
    """Roll a single die with the given number of sides.

    Args:
        sides: Number of sides on the die (e.g., 20 for a d20).

    Returns:
        A random integer between 1 and sides (inclusive).
    """
    return random.randint(1, sides)


def roll_d20() -> int:
    """Roll a 20-sided die."""
    return roll(20)


def roll_dice(num_dice: int, sides: int) -> list[int]:
    """Roll multiple dice of the same type.

    Args:
        num_dice: Number of dice to roll.
        sides: Number of sides on each die.

    Returns:
        A list of individual die results.
    """
    return [roll(sides) for _ in range(num_dice)]


def parse_dice_notation(notation: str) -> tuple[int, int, int]:
    """Parse dice notation like '2d6+3' into components.

    Args:
        notation: A string in the format 'NdS' or 'NdS+M' or 'NdS-M'
                  where N=number of dice, S=sides, M=modifier.

    Returns:
        A tuple of (num_dice, sides, modifier).
    """
    modifier = 0
    if "+" in notation:
        dice_part, mod_part = notation.split("+")
        modifier = int(mod_part)
    elif "-" in notation:
        dice_part, mod_part = notation.split("-")
        modifier = -int(mod_part)
    else:
        dice_part = notation

    num_dice, sides = dice_part.lower().split("d")
    return int(num_dice), int(sides), modifier


def roll_notation(notation: str) -> int:
    """Roll dice based on standard notation (e.g., '2d6+3').

    Args:
        notation: Dice notation string.

    Returns:
        Total result of the roll.
    """
    num_dice, sides, modifier = parse_dice_notation(notation)
    rolls = roll_dice(num_dice, sides)
    return sum(rolls) + modifier
