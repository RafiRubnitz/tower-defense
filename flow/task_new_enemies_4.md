---
task_id: 4
priority: CRITICAL
title: 3 New Enemy Types - Tank, Scout, Boss
status: COMPLETED
---

## Summary
Added Tank (300 HP, slow, armored look), Scout (50 HP, 4x speed, diamond shape), and Boss (1000 HP, crown, large size) enemy classes to enemy.py. Wave spawn queue now uses enemy_composition from DifficultyManager to select the correct enemy type per spawn slot. Each enemy type has distinct visuals and health bars.

## Changes
- enemy.py: Added Tank, Scout, Boss classes with visual rendering and health bars
- enemy.py: Soldier updated with max_life_point for accurate health bar ratio
- map.py: Imported Tank, Scout, Boss; added _build_spawn_queue() and updated _spawn_enemy()
- map.py: Wave._spawn_queue initialized in __init__

## Commits
- (next commit)

## Tests Completed
- [x] All four enemy types instantiate with correct stats
- [x] Spawn queue correctly distributes types per composition
- [x] Health bars show accurate ratios
- [x] Code follows project patterns
