# Task Dependency Analysis - Priority Queue

**Current Date:** April 14, 2026

## Task Overview

There are 4 priority tasks in the immediate queue:

```
Task 1: Fix Map Selection UI Layout        [INDEPENDENCE: HIGH]
Task 2: Tower Design & Selection UI        [INDEPENDENCE: HIGH]
Task 3: Increase Game Difficulty           [INDEPENDENCE: MEDIUM]
Task 4: Infinite Waves Mode                [INDEPENDENCE: MEDIUM]
```

## Dependency Graph

```
Task 1 (UI Fix)          Task 2 (Tower UI)
    ↓                          ↓
[Independent paths]     [Independent paths]
    ↓                          ↓
    └──────────┬───────────────┘
               ↓
Task 3 (Difficulty)  ← Blocks Task 4
               ↓
               Task 4 (Infinite Waves)
```

## Detailed Task Analysis

### Task 1: Fix Map Selection UI Layout
**Status:** IN PROGRESS (started Apr 14)  
**Priority:** HIGH (blocks testing of other features)  
**Complexity:** ⭐ (simple)

**What it does:**
- Increases start button width from 200px → 280px
- Centers button properly on screen
- Ensures long map names don't overflow

**Files affected:**
- ui/menu.py (1 file, ~5 lines changed)

**Time estimate:** 30 minutes  
**Blockers:** None  
**Blocks:** Nothing hard, but improves user experience before other features

**Acceptance criteria:**
- All map names fit completely in button
- Button visually centered below preview
- No text cutoff or overflow

**Post-completion impact:**
- Game looks more professional
- Testing can proceed without visual distraction
- Baseline for UI improvements in Task 2

---

### Task 2: Tower Design & Selection UI
**Status:** PENDING  
**Priority:** HIGH (visual polish)  
**Complexity:** ⭐⭐ (moderate)

**What it does:**
- Adds unique visual appearance to each tower type
  - BasicTower: Blue, circular
  - FreezeTower: Cyan, square
  - LaserTower: Red, diamond
  - (Extendable for new tower types)
- Redesigns tower selector panel
- Adds hover effects and selection feedback

