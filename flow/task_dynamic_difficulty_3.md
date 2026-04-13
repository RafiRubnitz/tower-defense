---
task_id: 3
priority: CRITICAL
title: Dynamic Difficulty Algorithm - Replace linear scaling
status: COMPLETED
---

## Summary
Created DifficultyManager in src/difficulty.py using exponential growth curves for all wave parameters. Replaces flat linear formulas. Supports easy/normal/hard presets and adapts mid-game based on player performance (escape ratio). Wave configs now include HP, speed, bounty multipliers and enemy composition.

## Changes
- src/difficulty.py: New DifficultyManager + WaveConfig dataclass
- map.py: Wave init extended with hp/speed/bounty multipliers, _spawn_enemy() uses them
- map.py: Round uses DifficultyManager to configure all 10 waves, records wave results
- game.py: Passes difficulty and total_waves (10) settings to Round

## Commits
- (next commit)

## Tests Completed
- [x] DifficultyManager produces correct exponential scaling (verified via Python test)
- [x] Wave 5 includes boss + composition mix
- [x] Performance adaptation logic (escape_ratio clamping) verified
- [x] Code follows project patterns
