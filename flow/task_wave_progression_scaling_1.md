---
task_id: 2
priority: HIGH
title: Implement Wave Progression Scaling Algorithm
status: PENDING
---

## Summary
Implement progressive difficulty scaling so each wave is 20-35% harder than the previous. This ensures the game provides increasing challenge while maintaining fairness.

## Requirements
- Wave 1: Baseline difficulty (test player skill)
- Wave 2: +25% difficulty
- Wave 3: +30% difficulty  
- Wave 4: +35% difficulty
- Wave 5: +40% difficulty (final challenge)

## Implementation Details

### Create difficulty multiplier function in `map.py`:
```python
def get_wave_difficulty_multiplier(wave_number: int) -> float:
    """Return difficulty multiplier for given wave (1-indexed)"""
    multipliers = {
        1: 1.0,    # baseline
        2: 1.25,   # +25%
        3: 1.30,   # +30%
        4: 1.35,   # +35%
        5: 1.40,   # +40%
    }
    return multipliers.get(wave_number, 1.0)
```

### Apply to Wave class:
- Store difficulty multiplier in Wave instance
- Use when calculating enemy spawning rates and wave composition

## Testing
- [ ] Each wave spawns appropriately more difficult enemies
- [ ] Progression feels smooth, not too easy or too hard
- [ ] Player can still win with good strategy

## Related Files
- `map.py` - Wave class
- `database.py` - wave_configs table

## Notes
This is the foundation for balancing all other game difficulty aspects.
