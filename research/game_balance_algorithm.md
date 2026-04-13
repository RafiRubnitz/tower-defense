# Tower Defense Game Balance Algorithm Research

## Executive Summary

This research investigates optimal balancing algorithms for the Tower Defense game to ensure that players must strategically place towers to succeed. The game must provide a challenge that rewards skilled placement while remaining fair and not frustrating.

---

## 1. Game Balance Principles

### Core Concept
Game balance exists at the intersection of **player resources** (money, lives) and **enemy difficulty** (quantity, strength, density). A balanced game forces players to make meaningful strategic decisions about tower placement.

### Key Balance Metrics
1. **Resource-to-Difficulty Ratio**: Money available vs. enemy HP that must be dealt with
2. **Placement Criticality**: Whether tower placement position significantly affects outcome
3. **Skill Expression**: Ability of skilled players to win vs. mediocre players struggling
4. **Fairness**: Players feel loss is due to poor strategy, not RNG or unfair enemy waves

---

## 2. Current Game State

### Available Player Resources
- **Starting Money**: $450
- **Starting Lives**: 10
- **Tower Cost**: $100 (allows ~4-5 initial towers)
- **Tower Performance**: 
  - Range: 3.5 grid cells (70px)
  - Power: 50 damage
  - Cooldown: 600ms = 83.3 DPS per tower
  - Grid: 40x30, Map area: 800x600

### Enemy Stats
- **Soldier (Basic Enemy)**
  - HP: 100
  - Speed: 2.0 px/frame
  - Bounty: $15 per kill
- **Total Waves**: 5
- **Path Length**: Varies by map (15-30 cells typical)

### Economic Model
- Kill bounties ($15) partially fund new towers
- Early waves must be survivable with starting money
- Later waves test resource management and tower upgrading

---

## 3. Recommended Balance Algorithm

### 3.1 Wave Progression Strategy

**Progressive Difficulty Scaling** - Each wave should be approximately 20-35% harder than the previous:

```
Wave 1: Baseline (test player skill)
Wave 2: +25% difficulty
Wave 3: +30% difficulty  
Wave 4: +35% difficulty
Wave 5: +40% difficulty (final challenge)
```

### 3.2 Money-to-Enemy Difficulty Formula

**Core Equation:**
```
Required_Money = (Total_Enemy_HP / Tower_DPS) * Safety_Multiplier
```

Where:
- **Total_Enemy_HP** = sum of all enemy HP in wave
- **Tower_DPS** = 83.3 (current basic tower)
- **Safety_Multiplier** = 1.2-1.5 (allows inefficient placement to still work)

**Example Calculation (Wave 1):**
- Enemies: 8 Soldiers = 800 total HP
- Required DPS: 800 / 6 seconds = 133 DPS needed
- Towers needed: 133 / 83.3 = 1.6 towers ≈ 2 towers minimum
- Cost: 2 × $100 = $200
- Available: $450 → **Surplus: $250** (allows strategic experimenting)

### 3.3 Wave Composition Formula

**Balanced Wave Structure** - Each wave should have enemy composition:

```
Wave_Enemy_Count = Base_Count × (1 + Wave_Number × 0.3)
Wave_HP_Per_Enemy = Base_HP × (1 + Wave_Number × 0.15)
```

**Example Wave Progression:**
| Wave | Base Count | Adjusted Count | HP/Enemy | Total HP | Money Available |
|------|-----------|-----------------|----------|----------|-----------------|
| 1    | 6         | 6               | 100      | 600      | $450            |
| 2    | 6         | 8               | 115      | 920      | $575            |
| 3    | 6         | 10              | 132      | 1320     | $700            |
| 4    | 6         | 13              | 152      | 1976     | $875            |
| 5    | 6         | 17              | 175      | 2975     | $1050           |

*Note: Money grows from enemy bounties + starting allocation*

---

## 4. Strategic Depth Mechanics

### 4.1 Tower Placement Critical Factors

**Path Choke Points**: 
- Enemies follow a set path; towers placed on path intersections deal damage to multiple enemies
- Players who identify and exploit choke points win with fewer towers
- Poor placement requires excessive towers

**Firing Efficiency**:
- Towers far from path waste bullets on distant targets
- Towers at path turns force enemies to slow down naturally
- Staggered placement (not clustering) prevents overkill

**Range Overlap**:
- Minimal overlap = efficient coverage
- Excessive overlap = wasted tower investment
- Skilled players minimize total towers while maintaining coverage

### 4.2 Economic Strategy Decisions

