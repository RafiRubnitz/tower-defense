# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tower Defense game built with Pygame. A grid-based game where players place towers to stop enemies from following a path.

## Running the Game

```bash
python run.py
```

**Controls:**
- `SPACE` - Pause/Unpause
- `R` - Restart game
- `Left Click` - Place towers on grass areas (not on path)
- Game over/victory screen has a restart button

## Architecture

### Core Structure

```
run.py          # Entry point - creates window (980x600) and Game instance
game.py         # Game class - main loop, event handling, rendering
map.py          # Map, Wave, Round classes - game logic, enemies, towers, bullets
tower.py        # Tower classes - tower behavior and rendering
enemy.py        # Enemy classes (Soldier) - enemy behavior and rendering
player.py       # Player class - holds money and lives (minimal)
database.py     # Database class - SQLite persistence for maps, stats, achievements
src/            # Utility modules
  - point.py    # Point class for 2D coordinates
  - direction.py# Direction enum with x/y properties
  - game_state.py# GameState enum
ui/
  - menu.py     # MenuManager - main menu, map selection, settings screens
```

### Grid System

- Map is 40x30 grid, each cell is 20x20 pixels (800x600 total map area)
- Window is 980x600 (map + 180px UI panel on right)
- Path is a list of PathField objects that enemies follow
- Towers can only be placed on grass (non-path) cells

### Game Flow

1. `Round` manages the overall game state (waves, towers, enemies, lives, money, score)
2. Each `Wave` spawns enemies and manages bullets
3. `Tower.update()` finds enemies in range and fires bullets
4. `Bullet.update()` moves toward target and deals damage on hit
5. Enemies follow the path; if they reach the end, player loses a life
6. Game ends when lives reach 0 (game over) or all waves completed (victory)

### Database (`database.py`)

SQLite database (`tower_defense.db`) stores:
- **maps** - Custom and built-in maps with path data
- **round_configs** - Game configuration (waves, starting money/lives, tower cost)
- **wave_configs** - Per-wave enemy composition and spawn rates
- **game_stats** - Play history and statistics
- **achievements** - Unlockable achievements
- **player_settings** - User preferences (difficulty, lives, money)

Built-in maps: Classic L-Path, Zigzag Challenge, Spiral Madness, Figure-8 Loop

### Key Classes

| Class | File | Responsibility |
|-------|------|----------------|
| `Game` | game.py | Main loop, clock, state management |
| `Round` | map.py | Game state, UI panel, tower placement, win/loss |
| `Wave` | map.py | Enemy spawning, bullet management |
| `Map` | map.py | Grid, path, mouse interaction for placement |
| `BasicTower` | tower.py | Tower with range=3.5, power=50, cooldown=600ms, cost=$100 |
| `Soldier` | enemy.py | Basic enemy with 100 HP, speed=2.0, bounty=$15 |
| `Bullet` | map.py | Projectile with speed=10 |
| `MenuManager` | ui/menu.py | Main menu, map selection, settings screens |

### Important Values

- Tower cost: $100
- Starting money: $450
- Starting lives: 10
- Total waves: 5
- Soldier bounty: $15
- Grid cell size: 20x20 pixels
- Tower range: 3.5 grid units (70 pixels)
- Bullet speed: 10 pixels/frame
- Game runs at 60 FPS
