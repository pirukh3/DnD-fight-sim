"""Tests for the combat encounter engine."""

from combat_sim.combat import CombatEncounter
from combat_sim.combatant import Attack, Combatant


def _make_combatant(
    name: str,
    hp: int,
    ac: int,
    attack_bonus: int,
    damage_dice: str,
    is_player: bool = True,
) -> Combatant:
    """Helper to create a simple combatant for testing."""
    return Combatant(
        name=name,
        max_hp=hp,
        armor_class=ac,
        attacks=[Attack("Test Attack", attack_bonus, damage_dice, "slashing")],
        is_player=is_player,
    )


def test_roll_initiative_sets_turn_order() -> None:
    """roll_initiative should populate turn_order with all combatants."""
    p = _make_combatant("Player", 20, 15, 5, "1d8+3", is_player=True)
    m = _make_combatant("Monster", 10, 12, 3, "1d6+1", is_player=False)
    encounter = CombatEncounter([p], [m])
    order = encounter.roll_initiative()
    assert len(order) == 2


def test_combat_ends_when_one_side_defeated() -> None:
    """Combat should end when all combatants on one side are defeated."""
    # Player with high attack vs. fragile monster
    p = _make_combatant("Player", 100, 1, 20, "10d10+50", is_player=True)
    m = _make_combatant("Monster", 1, 1, 0, "1d4", is_player=False)
    encounter = CombatEncounter([p], [m])
    winner = encounter.run()
    assert winner == "players"
    assert not m.is_alive


def test_monsters_can_win() -> None:
    """Monsters should be able to win if they are stronger."""
    p = _make_combatant("Player", 1, 1, 0, "1d4", is_player=True)
    m = _make_combatant("Monster", 100, 1, 20, "10d10+50", is_player=False)
    encounter = CombatEncounter([p], [m])
    winner = encounter.run()
    assert winner == "monsters"
    assert not p.is_alive


def test_get_summary_includes_all_combatants() -> None:
    """get_summary should mention every combatant."""
    p = _make_combatant("Hero", 20, 15, 5, "1d8+3", is_player=True)
    m = _make_combatant("Villain", 10, 12, 3, "1d6+1", is_player=False)
    encounter = CombatEncounter([p], [m])
    summary = encounter.get_summary()
    assert "Hero" in summary
    assert "Villain" in summary


def test_combat_log_is_populated() -> None:
    """After running combat, the log should contain entries."""
    p = _make_combatant("Player", 100, 1, 20, "10d10+50", is_player=True)
    m = _make_combatant("Monster", 1, 1, 0, "1d4", is_player=False)
    encounter = CombatEncounter([p], [m])
    encounter.run()
    assert len(encounter.log.entries) > 0


def test_multiple_combatants_per_side() -> None:
    """Combat should work with multiple combatants on each side."""
    players = [
        _make_combatant("P1", 50, 10, 10, "2d6+5", is_player=True),
        _make_combatant("P2", 50, 10, 10, "2d6+5", is_player=True),
    ]
    monsters = [
        _make_combatant("M1", 10, 10, 3, "1d6+1", is_player=False),
        _make_combatant("M2", 10, 10, 3, "1d6+1", is_player=False),
    ]
    encounter = CombatEncounter(players, monsters)
    winner = encounter.run()
    # Players should almost certainly win given the stat advantage
    assert winner in ("players", "monsters")


def test_max_rounds_limit() -> None:
    """Combat should stop after max_rounds even if nobody has won."""
    # Two combatants that can never hit each other (AC 99)
    p = _make_combatant("Player", 100, 99, 0, "1d4", is_player=True)
    m = _make_combatant("Monster", 100, 99, 0, "1d4", is_player=False)
    encounter = CombatEncounter([p], [m])
    winner = encounter.run(max_rounds=3)
    # Both should still be alive; combat is ongoing
    assert winner == "ongoing"
    assert encounter.round_number == 3
