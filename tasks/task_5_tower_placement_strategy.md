---
task_id: 6
priority: MEDIUM
title: Implement Tower Placement Strategy Analytics
status: PENDING
---

## Summary
Add analytics to understand and reward optimal tower placement, especially at path choke points. Track placement efficiency metrics.

## Strategic Placement Concepts

### Choke Points
- Identify map-specific path intersections where multiple enemies pass
- Towers at choke points deal damage to multiple enemies efficiently
- Skilled players can win with fewer towers by using choke points

### Firing Efficiency
- Towers near path: fire at max efficiency
- Towers far from path: wasted bullet range
- Overlapping ranges: overkill (wasteful)

### Placement Quality Metrics
- Towers required: optimal vs. actual (efficiency score)
- Coverage: minimal overlap between tower ranges
- Strategic positioning: choke point vs. general placement

## Implementation Details

### Create analytics in `map.py`:
```python
def calculate_tower_efficiency():
    """Analyze tower placement and return efficiency metrics"""
    return {
        "total_towers": count,
        "optimal_towers": calculated_optimal,
        "efficiency_ratio": optimal / actual,  # 1.0 = perfect, <1.0 = inefficient
        "overlap_count": overlapping_ranges,
        "choke_point_coverage": percentage
    }
```

### Track during gameplay:
- Record player's tower placement
- Calculate actual vs optimal for each wave
- Show efficiency feedback after level

## Testing
- [ ] Choke points are identifiable on maps
- [ ] Towers at choke points hit multiple enemies
- [ ] Efficiency calculation is accurate
- [ ] Feedback helps players improve placement strategy

## Related Files
- `map.py` - Map class, tower management
- `game.py` - UI feedback after waves

## Notes
This encourages players to study maps and plan placement strategically. Don't penalize inefficient placement, just reward efficiency.
