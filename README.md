# Tower Defense

A classic tower defense game built with Pygame. Place towers along the enemy path to defend against waves of attackers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)

## Features

- **4 Built-in Maps**: Classic L-Path, Zigzag Challenge, Spiral Madness, and Figure-8 Loop
- **Wave-based Gameplay**: Survive 5 waves of increasingly difficult enemies
- **Tower Strategy**: Place towers strategically to maximize damage output
- **Settings**: Customize starting money, lives, and difficulty
- **High Scores**: Track your best runs
- **Achievements**: Unlock achievements as you play

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RafiRubnitz/tower-defense.git
cd tower-defense
```

2. Install dependencies:
```bash
pip install pygame
```

## Running the Game

```bash
python run.py
```

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Pause/Unpause game |
| `R` | Restart game |
| `Left Click` | Place tower |
| `Mouse` | Select menu options |

## Gameplay

### Objective
Prevent enemies from reaching the end of the path. Each enemy that escapes reduces your lives. Survive all 5 waves to win!

### Tower Placement
- Click on grass areas to place towers
- Towers cannot be placed on the path
- Each tower costs $100
- Towers automatically fire at enemies within range

### Economy
- **Starting Money**: $450
- **Tower Cost**: $100
- **Enemy Bounty**: $15 per kill
- **Starting Lives**: 10

### Waves
| Wave | Enemies | Spawn Interval |
|------|---------|----------------|
| 1 | 5 | 60 frames |
| 2 | 8 | 55 frames |
| 3 | 11 | 50 frames |
| 4 | 14 | 45 frames |
| 5 | 17 | 40 frames |

## Project Structure

```
tower-defense/
├── run.py              # Entry point
├── game.py             # Main game loop
├── map.py              # Map, Wave, Round classes
├── tower.py            # Tower classes
├── enemy.py            # Enemy classes
├── player.py           # Player class
├── database.py         # SQLite database management
├── src/
│   ├── point.py        # Point utility class
│   ├── direction.py    # Direction enum
│   └── game_state.py   # GameState enum
└── ui/
    └── menu.py         # Menu system
```

## Database

The game uses SQLite (`tower_defense.db`) to store:
- Custom maps
- Game statistics
- High scores
- Achievements
- Player settings

## License

MIT License
