---
task_id: 9
priority: LOW
title: Implement Tower Upgrade System (Future Enhancement)
status: PENDING
---

## Summary
Add tower upgrade tiers (Tier 1, 2, 3) to create economic strategy loop and late-game depth.

## Tier Structure

### Tier 1: Basic Tower (Current)
- Cost: $100
- Range: 3.5 cells
- Power: 50 damage
- Cooldown: 600ms (83.3 DPS)

### Tier 2: Enhanced Tower
- Upgrade Cost: $150 (from T1)
- Range: 4.5 cells (+28%)
- Power: 80 damage (+60%)
- Cooldown: 500ms (160 DPS) (+92%)

### Tier 3: Advanced Tower
- Upgrade Cost: $200 (from T2)
- Range: 5.5 cells (+56% from T1)
- Power: 120 damage (+140% from T1)
- Cooldown: 400ms (300 DPS) (+260% from T1)

## Strategic Decisions This Enables

- **1 Strong Tower vs. 2 Weak Towers**: Tier 3 costs $450, Basic costs $200
- **Early vs. Late Upgrade**: Spend early on Tier 2s or save for Tier 3?
- **Placement Optimization**: Does each tier reward different placement strategies?

## Implementation Details

### Create Tower classes in `tower.py`:
```python
class EnhancedTower(BasicTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 4.5
        self.power = 80
        self.cooldown = 500

class AdvancedTower(BasicTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 5.5
        self.power = 120
        self.cooldown = 400
```

### Add upgrade mechanics:
- Right-click tower to upgrade (if funds available)
- Show upgrade cost in tooltip
- Track upgraded towers in Round

### UI Updates:
- Show tower tier with different colors/icons
- Display upgrade cost when hovering over tower
- Show "Upgrade Available" indicator

## Testing
- [ ] Towers can be upgraded successfully
- [ ] Upgrade costs are correct
- [ ] Stats match tier specifications
- [ ] Strategic choices feel meaningful

## Related Files
- `tower.py` - Tower class hierarchy
- `map.py` - Round tower management, upgrade UI
- `game.py` - Click handling for upgrades

## Notes
This is a future enhancement. Depends on core balance being solid first. Can launch game without this feature.
