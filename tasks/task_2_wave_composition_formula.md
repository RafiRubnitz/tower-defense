---
task_id: 3
priority: HIGH
title: Implement Wave Composition Formula (Enemy Count & HP)
status: PENDING
---

## Summary
Implement formulas to calculate wave-specific enemy counts and HP per enemy, creating balanced progression through 5 waves.

## Formula
```
Wave_Enemy_Count = Base_Count × (1 + Wave_Number × 0.3)
Wave_HP_Per_Enemy = Base_HP × (1 + Wave_Number × 0.15)
```

## Target Wave Progression

| Wave | Enemy Count | HP/Enemy | Total HP | 
|------|------------|----------|----------|
| 1    | 6          | 100      | 600      |
| 2    | 8          | 115      | 920      |
| 3    | 10         | 132      | 1320     |
| 4    | 13         | 152      | 1976     |
| 5    | 17         | 175      | 2975     |

## Implementation Details

### Create functions in `map.py`:
```python
def calculate_wave_enemy_count(wave_number: int, base_count: int = 6) -> int:
    """Calculate enemy count for given wave"""
    return int(base_count * (1 + wave_number * 0.3))

def calculate_wave_enemy_hp(wave_number: int, base_hp: int = 100) -> int:
    """Calculate HP per enemy for given wave"""
    return int(base_hp * (1 + wave_number * 0.15))
```

### Update Wave class:
- Use these formulas when generating wave configuration
- Ensure smooth progression and playability

## Testing
- [ ] Wave progression matches target values approximately
- [ ] Each wave requires more towers than previous
- [ ] Bounties enable strategic tower placement in later waves

## Related Files
- `map.py` - Wave class, enemy spawning
- `database.py` - wave_configs table
- `enemy.py` - Enemy HP values

## Notes
Base count (6) and base HP (100) can be adjusted for difficulty tuning.
