# Game Balance Tasks Index

All tasks derived from `research/game_balance_algorithm.md`

## Priority Order

### CRITICAL (Foundation)
- [task_0_game_balance_implementation_overview.md](task_0_game_balance_implementation_overview.md) - Meta-task and overview

### HIGH (Core System)
- [task_1_wave_progression_scaling.md](task_1_wave_progression_scaling.md) - Difficulty multipliers per wave
- [task_2_wave_composition_formula.md](task_2_wave_composition_formula.md) - Enemy count and HP formulas
- [task_3_dynamic_money_allocation.md](task_3_dynamic_money_allocation.md) - Money growth system
- [task_4_database_wave_config.md](task_4_database_wave_config.md) - Seed database with parameters
- [task_7_playtest_and_validation.md](task_7_playtest_and_validation.md) - Systematic testing

### MEDIUM (Enhancement)
- [task_5_tower_placement_strategy.md](task_5_tower_placement_strategy.md) - Placement analytics
- [task_6_dynamic_difficulty_adjustment.md](task_6_dynamic_difficulty_adjustment.md) - Rubber-banding system
- [task_9_map_difficulty_variance.md](task_9_map_difficulty_variance.md) - Map-specific adjustments

### LOW (Future)
- [task_8_tower_upgrade_system.md](task_8_tower_upgrade_system.md) - Tower tiers (Tier 1, 2, 3)

## Quick Summary

| ID | Title | Priority | Status |
|----|-------|----------|--------|
| 0 | Game Balance Implementation Overview | CRITICAL | PENDING |
| 1 | Wave Progression Scaling | HIGH | PENDING |
| 2 | Wave Composition Formula | HIGH | PENDING |
| 3 | Dynamic Money Allocation | HIGH | PENDING |
| 4 | Database Wave Configuration | HIGH | PENDING |
| 5 | Tower Placement Strategy | MEDIUM | PENDING |
| 6 | Dynamic Difficulty Adjustment | MEDIUM | PENDING |
| 7 | Playtest and Validation | HIGH | PENDING |
| 8 | Tower Upgrade System | LOW | PENDING |
| 9 | Map Difficulty Variance | MEDIUM | PENDING |

## Recommended Implementation Path

1. Start with **task_0** for overview
2. Implement **tasks 1-4** (core balance system)
3. Run **task_7** (playtest and validate)
4. Add **tasks 5-6** (analytics and adjustment)
5. Refine **task_9** (map variance)
6. Future: **task_8** (tower upgrades)

## Key Files to Modify

- `map.py` - Wave spawning, Round money, analytics
- `database.py` - Wave configuration initialization
- `tower.py` - Tower efficiency metrics
- `game.py` - UI feedback and stats tracking
- `enemy.py` - Enemy balance parameters

## Research Document

All tasks are based on detailed analysis in:
- `research/game_balance_algorithm.md`

## Success Metrics

When all HIGH priority tasks are complete:
- [ ] Progressive difficulty 20-35% per wave
- [ ] Money grows from bounties enabling strategy
- [ ] Tower placement significantly impacts outcome
- [ ] All playtest checklists pass
- [ ] Skilled players win 60-75%, casual players win 20-40%
- [ ] No waves feel impossible or trivial
