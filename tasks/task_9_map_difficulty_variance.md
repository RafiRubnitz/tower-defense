---
task_id: 10
priority: MEDIUM
title: Adjust Maps for Difficulty Variance Based on Path Length
status: PENDING
---

## Summary
Different map paths (L-Path vs. Spiral) have different lengths, which affects difficulty. Adjust wave counts and enemy HP per map.

## Path Length Impact

### Short Path Maps (15 cells)
- **Advantage to Enemies**: Less time for towers to shoot
- **Disadvantage to Players**: Fewer choke points, harder to defend
- **Mitigation**: Reduce enemy count by 20% or reduce HP by 25%
- **Examples**: Classic L-Path

### Medium Path Maps (20-22 cells)
- **Baseline**: Use standard wave configuration
- **Examples**: Zigzag Challenge, Figure-8 Loop

### Long Path Maps (28-30 cells)
- **Advantage to Players**: More time to shoot, more placement options
- **Disadvantage to Enemies**: More exposure to tower fire
- **Mitigation**: Increase enemy count by 15% or increase HP by 20%
- **Examples**: Spiral Madness

## Implementation Details

### Create map difficulty multiplier in `database.py`:
```python
MAP_DIFFICULTY_MULTIPLIERS = {
    "Classic L-Path": 0.8,      # Short path: -20% difficulty
    "Zigzag Challenge": 1.0,    # Medium path: baseline
    "Spiral Madness": 1.15,     # Long path: +15% difficulty
    "Figure-8 Loop": 1.0,       # Medium path: baseline
}
```

### Update database schema:
- Add `path_length` field to maps table (or calculate from path)
- Add `difficulty_multiplier` field to maps table
- Store map-specific wave adjustments

### Apply multipliers to wave config:
```python
def apply_map_difficulty_multiplier(wave_config, map_id):
    multiplier = get_map_difficulty_multiplier(map_id)
    wave_config['count'] *= multiplier
    wave_config['hp_multiplier'] *= multiplier
    return wave_config
```

## Testing
- [ ] Short path maps are harder (fewer towers survive)
- [ ] Long path maps are easier (more time to plan)
- [ ] Medium path maps are balanced baseline
- [ ] Adjusted difficulty feels fair across all maps

## Map Analysis

### Measure Path Length:
```python
def calculate_path_length(path_list):
    """Return length of path in grid cells"""
    return len(path_list)
```

### Current Built-in Maps:
- [ ] Classic L-Path: Measure and assign multiplier
- [ ] Zigzag Challenge: Measure and assign multiplier
- [ ] Spiral Madness: Measure and assign multiplier
- [ ] Figure-8 Loop: Measure and assign multiplier

## Related Files
- `database.py` - Maps table, map initialization
- `map.py` - Apply difficulty multipliers when loading waves

## Notes
This ensures all maps are equally fun to play on. Players shouldn't feel forced to play specific maps for "correct" difficulty.
