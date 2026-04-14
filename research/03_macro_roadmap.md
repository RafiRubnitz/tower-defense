# Macro-Level Roadmap - Next 6 Months

**Current Date:** April 14, 2026  
**Planning Horizon:** April - September 2026

## Phase Overview

The project has completed core game mechanics and is now in the **Polish & Expansion** phase.

```
Phase 1 (Complete)       Phase 2 (Current)        Phase 3 (Future)
Core Mechanics           Polish & Balance          Content & Features
Jan - Mar 2026          Apr - May 2026            Jun - Sep 2026

✅ Game loop            🟡 UI/UX fixes           🔲 Endless mode
✅ Towers & Enemies     🟡 Game balance          🔲 Advanced towers
✅ Wave system          🟡 Visual design         🔲 Map editor
✅ Database             🟡 Controls              🔲 Achievements
✅ Menu system                                    🔲 Leaderboards
```

## Macro-Level Goals

### Q2 2026 (April-May): Reach Minimum Playable Polish
**Goal:** Game feels complete and balanced for 1-2 hour play sessions
- ✅ Fix all UI/UX issues (buttons, spacing, text overflow)
- ✅ Improve visual design (distinct tower appearances, cleaner UI)
- ✅ Balance game difficulty (challenging but fair)
- ✅ Stable gameplay without crashes or undefined behavior

**Success Metrics:**
- New players can complete a game without frustration
- Game takes 20-30 minutes per playthrough
- Win rate for skilled players: ~60-70%
- Zero crashes or game-breaking bugs

### Q3 2026 (June-August): Feature Expansion
**Goal:** Add replayability and long-form gameplay
- Add Infinite Waves mode with scoring
- Add difficulty selection (Easy, Normal, Hard, Nightmare)
- Implement leaderboards for Endless mode
- Add 2-3 new tower types
- Add 2-3 new map layouts

**Success Metrics:**
- Players can spend 10+ hours in Endless mode
- Leaderboard shows competitive play
- New tower types have distinct playstyles
- Difficulty selection provides true progression

### Q4 2026 (September+): Advanced Features & Community
**Goal:** Create content creation & community tools
- Map editor for custom maps
- Achievement system with 20+ unlockables
- Steam/itch.io release prep
- Modding support (custom towers/enemies)

## Detailed Q2 Roadmap (April-May 2026)

### Week 1-2 (Apr 14-27): UI/UX Polish
**Task 1: Fix Map Selection UI** (In Progress)
- Increase button width, center alignment
- Ensure all map names fit without overflow
- ~1-2 hours

**Task 2: Tower Design & Selector UI**
- Add unique colors/shapes to towers
- Style selector panel with clear stats
- Add hover effects and selection feedback
- ~4-6 hours

**Impact:** Game looks professional, not broken

### Week 2-3 (Apr 28 - May 11): Game Balance
**Task 3: Increase Game Difficulty**
- Adjust enemy stats (health, speed)
- Increase wave difficulty scaling
- Reduce starting money/resources
- Test: Players must use strategy to win
- ~3-5 hours

**Impact:** Game has challenge, requires skill

### Week 4 (May 12-25): New Game Mode
**Task 4: Infinite Waves Mode**
- Implement wave generation algorithm
- Add mode selection in menu
- Create scoring/leaderboard system
- ~6-8 hours

**Impact:** Replayability increases 5-10x

### Week 5+ (May 26+): Testing & Polish
- Playtest across 10+ playthroughs
- Fix balance issues discovered in testing
- Performance optimization if needed
- Document game rules and mechanics
- ~5-10 hours

## Detailed Q3 Roadmap (June-August 2026)

### Phase 3A: Content Expansion (June)
**Add Difficulty Levels**
- Easy: 1.2x health reduction, 1.5x starting money
- Normal: Current state
- Hard: 1.2x health/speed, 0.8x starting money
- Nightmare: 1.5x health/speed, 0.6x starting money
- Time estimate: ~2-3 hours

**Add 2-3 New Tower Types**
- Possible additions: SlowTower, MissileT Tower, ElectricTower
- Each needs unique mechanic, balance, visuals
- Time estimate: ~3-4 hours per tower

### Phase 3B: Content Expansion (July)
**Add 2-3 New Maps**
- Each with unique path layout, difficulty curve
- Time estimate: ~2-3 hours per map (design + testing)

