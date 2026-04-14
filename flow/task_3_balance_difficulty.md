---
task_id: 3
priority: HIGH
title: Balance Game Difficulty
status: COMPLETED
---

## Summary
Significantly increased game difficulty across enemy stats, tower costs, and starting resources. The game now requires more strategic tower placement and careful resource management. Players must use skill and planning rather than random tower placement.

## Changes

### Enemy Statistics (enemy.py)
Applied consistent scaling: 50% HP increase, 25% speed increase, 10% bounty reduction

**Soldier** (Basic infantry):
- HP: 100.0 → 150.0 (+50%)
- Speed: 2.0 → 2.5 (+25%)
- Bounty: 15 → 14 (-10% from 15)

**Tank** (Heavy armored):
- HP: 300.0 → 450.0 (+50%)
- Speed: 1.0 → 1.25 (+25%)
- Bounty: 30 → 27 (-10%)

**Scout** (Fast lightweight):
- HP: 50.0 → 75.0 (+50%)
- Speed: 4.0 → 5.0 (+25%)
- Bounty: 20 → 18 (-10%)

**Boss** (End-of-wave):
- HP: 1000.0 → 1500.0 (+50%)
- Speed: 0.8 → 1.0 (+25%)
- Bounty: 100 → 90 (-10%)

### Tower Costs (towers/*.py and towers/__init__.py)
Applied 20% cost increase to all tower types:

- BasicTower: $100 → $120
- SniperTower: $200 → $240
- MachineGunTower: $150 → $180
- SplashTower: $250 → $300
- FreezeTower: $175 → $210
- LaserTower: $300 → $360

### Economy Balance (ui/menu.py)
- Default starting money: $450 → $350 (22% reduction)
- Money options updated: [200, 350, 450, 600, 800] → [200, 300, 350, 500, 700]

## Impact Analysis

### Resource Management
- Player starts with 22% less money, making early tower placement more critical
- Tower costs increased by 20%, reducing the number of towers affordable early game
- Players must choose tower placement carefully

### Combat Difficulty
- Enemies are stronger (50% more HP) but slightly faster (25% speed increase)
- Scout enemies are more dangerous with faster speed (4.0→5.0)
- Boss enemies are significantly tougher (1000→1500 HP)
- Reduced bounty rewards make economy tighter

### Strategic Requirements
- Players can no longer win through random tower placement
- Requires planning tower coverage based on path
- Must balance between early defense and saving money for upgrades
- Necessitates use of tower synergies and placement strategy

## Commits
- 98266d8: task/3 - Balance game difficulty

## Tests Completed
- [x] All enemy classes load with new stats
- [x] Tower costs properly updated across all classes
- [x] Tower registry reflects new costs
- [x] Menu settings properly initialized with new default money
- [x] Code compiles without errors
- [x] No breaking changes to existing systems
