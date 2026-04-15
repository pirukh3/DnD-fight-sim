#!/usr/bin/env python3
"""Main entry point for the DnD Fight Simulator.

Run a sample combat encounter between a party of adventurers and a group
of monsters, printing the full combat log to the console.
"""

from combat_sim.combat import CombatEncounter
from combat_sim.presets import (
    dragon_wyrmling,
    fighter,
    goblin,
    orc,
    rogue,
    skeleton,
    wizard,
)


def run_party_vs_monsters() -> None:
    """Run a classic party vs. monsters encounter."""
    print("=" * 60)
    print("  DnD Fight Simulator - Party vs. Monsters")
    print("=" * 60)
    print()

    players = [
        fighter("Aldric the Bold"),
        rogue("Lyra Shadowstep"),
        wizard("Elminster"),
    ]

    monsters = [
        orc("Grokk"),
        goblin("Snik"),
        goblin("Snok"),
        skeleton("Bone Rattler"),
    ]

    print("PLAYERS:")
    for p in players:
        print(
            f"  {p.name} - HP: {p.max_hp}, AC: {p.armor_class}, "
            f"Attack: {p.attacks[0].name} (+{p.attacks[0].attack_bonus}, "
            f"{p.attacks[0].damage_dice} {p.attacks[0].damage_type})"
        )
    print()

    print("MONSTERS:")
    for m in monsters:
        print(
            f"  {m.name} - HP: {m.max_hp}, AC: {m.armor_class}, "
            f"Attack: {m.attacks[0].name} (+{m.attacks[0].attack_bonus}, "
            f"{m.attacks[0].damage_dice} {m.attacks[0].damage_type})"
        )
    print()

    encounter = CombatEncounter(players, monsters)
    winner = encounter.run()

    print(encounter.log)
    print()

    if winner == "players":
        print("The adventurers emerge victorious!")
    elif winner == "monsters":
        print("The monsters have triumphed...")
    else:
        print("The battle ends in a stalemate!")


def run_boss_fight() -> None:
    """Run a boss fight: full party vs. a dragon wyrmling."""
    print()
    print("=" * 60)
    print("  DnD Fight Simulator - Boss Fight!")
    print("=" * 60)
    print()

    players = [
        fighter("Aldric the Bold"),
        rogue("Lyra Shadowstep"),
        wizard("Elminster"),
    ]

    monsters = [dragon_wyrmling("Ember the Wyrmling")]

    print("PLAYERS:")
    for p in players:
        print(
            f"  {p.name} - HP: {p.max_hp}, AC: {p.armor_class}, "
            f"Attack: {p.attacks[0].name} (+{p.attacks[0].attack_bonus}, "
            f"{p.attacks[0].damage_dice} {p.attacks[0].damage_type})"
        )
    print()

    print("BOSS:")
    m = monsters[0]
    print(
        f"  {m.name} - HP: {m.max_hp}, AC: {m.armor_class}, "
        f"Attack: {m.attacks[0].name} (+{m.attacks[0].attack_bonus}, "
        f"{m.attacks[0].damage_dice} {m.attacks[0].damage_type})"
    )
    print()

    encounter = CombatEncounter(players, monsters)
    winner = encounter.run()

    print(encounter.log)
    print()

    if winner == "players":
        print("The dragon has been slain!")
    elif winner == "monsters":
        print("The dragon devours the adventurers...")
    else:
        print("The battle ends in a stalemate!")


if __name__ == "__main__":
    run_party_vs_monsters()
    run_boss_fight()
