---
task_id: 7
priority: MEDIUM
title: Implement Dynamic Difficulty Adjustment System
status: PENDING
---

## Summary
Adjust future waves based on player performance to keep challenge level appropriate without frustration.

## Adjustment Logic

### Reduce Next Wave If:
- Player lost more than 1 life in current wave
- Player has <$200 remaining (financial stress)
- Win was narrow (low resources left)

**Reduction**: Reduce enemy count or HP by 10-15%

### Increase Next Wave If:
- Player has >60% of total possible money remaining
- Player lost 0 lives
- Win was dominant (surplus resources)

**Increase**: Increase enemy count or HP by 10-15%

## Implementation Details

### Create function in `map.py`:
```python
def calculate_next_wave_adjustment(current_wave_stats: dict) -> float:
    """Return difficulty multiplier adjustment for next wave"""
    lives_lost = current_wave_stats['lives_lost']
    money_remaining = current_wave_stats['money_remaining']
    money_total = current_wave_stats['total_money']
    
    if lives_lost > 1 or money_remaining < 200:
        return 0.85  # Reduce by 15%
    elif money_remaining > money_total * 0.6 and lives_lost == 0:
        return 1.15  # Increase by 15%
    else:
        return 1.0   # Keep same
```

### Track in Round class:
- Store per-wave stats (lives lost, money spent, efficiency)
- Apply adjustment multiplier to next wave config
- Log adjustments for debugging

## Testing
- [ ] Easy waves are properly reduced
- [ ] Hard waves are properly increased
- [ ] Adjustments don't make game too easy or too hard
- [ ] Player feels challenge is fair

## Related Files
- `map.py` - Round class, wave adjustment logic
- `game.py` - Stats tracking

## Notes
This is optional "rubber-banding" to maintain engagement. Can be toggled in settings if player prefers fixed difficulty.