**Early Game** (Waves 1-2):
- Minimal tower set for survival
- Build surplus money for mid-game upgrades
- Decision: Full coverage vs. selective placement on choke points?

**Mid Game** (Waves 3-4):
- Use bounties to add 2-3 strategic towers
- Place towers for efficiency, not just survival
- Decision: Where are the high-value placement spots?

**End Game** (Wave 5):
- Final tower push with saved money
- Must make peace with either: Accept losses if underfunded, or place perfectly with available funds
- High-risk/high-reward decisions

---

## 5. Implementation Recommendations

### 5.1 Data-Driven Wave Config (Already in Database)

The `wave_configs` table in `database.py` already supports:
```python
{
  "wave_id": 1,
  "round_id": 1,
  "enemy_type": "Soldier",
  "count": 6,
  "spawn_rate": 0.3,  # seconds between spawns
  "hp_multiplier": 1.0,
  "speed_multiplier": 1.0,
  "bounty_multiplier": 1.0
}
```

This allows balance tuning without code changes.

### 5.2 Dynamic Money Allocation Per Wave

```python
def calculate_wave_money(wave_number, base_money, bounty_earned):
    """Calculate money available for tower placement in given wave"""
    wave_multiplier = 1.0 + (wave_number * 0.15)
    return int(base_money * wave_multiplier + bounty_earned)
```

### 5.3 Recommended Starting Parameters

```python
WAVE_CONFIG = {
    1: {"enemy_count": 6,  "hp_per": 100, "spawn_interval": 0.4},
    2: {"enemy_count": 8,  "hp_per": 115, "spawn_interval": 0.35},
    3: {"enemy_count": 10, "hp_per": 132, "spawn_interval": 0.3},
    4: {"enemy_count": 13, "hp_per": 152, "spawn_interval": 0.25},
    5: {"enemy_count": 17, "hp_per": 175, "spawn_interval": 0.2},
}
```

---

## 6. Testing & Validation Strategy

### Playtest Checklist
- [ ] Wave 1: Can win with $450 starting money + basic strategy?
- [ ] Wave 2-3: Do bounties provide enough for strategic additions?
- [ ] Wave 4: Can mediocre placement still survive?
- [ ] Wave 5: Does optimal placement beat suboptimal placement significantly?
- [ ] Choke Point Test: Can experienced player use 25% fewer towers with perfect placement?
- [ ] Fairness Test: No wave feels impossible or trivial after 3-5 playthroughs?

### Balance Metrics to Track
1. **Towers Required** (optimal vs. minimal vs. over-building)
2. **Win Rate** (should be 60-75% for skilled players, 20-40% for casual)
3. **Money Efficiency** (bounties earned vs. towers built)
4. **Placement Distribution** (players clustering towers vs. spreading them)

---

## 7. Advanced Balance Considerations

### Dynamic Difficulty Scaling
Consider adjusting future waves based on player performance:
- If player loses more than 1 life → reduce next wave slightly
- If player has >60% money remaining → increase next wave
- Keeps game challenging without frustration

### Tower Upgrade Path (Future Enhancement)
Adding tier 2/3 towers could create:
- Tower placement → economic → placement again loop
- Decision making: 1 strong tower vs. 2 weak towers?
- Late-game money sink (prevents sitting on $1000)

### Map Difficulty Variance
Different maps (L-Path vs. Spiral) have different path lengths:
- **Short paths** (15 cells): Fewer choke points, harder to defend
- **Long paths** (30 cells): More time to shoot, more placement options
- Adjust wave counts/enemy HP per map

---

## 8. Conclusion

A balanced Tower Defense game requires:
1. **Progressive difficulty** scaling (20-35% per wave)
2. **Positive resource feedback** (bounties fund growth)
3. **Placement criticality** (choke points reward strategy)
4. **Economic strategy** (spend carefully, invest wisely)
5. **Fair challenge** (skill distinctly rewarded over luck)

The recommended formula (Enemy_HP / Tower_DPS × Safety_Multiplier) combined with progressive wave composition creates a system where:
- Casual players can survive with basic strategy
- Skilled players can optimize placement for 30-40% tower efficiency gain
- Each wave feels distinctly harder while remaining fair

---

## References & Sources

- **Tower Defense Game Balance**: Principles from Bloons TD6, Plants vs. Zombies, Kingdom Rush
- **Difficulty Scaling**: Exponential vs. Linear progression research
- **Economic Systems**: Game theory applications in resource management
- **Placement Mechanics**: Spatial strategy game design patterns

---

*Research Date: 2026-04-13*
*Game Version: Tower Defense with Pygame, 5 waves, Menu integration*
