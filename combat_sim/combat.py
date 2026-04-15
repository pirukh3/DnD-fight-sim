"""Combat engine that runs turn-based DnD combat encounters."""

from __future__ import annotations

from dataclasses import dataclass, field

from combat_sim.combatant import Combatant


@dataclass
class CombatLog:
    """Stores a log of all events that occur during combat."""

    entries: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        """Add a message to the combat log."""
        self.entries.append(message)

    def __str__(self) -> str:
        return "\n".join(self.entries)


class CombatEncounter:
    """Manages a full combat encounter between two groups of combatants.

    Attributes:
        players: List of player combatants.
        monsters: List of monster combatants.
        turn_order: Initiative-sorted list of all combatants.
        round_number: Current round of combat.
        log: Record of all combat events.
    """

    def __init__(
        self, players: list[Combatant], monsters: list[Combatant]
    ) -> None:
        self.players = list(players)
        self.monsters = list(monsters)
        self.turn_order: list[tuple[int, Combatant]] = []
        self.round_number = 0
        self.log = CombatLog()

    def roll_initiative(self) -> list[tuple[int, Combatant]]:
        """Roll initiative for all combatants and determine turn order.

        Returns:
            Sorted list of (initiative_roll, combatant) tuples,
            highest first.
        """
        self.turn_order = []
        all_combatants = self.players + self.monsters
        for combatant in all_combatants:
            init_roll = combatant.roll_initiative()
            self.turn_order.append((init_roll, combatant))
            self.log.add(f"  {combatant.name} rolls initiative: {init_roll}")

        # Sort by initiative descending
        self.turn_order.sort(key=lambda x: x[0], reverse=True)

        self.log.add("\nInitiative Order:")
        for init_val, combatant in self.turn_order:
            self.log.add(f"  {init_val}: {combatant.name}")
        self.log.add("")

        return self.turn_order

    def _select_target(self, attacker: Combatant) -> Combatant | None:
        """Select a living target from the opposing side.

        Args:
            attacker: The combatant making the attack.

        Returns:
            A living enemy combatant, or None if all enemies are dead.
        """
        if attacker.is_player:
            enemies = self.monsters
        else:
            enemies = self.players

        living_enemies = [e for e in enemies if e.is_alive]
        if not living_enemies:
            return None

        # Target the enemy with the lowest current HP
        return min(living_enemies, key=lambda e: e.current_hp)

    def _resolve_attack(
        self, attacker: Combatant, defender: Combatant
    ) -> None:
        """Resolve a single attack from attacker against defender.

        Args:
            attacker: The combatant making the attack.
            defender: The combatant being attacked.
        """
        if not attacker.attacks:
            self.log.add(f"  {attacker.name} has no attacks available!")
            return

        attack = attacker.attacks[0]  # Use primary attack
        attack_roll, is_critical = attacker.make_attack_roll(attack)

        if is_critical:
            damage = attacker.roll_damage(attack, critical=True)
            actual_damage = defender.take_damage(damage)
            self.log.add(
                f"  {attacker.name} attacks {defender.name} with "
                f"{attack.name}: CRITICAL HIT! "
                f"Deals {actual_damage} {attack.damage_type} damage. "
                f"({defender.name}: {defender.current_hp}/{defender.max_hp} HP)"
            )
        elif attack_roll >= defender.armor_class:
            damage = attacker.roll_damage(attack, critical=False)
            actual_damage = defender.take_damage(damage)
            self.log.add(
                f"  {attacker.name} attacks {defender.name} with "
                f"{attack.name}: {attack_roll} vs AC {defender.armor_class} "
                f"- HIT! Deals {actual_damage} {attack.damage_type} damage. "
                f"({defender.name}: {defender.current_hp}/{defender.max_hp} HP)"
            )
        else:
            self.log.add(
                f"  {attacker.name} attacks {defender.name} with "
                f"{attack.name}: {attack_roll} vs AC {defender.armor_class} "
                f"- MISS!"
            )

        if not defender.is_alive:
            self.log.add(f"  >>> {defender.name} has been defeated! <<<")

    def _is_combat_over(self) -> bool:
        """Check if combat has ended (one side fully defeated).

        Returns:
            True if all players or all monsters are dead.
        """
        players_alive = any(p.is_alive for p in self.players)
        monsters_alive = any(m.is_alive for m in self.monsters)
        return not players_alive or not monsters_alive

    def run_round(self) -> bool:
        """Run a single round of combat.

        Each living combatant takes a turn in initiative order.

        Returns:
            True if combat is still ongoing, False if it has ended.
        """
        self.round_number += 1
        self.log.add(f"=== Round {self.round_number} ===")

        for _init, combatant in self.turn_order:
            if not combatant.is_alive:
                continue

            target = self._select_target(combatant)
            if target is None:
                break

            self._resolve_attack(combatant, target)

            if self._is_combat_over():
                break

        self.log.add("")
        return not self._is_combat_over()

    def get_winner(self) -> str:
        """Determine which side won the combat.

        Returns:
            'players', 'monsters', or 'ongoing' if combat hasn't ended.
        """
        players_alive = any(p.is_alive for p in self.players)
        monsters_alive = any(m.is_alive for m in self.monsters)

        if players_alive and not monsters_alive:
            return "players"
        elif monsters_alive and not players_alive:
            return "monsters"
        return "ongoing"

    def get_summary(self) -> str:
        """Get a summary of the current state of all combatants.

        Returns:
            A formatted string with each combatant's HP status.
        """
        lines = ["--- Combat Summary ---"]
        lines.append("Players:")
        for p in self.players:
            status = "ALIVE" if p.is_alive else "DEFEATED"
            lines.append(
                f"  {p.name}: {p.current_hp}/{p.max_hp} HP [{status}]"
            )
        lines.append("Monsters:")
        for m in self.monsters:
            status = "ALIVE" if m.is_alive else "DEFEATED"
            lines.append(
                f"  {m.name}: {m.current_hp}/{m.max_hp} HP [{status}]"
            )
        return "\n".join(lines)

    def run(self, max_rounds: int = 100) -> str:
        """Run the full combat encounter to completion.

        Args:
            max_rounds: Maximum number of rounds before forcing a draw.

        Returns:
            The winner ('players', 'monsters', or 'ongoing' if max rounds hit).
        """
        self.log.add("*** COMBAT BEGINS ***\n")
        self.log.add("Rolling Initiative...")
        self.roll_initiative()

        while self.round_number < max_rounds:
            still_going = self.run_round()
            if not still_going:
                break

        winner = self.get_winner()
        self.log.add("*** COMBAT ENDS ***\n")

        if winner == "players":
            self.log.add("VICTORY! The players are triumphant!")
        elif winner == "monsters":
            self.log.add("DEFEAT! The monsters have won!")
        else:
            self.log.add(
                f"STALEMATE! Combat ended after {max_rounds} rounds."
            )

        self.log.add("")
        self.log.add(self.get_summary())
        return winner
