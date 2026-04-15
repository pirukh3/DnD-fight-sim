"""Combatant classes representing players and monsters in combat."""

from __future__ import annotations

from dataclasses import dataclass, field

from combat_sim.dice import parse_dice_notation, roll_d20, roll_dice


@dataclass
class AbilityScores:
    """The six core ability scores for a DnD character."""

    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    def modifier(self, ability: str) -> int:
        """Calculate the modifier for a given ability score.

        Args:
            ability: Name of the ability (e.g., 'strength').

        Returns:
            The ability modifier: (score - 10) // 2.
        """
        score = getattr(self, ability.lower())
        return (score - 10) // 2


@dataclass
class Attack:
    """Represents a single attack action.

    Attributes:
        name: Display name of the attack (e.g., 'Longsword').
        attack_bonus: Bonus added to the d20 attack roll.
        damage_dice: Damage dice notation (e.g., '1d8+3').
        damage_type: Type of damage dealt (e.g., 'slashing').
    """

    name: str
    attack_bonus: int
    damage_dice: str
    damage_type: str = "bludgeoning"


@dataclass
class Combatant:
    """A participant in combat (player character or monster).

    Attributes:
        name: Display name.
        max_hp: Maximum hit points.
        current_hp: Current hit points.
        armor_class: Armor class (difficulty to hit).
        abilities: The six ability scores.
        attacks: List of available attacks.
        initiative_bonus: Bonus to initiative rolls.
        is_player: Whether this combatant is a player character.
    """

    name: str
    max_hp: int
    armor_class: int
    abilities: AbilityScores = field(default_factory=AbilityScores)
    attacks: list[Attack] = field(default_factory=list)
    initiative_bonus: int = 0
    is_player: bool = True
    current_hp: int = -1

    def __post_init__(self) -> None:
        if self.current_hp < 0:
            self.current_hp = self.max_hp

    @property
    def is_alive(self) -> bool:
        """Check if the combatant is still alive (HP > 0)."""
        return self.current_hp > 0

    def take_damage(self, amount: int) -> int:
        """Apply damage to this combatant.

        Args:
            amount: Amount of damage to take.

        Returns:
            Actual damage applied (clamped so HP doesn't go below 0).
        """
        actual = min(amount, self.current_hp)
        self.current_hp -= actual
        return actual

    def heal(self, amount: int) -> int:
        """Heal this combatant.

        Args:
            amount: Amount of HP to restore.

        Returns:
            Actual HP restored (clamped so HP doesn't exceed max).
        """
        actual = min(amount, self.max_hp - self.current_hp)
        self.current_hp += actual
        return actual

    def roll_initiative(self) -> int:
        """Roll initiative for this combatant.

        Returns:
            The initiative roll result (d20 + initiative bonus).
        """
        return roll_d20() + self.initiative_bonus

    def make_attack_roll(self, attack: Attack) -> tuple[int, bool]:
        """Make an attack roll with the given attack.

        Args:
            attack: The attack to use.

        Returns:
            A tuple of (total_roll, is_critical_hit).
        """
        natural_roll = roll_d20()
        is_critical = natural_roll == 20
        total = natural_roll + attack.attack_bonus
        return total, is_critical

    def roll_damage(self, attack: Attack, critical: bool = False) -> int:
        """Roll damage for an attack.

        On a critical hit, damage dice are rolled twice but the
        modifier is only applied once (per DnD 5e rules).

        Args:
            attack: The attack being made.
            critical: Whether this is a critical hit.

        Returns:
            Total damage rolled.
        """
        num_dice, sides, modifier = parse_dice_notation(attack.damage_dice)
        damage = sum(roll_dice(num_dice, sides)) + modifier
        if critical:
            damage += sum(roll_dice(num_dice, sides))
        return max(damage, 0)


def create_player(
    name: str,
    hp: int,
    ac: int,
    attack_name: str,
    attack_bonus: int,
    damage_dice: str,
    damage_type: str = "slashing",
    abilities: AbilityScores | None = None,
    initiative_bonus: int = 0,
) -> Combatant:
    """Convenience factory to create a player character.

    Args:
        name: Character name.
        hp: Maximum hit points.
        ac: Armor class.
        attack_name: Name of the primary attack.
        attack_bonus: Attack roll bonus.
        damage_dice: Damage dice notation.
        damage_type: Type of damage.
        abilities: Ability scores (defaults to all 10s).
        initiative_bonus: Initiative modifier.

    Returns:
        A configured Combatant instance.
    """
    return Combatant(
        name=name,
        max_hp=hp,
        armor_class=ac,
        abilities=abilities or AbilityScores(),
        attacks=[Attack(attack_name, attack_bonus, damage_dice, damage_type)],
        initiative_bonus=initiative_bonus,
        is_player=True,
    )


def create_monster(
    name: str,
    hp: int,
    ac: int,
    attack_name: str,
    attack_bonus: int,
    damage_dice: str,
    damage_type: str = "slashing",
    abilities: AbilityScores | None = None,
    initiative_bonus: int = 0,
) -> Combatant:
    """Convenience factory to create a monster.

    Args:
        name: Monster name.
        hp: Maximum hit points.
        ac: Armor class.
        attack_name: Name of the primary attack.
        attack_bonus: Attack roll bonus.
        damage_dice: Damage dice notation.
        damage_type: Type of damage.
        abilities: Ability scores (defaults to all 10s).
        initiative_bonus: Initiative modifier.

    Returns:
        A configured Combatant instance.
    """
    return Combatant(
        name=name,
        max_hp=hp,
        armor_class=ac,
        abilities=abilities or AbilityScores(),
        attacks=[Attack(attack_name, attack_bonus, damage_dice, damage_type)],
        initiative_bonus=initiative_bonus,
        is_player=False,
    )
