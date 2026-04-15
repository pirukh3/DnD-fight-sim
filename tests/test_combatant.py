"""Tests for the combatant module."""

from combat_sim.combatant import (
    AbilityScores,
    Attack,
    Combatant,
    create_monster,
    create_player,
)


def test_ability_modifier() -> None:
    """Ability modifiers should follow the (score - 10) // 2 formula."""
    abilities = AbilityScores(strength=16, dexterity=8, constitution=10)
    assert abilities.modifier("strength") == 3
    assert abilities.modifier("dexterity") == -1
    assert abilities.modifier("constitution") == 0


def test_combatant_starts_at_max_hp() -> None:
    """A combatant's current HP should default to max HP."""
    c = Combatant(name="Test", max_hp=20, armor_class=15)
    assert c.current_hp == 20


def test_take_damage() -> None:
    """take_damage should reduce HP and return actual damage dealt."""
    c = Combatant(name="Test", max_hp=20, armor_class=15)
    actual = c.take_damage(5)
    assert actual == 5
    assert c.current_hp == 15


def test_take_damage_does_not_go_below_zero() -> None:
    """HP should not drop below 0."""
    c = Combatant(name="Test", max_hp=10, armor_class=15)
    actual = c.take_damage(25)
    assert actual == 10
    assert c.current_hp == 0


def test_is_alive() -> None:
    """is_alive should be True when HP > 0 and False when HP == 0."""
    c = Combatant(name="Test", max_hp=10, armor_class=15)
    assert c.is_alive is True
    c.take_damage(10)
    assert c.is_alive is False


def test_heal() -> None:
    """heal should restore HP up to max."""
    c = Combatant(name="Test", max_hp=20, armor_class=15)
    c.take_damage(10)
    actual = c.heal(5)
    assert actual == 5
    assert c.current_hp == 15


def test_heal_does_not_exceed_max() -> None:
    """Healing should not push HP above max_hp."""
    c = Combatant(name="Test", max_hp=20, armor_class=15)
    c.take_damage(5)
    actual = c.heal(100)
    assert actual == 5
    assert c.current_hp == 20


def test_roll_initiative_returns_int() -> None:
    """roll_initiative should return an integer."""
    c = Combatant(name="Test", max_hp=10, armor_class=15, initiative_bonus=2)
    result = c.roll_initiative()
    assert isinstance(result, int)
    assert result >= 3  # minimum: 1 + 2


def test_make_attack_roll() -> None:
    """make_attack_roll should return a tuple of (int, bool)."""
    c = Combatant(
        name="Test",
        max_hp=10,
        armor_class=15,
        attacks=[Attack("Sword", 5, "1d8+3", "slashing")],
    )
    total, is_crit = c.make_attack_roll(c.attacks[0])
    assert isinstance(total, int)
    assert isinstance(is_crit, bool)


def test_roll_damage_returns_positive() -> None:
    """Damage rolls should always be >= 0."""
    c = Combatant(
        name="Test",
        max_hp=10,
        armor_class=15,
        attacks=[Attack("Sword", 5, "1d8+3", "slashing")],
    )
    for _ in range(100):
        damage = c.roll_damage(c.attacks[0])
        assert damage >= 0


def test_create_player() -> None:
    """create_player should return a player combatant."""
    p = create_player("Hero", 20, 16, "Sword", 5, "1d8+3")
    assert p.name == "Hero"
    assert p.max_hp == 20
    assert p.armor_class == 16
    assert p.is_player is True
    assert len(p.attacks) == 1


def test_create_monster() -> None:
    """create_monster should return a non-player combatant."""
    m = create_monster("Goblin", 7, 15, "Scimitar", 4, "1d6+2")
    assert m.name == "Goblin"
    assert m.is_player is False
