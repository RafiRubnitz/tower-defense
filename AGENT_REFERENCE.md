# Agent Reference - Tower Defense

Pygame grid-based tower defense: place towers on grass to stop enemies following a path.

## Run
`python run.py`

## Files
| File | Purpose |
|---|---|
| run.py | Entry, 980x600 window |
| game.py | `Game`: main loop, events, render |
| map.py | `Map`, `Wave`, `Round`, `Bullet` |
| tower.py | `BasicTower` |
| enemy.py | `Soldier` |
| player.py | `Player` (money, lives) |
| database.py | SQLite persistence (`tower_defense.db`) |
| src/ | `Point`, `Direction`, `GameState` |
| ui/menu.py | `MenuManager` |

## Numbers
| Key | Value |
|---|---|
| Grid | 40x30 @ 20px |
| Map area | 800x600 |
| UI panel | 180px right |
| FPS | 60 |
| Waves | 5 |
| Start money | $450 |
| Start lives | 10 |
| Tower cost | $100 |
| Tower range | 3.5 cells (70px) |
| Tower power | 50 |
| Tower cooldown | 600ms |
| Bullet speed | 10 px/frame |
| Soldier HP | 100 |
| Soldier speed | 2.0 |
| Soldier bounty | $15 |

## Flow
1. `Round` holds state (waves, money, lives, score).
2. `Wave` spawns enemies + manages bullets.
3. `Tower.update()` targets enemies in range, fires `Bullet`.
4. `Bullet.update()` moves to target, deals damage.
5. Enemy reaching path end costs a life.
6. Lives=0 -> game over; all waves cleared -> victory.

## Controls
SPACE pause | R restart | LClick place tower (grass only)

## DB Tables
maps, round_configs, wave_configs, game_stats, achievements, player_settings
Built-in maps: Classic L-Path, Zigzag Challenge, Spiral Madness, Figure-8 Loop
