# Architecture Analysis - Tower Defense Game

**Scope:** Current technical architecture, design patterns, and system boundaries

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Pygame Window (980x600)              │
├─────────────────────────────┬──────────────────────────┤
│                             │   UI Panel               │
│    Game Area (800x600)      │  Tower Selector         │
│    Grid 40x30 cells         │  Stats Display          │
│    Map + Enemies + Towers   │  Info Display           │
│                             │                         │
└─────────────────────────────┴──────────────────────────┘
           ↑
      GameState

┌──────────────────────────────────────────────┐
│          Game Loop (60 FPS)                  │
├──────────────────────────────────────────────┤
│  1. Handle Events (MenuManager or Round)    │
│  2. Update State (if playing Round)         │
│  3. Render Graphics (Pygame)                │
│  4. Sleep (16ms per frame)                  │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│      Data Layer (SQLite Database)           │
├──────────────────────────────────────────────┤
│  • Maps & Paths                             │
│  • Round Configurations                     │
│  • Wave Compositions                        │
│  • Game Statistics & Achievements           │
│  • Player Settings                          │
└──────────────────────────────────────────────┘
```

## Core Class Hierarchy

### Game State Machine
```
GameState (Enum - src/game_state.py)
├── MAIN_MENU
├── MAP_SELECTION
├── SETTINGS
├── PLAYING
├── PAUSED
├── GAME_OVER
└── VICTORY
```

### Core Game Classes

**Game** (game.py)
- Owns the main loop and Pygame window
- Routes events to MenuManager or current Round
- Manages GameState transitions
- Owned by: run.py
- Owns: MenuManager, Optional[Round]

**MenuManager** (ui/menu.py)
- Renders all menu screens (Main Menu, Map Selection, Settings)
- Handles menu input
- Calls Game.start_game_from_menu() when map selected
- Database access: reads maps, player settings

**Round** (map.py)
- Game session container (one map + player + waves)
- Owns: Map, Player, List[Wave], enemies, bullets
- Manages turn-by-turn game logic
- Tracks lives, money, score, wave progress
- Rendering: draws map, towers, enemies, bullets, UI panel

**Wave** (map.py)
- Enemy spawning controller for one wave
- Owns: List[Enemy], List[Bullet]
- Manages wave composition (enemy count, types, spawn timing)
- Called each frame by Round.update()

**Map** (map.py)
- Handles grid and path data
- Tracks grass cells for tower placement
- Manages mouse input for tower placement/selling
- No AI - purely data structure + placement logic

### Tower System

**Tower** (tower.py → tower base class, imports from towers/)
- Abstract tower with: position, range, cooldown, target tracking
- Subclasses in towers/ directory:
  - BasicTower: standard attack
  - FreezeTower: slows enemies
  - LaserTower: piercing attacks
  - Each has distinct damage, cooldown, cost

**Bullet** (map.py)
- Projectile with velocity, target, damage
- Handles collision detection and damage application
- Simple rectangular collision box

### Enemy System

**Enemy** (enemy.py → enemy base class, imports from enemies/)
- Abstract enemy with: position, health, speed, path following
- Subclasses in enemies/ directory:
  - Soldier: basic balanced enemy
  - Tank: high health, slow
  - Scout: fast, low health
  - Healer: supports other enemies
  - ArmoredSoldier: resists damage
  - Boss: high health, high bounty

**Player** (player.py)
- Minimal class: tracks money, lives
- No complex logic - pure data container

## Data Flow Patterns

### Tower Placement Flow
```
Map.mouse_interaction()
    ↓
Check cell is grass
    ↓
Deduct cost from Player.money
    ↓
Create tower instance
    ↓
Round.towers.append(tower)
    ↓
Each frame: Tower.update() finds targets and fires
```

### Enemy Spawning Flow
```
Wave.update() each frame
    ↓
Check spawn timer
    ↓
Create enemy based on wave_config
    ↓
Round.enemies.append(enemy)
    ↓
Each frame: Enemy.update() moves along path, takes damage
```

### Victory/Defeat Flow
```
Round.update()
    ↓
Check: All waves completed? → VICTORY
Check: Lives ≤ 0? → GAME_OVER
Check: Current wave complete? → Advance to next
Check: All enemies dead & wave time passed? → Spawn next
```

## Database Schema

**Key Tables:**
- **maps** - Map data with path, grid, metadata
- **round_configs** - Game settings (starting money, lives, tower costs)
- **wave_configs** - Per-map wave composition
- **game_stats** - Play history, leaderboard data
- **achievements** - Unlockable achievements
- **player_settings** - User preferences, difficulty choice

*Note: database.py is 30KB (large), contains ~500 lines of SQL logic*

## Key Design Decisions

### 1. Modular Tower/Enemy Structure
- **Why:** Allow easy addition of new tower/enemy types
- **How:** Each type is a separate file (towers/basic.py, enemies/soldier.py, etc.)
- **Trade-off:** More files, but cleaner class organization

### 2. Wave as Spawner
- **Why:** Decouple enemy spawning from Round game logic
- **How:** Wave owns enemies and bullets, Round queries them
- **Trade-off:** Wave class is large (~800 lines), handles many responsibilities

### 3. SQLite Persistence
- **Why:** Persistent map library, statistics tracking, settings storage
- **How:** Database accessed at game start/end, not during gameplay
- **Trade-off:** Adds complexity, but enables features like map library and leaderboard

### 4. GameState Enum
- **Why:** Prevent invalid state transitions (e.g., can't pause on menu)
- **How:** Game.state checked before routing input
- **Trade-off:** Simpler than full state machine, but less formal

## Performance Characteristics

- **Frame rate:** 60 FPS sustained
- **Entity count:** Handles 100+ enemies + 20 towers + 1000+ bullets without lag
- **Database queries:** Only at game start/end, not during gameplay
- **Memory:** ~50-100 MB (Pygame window + game data + venv)

## Testing Coverage

- Comprehensive test suite exists (test.py from commit 49e557b)
- Tests cover: wave logic, enemy behavior, tower mechanics, round state
- No automated UI testing (manual testing required for menu/button layout)

## Known Limitations

1. **No server architecture** - Single-player only, no multiplayer
2. **No graphics optimization** - All Pygame rendering is immediate mode
3. **No save/load during game** - Can only save after game ends
4. **Limited configurability** - Difficulty and settings defined in code/database
5. **No analytics/telemetry** - No player behavior tracking (intentional privacy choice)

## Architecture Health

**Strengths:**
- Clear separation of concerns (Game → Round → Wave)
- Modular tower/enemy system allows easy extension
- Database provides structured data persistence
- Pygame abstracts OS-level graphics details

**Weaknesses:**
- Wave class is large and handles multiple responsibilities
- UIMenu has grown to 22KB (could be split into multiple files)
- Database class is monolithic (30KB, 500+ lines)
- No formal error handling or logging system

**Recommended Refactors (Future):**
- Split menu.py into separate screen classes
- Extract database logic into repository pattern
- Add logging system for debugging
- Add event system for state changes (instead of direct method calls)

## Next Steps for Architecture

See `03_macro_roadmap.md` and `04_implementation_strategy.md` for planned improvements.
