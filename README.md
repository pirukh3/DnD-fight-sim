# DnD Fight Simulator

A Dungeons & Dragons combat encounter simulator. Model characters, monsters, and spells, then run automated fight simulations to analyze outcomes and test party compositions.

## Features

- **Ability Scores & Modifiers** – Full six-stat ability score system with automatic modifier calculation
- **Attack Rolls** – d20-based attack rolls with attack bonuses vs. Armor Class
- **Critical Hits** – Natural 20s deal double damage dice
- **Damage Calculation** – Flexible dice notation parser (e.g., `2d6+3`) for damage rolls
- **Hit Point Tracking** – Real-time HP tracking with damage and healing support
- **Initiative System** – d20 initiative rolls to determine turn order
- **Combat Logging** – Detailed round-by-round combat log
- **Preset Characters** – Ready-to-use player classes (Fighter, Rogue, Wizard, Cleric) and monsters (Goblin, Skeleton, Orc, Dragon Wyrmling)

## Quick Start

```bash
# Run a sample combat encounter
python main.py

# Run the test suite
python -m pytest tests/ -v
```

## Project Structure

```
DnD-fight-sim/
├── combat_sim/           # Combat simulation engine
│   ├── __init__.py       # Package metadata
│   ├── dice.py           # Dice rolling utilities and notation parser
│   ├── combatant.py      # Player/monster classes with stats and attacks
│   ├── combat.py         # Combat encounter engine
│   └── presets.py        # Pre-built characters and monsters
├── tests/                # Unit and integration tests
│   ├── test_dice.py      # Dice module tests
│   ├── test_combatant.py # Combatant module tests
│   └── test_combat.py    # Combat engine tests
├── src/                  # Future application source code
│   ├── models/           # Data models (characters, monsters, spells, items)
│   ├── combat/           # Combat engine (initiative, attacks, damage, AI)
│   ├── utils/            # Shared utilities (dice rolling, logging, config)
│   └── ui/               # User interface (CLI/GUI)
├── docs/                 # Project documentation and design notes
├── assets/               # Static assets
│   ├── data/             # Game data files (monster stats, spell lists, etc.)
│   └── images/           # Optional images (maps, tokens, icons)
├── config/               # Configuration files for simulation settings
└── main.py               # Entry point with sample encounters
```

## Usage Example

```python
from combat_sim.combat import CombatEncounter
from combat_sim.presets import fighter, goblin, orc

# Create combatants
players = [fighter("Aldric")]
monsters = [goblin("Snik"), orc("Grokk")]

# Run the encounter
encounter = CombatEncounter(players, monsters)
winner = encounter.run()
print(encounter.log)
```

## Contributing

_Coming soon._

## License

_TBD_
