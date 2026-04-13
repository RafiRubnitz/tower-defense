---
task_id: 4
priority: HIGH
title: Implement Dynamic Money Allocation System
status: PENDING
---

## Summary
Implement dynamic money allocation so players have more money available in later waves (from bounties + wave bonuses), enabling strategic tower additions.

## Formula
```python
wave_available_money = (base_starting_money + earned_bounties) * (1 + wave_number * 0.15)
```

## Target Money Progression

| Wave | Money Available | Notes |
|------|-----------------|-------|
| 1    | $450            | Starting amount |
| 2    | $575            | ~+28% (from bounties + multiplier) |
| 3    | $700            | Additional tower funding |
| 4    | $875            | Strategic additions possible |
| 5    | $1050           | Final tower push |

## Implementation Details

### Create function in `map.py`:
```python
def calculate_wave_money(wave_number: int, base_money: int, bounty_earned: int) -> int:
    """Calculate total money available for tower placement in given wave"""
    wave_multiplier = 1.0 + (wave_number * 0.15)
    return int((base_money + bounty_earned) * wave_multiplier)
```

### Update Round class:
- Track total bounties earned from killed enemies
- Calculate available money at start of each wave
- Display to player (UI: "Available: $XXX")

## Testing
- [ ] Money grows progressively through waves
- [ ] Bounties are properly tracked and added
- [ ] Money display is accurate
- [ ] Players can afford strategic tower additions

## Related Files
- `map.py` - Round class, money management
- `game.py` - Money display in UI

## Notes
This creates positive feedback: Kill enemies → Get bounties → Fund new towers → Kill more enemies.
