---
task_id: 5
priority: HIGH
title: Update Database with Balanced Wave Configuration Parameters
status: PENDING
---

## Summary
Update the database `wave_configs` table with recommended starting parameters based on the balance research.

## Recommended Parameters

```python
RECOMMENDED_WAVE_CONFIG = {
    1: {
        "enemy_count": 6,
        "hp_per": 100,
        "spawn_interval": 0.4,
        "hp_multiplier": 1.0,
        "speed_multiplier": 1.0,
        "bounty_multiplier": 1.0
    },
    2: {
        "enemy_count": 8,
        "hp_per": 115,
        "spawn_interval": 0.35,
        "hp_multiplier": 1.15,
        "speed_multiplier": 1.0,
        "bounty_multiplier": 1.0
    },
    3: {
        "enemy_count": 10,
        "hp_per": 132,
        "spawn_interval": 0.3,
        "hp_multiplier": 1.32,
        "speed_multiplier": 1.05,
        "bounty_multiplier": 1.0
    },
    4: {
        "enemy_count": 13,
        "hp_per": 152,
        "spawn_interval": 0.25,
        "hp_multiplier": 1.52,
        "speed_multiplier": 1.1,
        "bounty_multiplier": 1.0
    },
    5: {
        "enemy_count": 17,
        "hp_per": 175,
        "spawn_interval": 0.2,
        "hp_multiplier": 1.75,
        "speed_multiplier": 1.15,
        "bounty_multiplier": 1.0
    }
}
```

## Implementation Details

### Update database.py:
- Modify built-in round configs to use these parameters
- Ensure wave_configs table entries match the formula calculations
- Test with existing database or create new seed data

### Verify Formulas Match:
- wave_configs.count should match `calculate_wave_enemy_count()`
- wave_configs.hp_multiplier should match `calculate_wave_enemy_hp()`

## Testing
- [ ] Database contains all 5 waves with correct parameters
- [ ] Game loads waves correctly from database
- [ ] Wave progression feels balanced in-game

## Related Files
- `database.py` - wave_configs initialization
- `map.py` - Wave loading from database

## Notes
These are starter values. Use playtest feedback to fine-tune individual parameters.