**Achievement System**
- 20+ achievements (e.g., "Win on Nightmare", "Kill 1000 enemies")
- Tracking and persistence in database
- Time estimate: ~3-4 hours

### Phase 3C: Polish & Release (August)
**Leaderboard System**
- Persistent high scores for Endless mode
- Display top 10 players globally (local database)
- Time estimate: ~2-3 hours

**Performance Tuning**
- Profile for bottlenecks
- Optimize rendering if needed
- Time estimate: ~2-3 hours

**Release Prep**
- Package game for distribution (EXE)
- Write game manual / tutorial
- Create marketing materials (screenshots, trailer concept)
- Time estimate: ~4-5 hours

## Success Criteria by Phase

### Phase 2 (Current - May 2026)
- [ ] All 4 priority tasks completed
- [ ] UI/UX passes usability testing (5+ playtests)
- [ ] Game difficulty is balanced (skilled players win 60-70%)
- [ ] Endless mode has working leaderboard
- [ ] Zero critical bugs (crashes, undefined behavior)
- [ ] Game loop runs at 60 FPS consistently

### Phase 3 (June-August 2026)
- [ ] 3-5 difficulty levels implemented
- [ ] 3-6 tower types with distinct playstyles
- [ ] 3-5 maps with varied layouts
- [ ] 20+ achievements implemented
- [ ] Leaderboards working and persistent
- [ ] Players report 10+ hours enjoyment in testing

### Post-Phase 3 (September+ 2026)
- [ ] Game ready for Steam/itch.io release
- [ ] Community map editor functional
- [ ] Modding documentation complete
- [ ] 100+ downloads in first week

## Resource Allocation

### Developer Time (Your Time)
- **Phase 2 (Apr-May):** 30-40 hours
  - Tasks 1-4: 15-20 hours
  - Testing/bugfixing: 15-20 hours
  
- **Phase 3 (Jun-Aug):** 50-60 hours
  - Content: 30-35 hours
  - Leaderboards/achievements: 10-15 hours
  - Polish/testing: 10-15 hours

- **Total Q2-Q3:** ~80-100 hours over 4 months
- **Pace:** 5-7 hours/week (manageable alongside other work)

### Tools & Infrastructure
- **Pygame:** Already in use, no licensing costs
- **SQLite:** Already in use, no licensing costs
- **Distribution:** itch.io (free), Steam (1-time $100 fee)
- **Testing:** Manual playtesting (no tools needed)

## Risk Assessment

### High Risk
- **Game balance:** Hard to predict if changes make game too easy/hard
  - Mitigation: Playtest heavily, iterate quickly
  
- **Scope creep:** Each task might take 50% longer
  - Mitigation: Set hard time limits, cut features if needed

### Medium Risk
- **Performance:** More towers/enemies might slow down 60 FPS
  - Mitigation: Profile early, optimize if needed
  
- **Database schema changes:** Leaderboards need schema update
  - Mitigation: Plan schema carefully, test migration

### Low Risk
- **Pygame API changes:** Unlikely mid-project
- **Feature confusion:** Clear task descriptions reduce ambiguity

## Pivot Points & Decision Gates

**Gate 1 (May 11, 2026):** Is game balanced and fun?
- If NO: Spend extra 1-2 weeks rebalancing
- If YES: Proceed to Endless mode

**Gate 2 (May 25, 2026):** Does Endless mode add value?
- If NO: Consider alternative endgame features
- If YES: Proceed to Phase 3

**Gate 3 (July 1, 2026):** Do we have enough content for release?
- If NO: Add more maps/towers/difficulties
- If YES: Focus on polish and leaderboards

## Dependencies & Blockers

### Hard Blockers
- None identified - all tasks are independent

### Soft Dependencies
- **Task 1 → Task 2:** Both are UI, can be done in parallel
- **Task 3 → Everything:** Balance must be right before adding modes
- **Task 4 → Phase 3:** Leaderboards only make sense if Endless mode exists

## Conclusion

The project is well-positioned for Phase 2 completion by end of May 2026. Focus should be:
1. **Quality over quantity:** Polish existing features before adding new ones
2. **Player feedback loop:** Playtest early and often
3. **Iteration speed:** Keep changes small and testable
4. **Documentation:** Ensure decisions are recorded for future reference

See `04_implementation_strategy.md` for detailed execution plan.
