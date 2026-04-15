"""Preset characters and monsters for quick combat setup."""

from combat_sim.combatant import (
    AbilityScores,
    Attack,
    Combatant,
    create_monster,
    create_player,
)


def fighter(name: str = "Fighter") -> Combatant:
    """Create a level-1 Fighter preset.

    A sturdy melee combatant with heavy armor and a longsword.
    """
    return create_player(
        name=name,
        hp=12,
        ac=18,
        attack_name="Longsword",
        attack_bonus=5,
        damage_dice="1d8+3",
        damage_type="slashing",
        abilities=AbilityScores(
            strength=16,
            dexterity=12,
            constitution=14,
            intelligence=10,
            wisdom=10,
            charisma=10,
        ),
        initiative_bonus=1,
    )


def rogue(name: str = "Rogue") -> Combatant:
    """Create a level-1 Rogue preset.

    A nimble combatant with a short sword and high dexterity.
    """
    return create_player(
        name=name,
        hp=10,
        ac=15,
        attack_name="Short Sword",
        attack_bonus=5,
        damage_dice="1d6+3",
        damage_type="piercing",
        abilities=AbilityScores(
            strength=10,
            dexterity=16,
            constitution=12,
            intelligence=14,
            wisdom=10,
            charisma=12,
        ),
        initiative_bonus=3,
    )


def wizard(name: str = "Wizard") -> Combatant:
    """Create a level-1 Wizard preset.

    A fragile spellcaster using fire bolt as a primary attack.
    """
    return create_player(
        name=name,
        hp=8,
        ac=12,
        attack_name="Fire Bolt",
        attack_bonus=5,
        damage_dice="1d10",
        damage_type="fire",
        abilities=AbilityScores(
            strength=8,
            dexterity=14,
            constitution=12,
            intelligence=16,
            wisdom=12,
            charisma=10,
        ),
        initiative_bonus=2,
    )


def cleric(name: str = "Cleric") -> Combatant:
    """Create a level-1 Cleric preset.

    A divine warrior with a mace and medium armor.
    """
    return create_player(
        name=name,
        hp=10,
        ac=16,
        attack_name="Mace",
        attack_bonus=4,
        damage_dice="1d6+2",
        damage_type="bludgeoning",
        abilities=AbilityScores(
            strength=14,
            dexterity=10,
            constitution=12,
            intelligence=10,
            wisdom=16,
            charisma=12,
        ),
        initiative_bonus=0,
    )


def goblin(name: str = "Goblin") -> Combatant:
    """Create a Goblin monster preset (CR 1/4)."""
    return create_monster(
        name=name,
        hp=7,
        ac=15,
        attack_name="Scimitar",
        attack_bonus=4,
        damage_dice="1d6+2",
        damage_type="slashing",
        abilities=AbilityScores(
            strength=8,
            dexterity=14,
            constitution=10,
            intelligence=10,
            wisdom=8,
            charisma=8,
        ),
        initiative_bonus=2,
    )


def skeleton(name: str = "Skeleton") -> Combatant:
    """Create a Skeleton monster preset (CR 1/4)."""
    return create_monster(
        name=name,
        hp=13,
        ac=13,
        attack_name="Shortsword",
        attack_bonus=4,
        damage_dice="1d6+2",
        damage_type="piercing",
        abilities=AbilityScores(
            strength=10,
            dexterity=14,
            constitution=10,
            intelligence=6,
            wisdom=8,
            charisma=5,
        ),
        initiative_bonus=2,
    )


def orc(name: str = "Orc") -> Combatant:
    """Create an Orc monster preset (CR 1/2)."""
    return create_monster(
        name=name,
        hp=15,
        ac=13,
        attack_name="Greataxe",
        attack_bonus=5,
        damage_dice="1d12+3",
        damage_type="slashing",
        abilities=AbilityScores(
            strength=16,
            dexterity=12,
            constitution=16,
            intelligence=7,
            wisdom=11,
            charisma=10,
        ),
        initiative_bonus=1,
    )


def dragon_wyrmling(name: str = "Dragon Wyrmling") -> Combatant:
    """Create a Young Red Dragon Wyrmling preset (CR 4).

    A powerful boss-type monster with a devastating bite attack.
    """
    return create_monster(
        name=name,
        hp=75,
        ac=17,
        attack_name="Bite",
        attack_bonus=6,
        damage_dice="2d10+4",
        damage_type="piercing",
        abilities=AbilityScores(
            strength=19,
            dexterity=10,
            constitution=17,
            intelligence=12,
            wisdom=11,
            charisma=15,
        ),
        initiative_bonus=0,
    )


# Convenient groupings for quick encounters
PRESET_PLAYERS = {
    "fighter": fighter,
    "rogue": rogue,
    "wizard": wizard,
    "cleric": cleric,
}

PRESET_MONSTERS = {
    "goblin": goblin,
    "skeleton": skeleton,
    "orc": orc,
    "dragon_wyrmling": dragon_wyrmling,
}