**Files affected:**
- towers/*.py (3-4 files, add color/shape properties)
- ui/tower_selector.py (redesign panel rendering)

**Time estimate:** 4-6 hours  
**Blockers:**
- Recommended (not required): Task 1 should be done first (cleaner testing environment)

**Blocks:** Nothing - Task 3 and 4 are independent

**Acceptance criteria:**
- Each tower type visually distinct
- Selector panel shows tower name, cost, stats (range, damage, cooldown)
- Selected tower is highlighted
- Hover effects provide visual feedback

**Post-completion impact:**
- Game feels more polished
- Players can distinguish tower types at a glance
- Better foundation for adding new tower types in Phase 3

**Technical considerations:**
- Tower drawing code is in tower.py
- Need to add color properties to each tower class
- Need to ensure selector panel can scale with new tower types

---

### Task 3: Increase Game Difficulty
**Status:** PENDING  
**Priority:** CRITICAL (game balance)  
**Complexity:** ⭐⭐⭐ (complex, requires playtesting)

**What it does:**
- Adjusts enemy stats
  - Health: Soldier 100 → 150
  - Speed: Soldier 2.0 → 2.5
  - Bounty: -10% gold rewards
- Increases wave difficulty
  - Higher enemy counts per wave
  - Shorter spawn intervals
  - More dangerous enemy mixes
- Reduces starting resources
  - Money: 450 → 350
  - Tower cost: 100 → 120
- Adjusts difficulty multiplier formula

**Files affected:**
- enemy.py (enemy base stats)
- map.py (wave composition, spawning)
- ui/menu.py (starting money defaults)
- src/difficulty.py (multiplier formula)

**Time estimate:** 4-6 hours (including 3-5 playtest sessions)  
**Blockers:** None hard, but recommend Tasks 1-2 complete first (cleaner testing)

**Blocks:** Task 4 (Infinite Waves should use balanced difficulty as baseline)

**Acceptance criteria:**
- Skilled player wins in 60-70% of attempts
- Unskilled player struggles (needs strategy)
- Difficulty feels progressive (waves get harder)
- Bounties vs tower costs balanced (not trivial to afford towers)

**Post-completion impact:**
- Game has meaningful challenge
- Players must use tower placement strategy
- Establishes difficulty baseline for Task 4

**Testing requirements:**
- Playtest 5-10 full runs
- Try different tower placement strategies
- Verify wave 1 is achievable, wave 5 is hard
- Check if starting money allows first 2-3 towers

**Iteration risk:** High
- Changes to enemy stats cascade to wave composition
- Difficulty balance is subjective (may need multiple iterations)
- Playtesters may have different skill levels

---

### Task 4: Infinite Waves Mode
**Status:** PENDING  
**Priority:** HIGH (replayability)  
**Complexity:** ⭐⭐⭐⭐ (complex, new system)

**What it does:**
- Adds game mode selection (Classic 10-wave vs Infinite)
- Implements infinite wave generation algorithm
  - Wave difficulty scales: `1.0 + (wave_number * 0.08)`
  - Enemy count scales: `3 + (wave_number * 0.5)`
  - Enemy composition evolves per wave
- Creates scoring system for Endless mode
- Implements persistent leaderboard
- Adds UI elements: wave counter, survival timer, high score display

**Files affected:**
- map.py (add Wave.generate_infinite_wave() method)
- ui/menu.py (add mode selection screen)
- database.py (update schema for leaderboard scores)
- game.py (possibly update state handling)

**Time estimate:** 6-8 hours  
**Blockers:**
- MUST complete Task 3 first (Infinite Waves needs balanced difficulty to be fun)
- SHOULD complete Tasks 1-2 first (cleaner development environment)

**Blocks:** Nothing - but is required for Phase 3 leaderboard features

**Acceptance criteria:**
- Mode selection works in menu
- Infinite waves spawn correctly up to wave 100+
- Waves get progressively harder (not exponentially)
- Leaderboard scores persist across sessions
- Score displayed prominently on game over screen
- High score shown in menu

**Post-completion impact:**
- Game has 5-10x replayability
- Creates competitive element (high score chasing)
- Foundation for multiplayer leaderboards in Phase 3
- Enables achievement system ("Survive 50 waves" etc.)

**Technical complexity:**
- Wave generation algorithm is new (needs design)
- Database schema changes need careful migration
- Leaderboard ranking logic (sorting, ties)
- UI needs to show both wave number and survival time

**Iteration risk:** Medium
- Wave generation math might be too easy/hard
- Scoring might not be motivating enough
- Leaderboard might feel incomplete without more features

---

## Recommended Execution Order

### Path A: Sequential (Safer, lower risk)
```
1. Task 1 (30 min)      ← Foundation
2. Task 2 (4-6 hours)   ← Build on Task 1
3. Task 3 (4-6 hours)   ← Balance before features
4. Task 4 (6-8 hours)   ← Build on Task 3
─────────────────────────
Total: 14-20 hours
Timeline: 2-3 weeks at 7-10 hours/week
```

**Pros:**
- Each task builds on clean foundation
- Testing environment improves progressively
- Clear success criteria at each step
- Easy to pause and resume

**Cons:**
- Takes longer overall
- Tasks 1-2 can't be parallelized with Tasks 3-4

### Path B: Parallel (Faster, higher risk)
```
Start simultaneously:
- Developer A: Tasks 1-2 (UI)    [6-6.5 hours]
- Developer B: Task 3 (Balance)  [4-6 hours]

Then:
- Both: Task 4 (Waves)           [6-8 hours]
─────────────────────────────────────────────
Total: 16-20 hours
Timeline: 2-3 weeks with 2 developers
```

**Pros:**
- Faster completion
- Parallel work on UI and balance
- Both done sooner

**Cons:**
- Requires coordination
- Harder to debug cross-task issues
- Only viable with 2+ developers

### Recommended: Path A (Sequential)
**Reasoning:**
- You're working solo (based on git history)
- Tasks build logically on each other
- Lower risk of integration problems
- Clear milestones every 30 mins - 6 hours

## Parallelization Opportunities

### CAN run in parallel:
- Task 1 and Task 2 (both UI, don't interfere)
- Research/design for Task 4 while doing Task 3

### MUST run sequentially:
- Task 3 before Task 4 (balance is prerequisite)
- Task 1 recommended before Task 2 (cleaner testing)

## Exit Criteria & Rollback

### Task 1
- **Success:** Button text visible, centered
- **Rollback:** Revert ui/menu.py to previous commit
- **Effort:** ~1 minute

### Task 2
- **Success:** Towers look distinct, selector works
- **Rollback:** Revert tower colors to defaults, revert ui/tower_selector.py
- **Effort:** ~5 minutes

### Task 3
- **Success:** Game is challenging (>5 playtests pass)
- **Rollback:** Revert enemy stats to previous values
- **Effort:** ~10 minutes, but may need re-iteration

### Task 4
- **Success:** Infinite waves generate correctly, leaderboard works
- **Rollback:** Revert map.py, database.py, ui/menu.py
- **Effort:** ~10 minutes

## Testing Strategy

### Task 1-2 Testing
- Visual inspection of UI
- Check all button states (normal, hover, clicked)
- Test with longest map name in database
- No gameplay changes needed

### Task 3 Testing (Most important)
- Play 10 full games on each map
- Try different tower placement strategies
- Time first 2 towers (should be achievable in <5 min)
- Time final tower (should be challenging)
- Check if player can afford towers from bounties

### Task 4 Testing
- Run infinite waves to wave 100 (15-20 mins)
- Check wave difficulty progression (not too easy, not instant loss)
- Verify leaderboard saves scores
- Compare scores across multiple runs

## Conclusion

All 4 tasks are achievable within 2-3 weeks at a comfortable pace (7-10 hours/week).

**Recommended path:**
1. Complete Task 1 immediately (quick win)
2. Do Task 2 next week (visual improvements)
3. Start Task 3 playtest loop (balance iterations)
4. Once Task 3 is balanced, tackle Task 4 (new features)

This order:
- Builds confidence (quick wins first)
- Improves game quality progressively
- Minimizes integration issues
- Maintains flexible pivoting if challenges arise

See `05_implementation_strategy.md` for detailed implementation steps.
