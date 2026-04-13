---
task_id: 8
priority: HIGH
title: Execute Playtest Checklist and Balance Validation
status: PENDING
---

## Summary
Run through systematic playtests to validate game balance and ensure all waves are fair and fun.

## Playtest Checklist

- [ ] **Wave 1**: Can win with $450 starting money + basic strategy?
  - Requirement: Should be easily winnable
  - Target: Player loses 0 lives with average tower placement
  
- [ ] **Wave 2-3**: Do bounties provide enough for strategic additions?
  - Requirement: Player should have $150-250 to add 1-2 strategic towers
  - Target: Good placement beats poor placement significantly
  
- [ ] **Wave 4**: Can mediocre placement still survive?
  - Requirement: Not impossible, but requires decent strategy
  - Target: Skilled player easily survives; casual player struggles
  
- [ ] **Wave 5**: Does optimal placement beat suboptimal placement?
  - Requirement: Perfect placement should beat mediocre by >40% efficiency
  - Target: Skilled placement feels rewarding, not RNG-dependent
  
- [ ] **Choke Point Test**: Can experienced player use 25% fewer towers?
  - Requirement: Strategic placement at choke points enables 6 towers instead of 8
  - Target: Skilled players are rewarded significantly
  
- [ ] **Fairness Test**: No wave feels impossible or trivial?
  - Requirement: After 3-5 playthroughs, each wave feels fair
  - Target: Loss feels like player error, not unfair difficulty

## Balance Metrics to Track

Create a playtest spreadsheet tracking:

| Metric | Wave 1 | Wave 2 | Wave 3 | Wave 4 | Wave 5 |
|--------|--------|--------|--------|--------|--------|
| Towers Used | | | | | |
| Lives Lost | | | | | |
| Money Left | | | | | |
| Bounty Earned | | | | | |
| Win/Lose | | | | | |

### Key Metrics
1. **Towers Required**: Optimal vs. minimum vs. over-built
2. **Win Rate**: Should be 60-75% for skilled players, 20-40% for casual
3. **Money Efficiency**: Bounties earned vs. towers built ratio
4. **Placement Distribution**: Do players cluster towers or spread them?

## Data Collection

### Run Multiple Playthroughs
- At least 3 complete games per difficulty level
- Vary tower placement strategies (aggressive, conservative, optimized)
- Document any waves that feel unfair or too easy

### Record Findings
- Create `PLAYTEST_RESULTS.md` with findings
- Note any waves that need adjustment
- Suggest parameter tweaks based on results

## Adjustment Rules

If playtest finds issues:
- **Wave too easy**: Increase enemy count by 10% or HP by 15%
- **Wave too hard**: Decrease enemy count by 15% or HP by 10%
- **Money shortage**: Increase bounty multiplier or starting money
- **Placement triviality**: Reduce tower range or add more choke points

## Completion Criteria

- [ ] All 6 playtest checklist items verified ✓
- [ ] No waves feel impossible or trivial
- [ ] Skilled placement noticeably beats poor placement
- [ ] All metrics tracked and documented
- [ ] `PLAYTEST_RESULTS.md` created with findings

## Related Files
- `map.py` - Wave difficulty parameters
- `database.py` - Wave configuration
- Future: `PLAYTEST_RESULTS.md` - Results document

## Notes
Balance is iterative. This playtest is the foundation for ongoing adjustments.
