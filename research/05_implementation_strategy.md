# Implementation Strategy - Detailed Execution Plan

**Document created:** April 14, 2026  
**Target completion:** May 25, 2026  
**Pace:** 5-10 hours/week

## Overview

This document provides specific, actionable steps for completing the 4 priority tasks in sequence. Each task includes code locations, exact changes needed, and validation steps.

## Task 1: Fix Map Selection UI Layout (30 minutes)

### Status
**Branch:** Currently on feature/tower-selection-ui  
**To do:** 
1. Switch to feature branch for this task (or continue on current)
2. Make 2 changes to ui/menu.py
3. Test visually
4. Commit

### Step-by-step

**Step 1.1: Locate the button code**
- File: `ui/menu.py`
- Search for: "Start: " button definition
- Expected: Lines ~236-240 (approximate)
- Look for: pygame.Rect with width=200

**Step 1.2: Change 1 - Increase button width**
```python
# BEFORE:
start_button = pygame.Rect(map_x - 100, map_y + 320, 200, 50)

# AFTER:
start_button = pygame.Rect(map_x - 140, map_y + 320, 280, 50)
```
**Why:** 280px width accommodates longest map names, adjust x offset to keep centered

**Step 1.3: Change 2 - Verify button positioning**
- Confirm button is centered horizontally (x = map_x - width/2)
- For 280px width: x = map_x - 140 ✓

**Step 1.4: Test visually**
```bash
python run.py
```
- Navigate to map selection screen
- Check each map name fits in button
- Longest: "Spiral Madness" (14 chars) - should fit
- Button should be centered below map preview

**Step 1.5: Commit**
```bash
git add ui/menu.py
git commit -m "Task 1: Adjust map selection button width and positioning for longer map names"
```

### Acceptance Criteria Checklist
- [ ] All map names visible (no overflow)
- [ ] Button visually centered on screen
- [ ] No text cutoff or distortion
- [ ] Game still runs without errors

### Rollback Plan
```bash
git revert <commit-hash>  # Reverts width back to 200px
```

---

## Task 2: Tower Design & Selection UI (4-6 hours)

### Status
**Branch:** Create feature/tower-visuals  
**Subtasks:** 3 (tower visuals, selector styling, refinement)

### Approach
Tower visuals have two parts: (1) how towers appear on the map, and (2) how towers appear in the selector panel.

### Change 1: Add color/shape properties to towers

**File:** `towers/base.py` (or where BasicTower is defined)

**Step 2.1: Add color property to tower base class**
```python
class Tower:
    # ... existing code ...
    
    # Add color for rendering:
    color = (100, 100, 200)  # Default blue (RGB)
```

**Step 2.2: Override in each tower subclass**
Example implementations:
```python
# towers/basic.py
class BasicTower(Tower):
    color = (50, 120, 200)      # Dark blue
    shape = "circle"

# towers/freeze.py
class FreezeTower(Tower):
    color = (100, 200, 255)     # Cyan
    shape = "square"

# towers/laser.py
class LaserTower(Tower):
    color = (255, 50, 50)       # Red
    shape = "diamond"
```

**Step 2.3: Update tower rendering in tower.py**
- Find tower.draw() or where towers are rendered on map
- Use tower.color instead of hardcoded color
- Update shape rendering (circle vs square vs diamond)

**Time estimate:** 1-2 hours

### Change 2: Redesign tower selector panel

**File:** `ui/tower_selector.py`

**Step 2.4: Examine current selector layout**
```bash
# Check what tower_selector.py currently renders
grep -n "def draw\|def render" ui/tower_selector.py
```

**Step 2.5: Plan new layout**
```
┌─────────────────────────────────┐
│   Tower Selector Panel          │
├─────────────────────────────────┤
│  [Blue Circ] BasicTower   Cost: $100
│  Range: 3.5  Damage: 50   Cooldown: 600ms
│  ─────────────────────────────  │
│  [Cyan Squa] FreezeTower  Cost: $120
│  Range: 2.5  Damage: 30   Cooldown: 800ms
│  ─────────────────────────────  │
│  [Red  Diam] LaserTower   Cost: $150
│  Range: 4.0  Damage: 70   Cooldown: 500ms
│  ═════════════════════════════  │ ← Selected
│                                 │
│  $ 450 / Lives: 10              │
└─────────────────────────────────┘
```

**Step 2.6: Implement selector panel redesign**
- Draw background box with border
- For each tower type, show:
  - Tower preview (colored icon)
  - Name
  - Cost
  - Stats (range, damage, cooldown)
- Highlight selected tower with darker background
- Update player money/lives display

**Time estimate:** 2-3 hours

### Change 3: Add hover effects

**Step 2.7: Track mouse position in Round class**
- Pass mouse position to selector.draw()
- Check if mouse over tower entry
- Draw hover highlight (slightly lighter background)

**Step 2.8: Test interaction**
- Run game, navigate to tower selection
- Hover over different towers
- Verify highlighting works
- Click to select towers
- Verify selection persists

**Time estimate:** 1 hour

### Testing for Task 2

```bash
python run.py
1. Go to map selection
2. Start game
3. Check tower selector panel:
   - [ ] Each tower visually distinct
   - [ ] Colors are clear and different
   - [ ] Stats displayed clearly
   - [ ] Cost shown prominently
   - [ ] Selection highlighting works
   - [ ] Hover effects work
4. Verify towers on map use new colors
5. Place some towers, verify colors match selector
```

### Acceptance Criteria Checklist
- [ ] Each tower type has distinct color
- [ ] Tower shapes differ (circle, square, diamond)
- [ ] Selector panel is styled with background/border
- [ ] All stats displayed (range, damage, cooldown, cost)
- [ ] Selected tower is highlighted
- [ ] Hover effects provide visual feedback
- [ ] Game functions correctly with new visuals

### Commit
```bash
git add towers/ ui/tower_selector.py
git commit -m "Task 2: Add unique tower visuals and redesigned selector panel"
```

### Rollback Plan
```bash
git revert <commit-hash>  # Reverts to default colors
```

---

## Task 3: Increase Game Difficulty (4-6 hours + 2-3 hours playtesting)

### Status
**Branch:** Create feature/difficulty-balance  
**Approach:** Make surgical changes, test between each change

### Step-by-step

**Step 3.1: Identify current baseline**
Play 1 full game with current settings:
- How many towers placed by wave 5? (Aim: 5-7)
- What's final money remaining? (Aim: $0-50)
- Did you need to plan tower placement? (Aim: YES)
- Time to complete? (Should be 20-30 min)

**Step 3.2: Increase enemy stats (Change 1)**
**File:** `enemy.py` or wherever Soldier is defined

```python
# BEFORE:
class Soldier(Enemy):
    max_health = 100
    speed = 2.0
    bounty = 15

# AFTER:
class Soldier(Enemy):
    max_health = 150      # +50% health
    speed = 2.5           # +25% speed
    bounty = 13           # -13% bounty (don't round exactly)
```

**Reasoning:** Harder enemies = more money needed for towers

**Step 3.3: Adjust wave composition (Change 2)**
**File:** `map.py` - find Wave.spawn_enemies() or similar

Look for code like:
```python
# BEFORE:
enemy_count = 3 + (wave_number * 0.3)
spawn_interval = 2000  # 2 seconds

# AFTER:
enemy_count = 3 + (wave_number * 0.5)  # More enemies
spawn_interval = 1500  # Spawn faster (1.5 sec)
```

**Step 3.4: Reduce starting money (Change 3)**
**File:** `ui/menu.py` or `database.py`

Look for:
```python
# BEFORE:
starting_money = 450

# AFTER:
starting_money = 350  # -$100 (forces harder choices)
```

**Step 3.5: Increase tower cost (Change 4)**
**File:** `database.py` or tower class definitions

```python
# BEFORE:
BasicTower.cost = 100

# AFTER:
BasicTower.cost = 120  # +20%
```

**Step 3.6: Adjust difficulty multiplier (Change 5)**
**File:** `src/difficulty.py`

```python
# BEFORE:
multiplier = 1.0 + (wave_number * 0.05)  # 1.0, 1.05, 1.10, ...

# AFTER:
multiplier = 1.0 + (wave_number * 0.08)  # 1.0, 1.08, 1.16, ...
```

### Testing for Task 3 (Critical!)

**Playtest procedure:**
1. Start game with new settings
2. Play through all waves
3. Evaluate:
   - Can I afford first tower? (Should be YES, ~1 min)
   - Must I think about placement? (Should be YES)
   - Do waves get progressively hard? (Should be CLEAR YES)
   - Did I win? (Should be: 60-70% of attempts)
   - Time spent: 20-30 minutes

**Iteration loop:**
```
Play game → Evaluate difficulty → Adjust → Repeat
```

**Acceptance criteria:**
- Can afford first tower in first 1-2 minutes
- Waves 1-3 are manageable
- Waves 4-5 are challenging
- Win rate across 5 playtests: 60-70%
- Each wave clearly harder than previous

**If too hard (losing every game):**
- Reduce `enemy_count` multiplier
- Increase `starting_money` back to 380-400
- Reduce enemy health increase (150 → 130)

**If too easy (winning easily):**
- Increase `spawn_interval` (shorter = harder)
- Increase `difficulty_multiplier` more
- Reduce `starting_money` more (350 → 320)

### Commits for Task 3
After each change that works:
```bash
git add <changed-files>
git commit -m "Task 3: Increase [enemy stats|wave composition|starting money|tower cost] difficulty"
```

### Final commit
```bash
git commit -m "Task 3: Increase overall game difficulty - balanced after 5+ playtests"
```

---

## Task 4: Infinite Waves Mode (6-8 hours)

### Status
**Branch:** Create feature/infinite-waves  
**Approach:** Modular - add menu option first, then wave generation, then leaderboard

### Step-by-step

**Step 4.1: Add game mode selection to menu**
**File:** `ui/menu.py`

Add new screen after main menu:
```
┌─────────────────────────────────┐
│       Game Mode Selection       │
├─────────────────────────────────┤
│                                 │
│  [ Classic Mode ]               │
│  10 waves, complete and win     │
│                                 │
│  [ Endless Mode ]               │
│  Infinite waves, chase high score
│                                 │
│  [ Back ]                       │
└─────────────────────────────────┘
```

**Step 4.2: Add mode to GameState**
**File:** `src/game_state.py`

```python
class GameState(Enum):
    MAIN_MENU = 1
    MODE_SELECTION = 2  # NEW
    MAP_SELECTION = 3
    # ... rest unchanged
```

**Step 4.3: Store mode selection in Round**
**File:** `map.py`

When Round created, store:
```python
self.game_mode = "classic"  # or "endless"
self.wave_limit = 10 if game_mode == "classic" else None
```

**Step 4.4: Implement infinite wave generation**
**File:** `map.py` - add to Wave class

```python
@classmethod
def generate_infinite_wave(cls, wave_number):
    """Generate a wave for infinite mode."""
    # Calculate difficulty
    base_multiplier = 1.0 + (wave_number * 0.08)
    
    # Calculate enemy count
    enemy_count = int(3 + (wave_number * 0.5))
    
    # Mix enemy types (more variety as waves progress)
    if wave_number < 5:
        types = ["Soldier"]  # Only soldiers early
    elif wave_number < 10:
        types = ["Soldier", "Scout"]  # Add fast enemies
    else:
        types = ["Soldier", "Scout", "Tank"]  # Add tanks
    
    # Create wave config
    wave_config = {
        "enemies": enemy_count,
        "multiplier": base_multiplier,
        "composition": types,
        # ... other config
    }
    
    return cls.from_config(wave_config)
```

**Step 4.5: Update Round to generate waves dynamically**
**File:** `map.py`

```python
# In Round.advance_wave():
if self.game_mode == "classic":
    self.current_wave = db.get_wave_config(...)
elif self.game_mode == "endless":
    self.current_wave = Wave.generate_infinite_wave(self.wave_number)
    self.wave_number += 1
```

**Step 4.6: Add wave counter to UI**
**File:** `ui/menu.py` or `map.py` (rendering code)

Display during gameplay:
- Current wave number (e.g., "Wave 5" or "Endless: 5")
- Survival time if in endless mode
- High score for endless mode

**Step 4.7: Implement leaderboard storage**
**File:** `database.py`

Add schema update:
```python
# Create endless_scores table
CREATE TABLE IF NOT EXISTS endless_scores (
    id INTEGER PRIMARY KEY,
    player_name TEXT,
    max_wave INTEGER,
    survival_time INTEGER,  # In seconds
    score INTEGER,
    timestamp DATETIME,
    map_id INTEGER
);
```

**Step 4.8: Save score on game over**
**File:** `game.py` or Round class

```python
def save_endless_score(self, map_id, max_wave, survival_time):
    from database import Database
    db = Database()
    db.save_endless_score(
        player_name="Player",  # Could be configurable
        max_wave=max_wave,
        survival_time=survival_time,
        score=max_wave * 100 + survival_time,  # Scoring formula
        map_id=map_id
    )
    db.close()
```

**Step 4.9: Display high score on game over screen**
**File:** Game over screen rendering

```
Game Over!
─────────
Max Wave: 23
Survival Time: 12m 34s
Score: 2534

High Score: 3012 (8 waves ago)

[ Restart ]  [ Main Menu ]
```

### Testing for Task 4

**Test 1: Mode selection**
```bash
python run.py
- [ ] Mode selection screen appears after main menu
- [ ] Clicking "Classic" goes to map selection
- [ ] Clicking "Endless" goes to map selection
- [ ] Selected mode is remembered
```

**Test 2: Infinite wave generation**
```bash
# Play endless mode for 15-20 minutes
- [ ] Waves spawn indefinitely (past wave 10)
- [ ] Each wave slightly harder than previous
- [ ] Wave counter increments correctly
- [ ] Game doesn't crash at wave 100+
```

**Test 3: Wave difficulty progression**
```
Expected progression:
Wave 1: 3 enemies, 1.0x multiplier
Wave 5: 5 enemies, 1.32x multiplier
Wave 10: 8 enemies, 1.64x multiplier
Wave 50: 28 enemies, 5.0x multiplier

Check: Difficulty doesn't spike too hard
       (Each wave 5-10% harder than previous)
```

**Test 4: Leaderboard persistence**
```bash
# Play game 1: Reach wave 20
- [ ] Score saved to database

# Play game 2: Reach wave 15
- [ ] Previous high score shown
- [ ] Leaderboard updated correctly
```

**Test 5: Game over screen**
```bash
# Lose in endless mode
- [ ] High score displayed
- [ ] Final wave number shown
- [ ] Survival time correct
- [ ] Restart button works
```

### Acceptance Criteria Checklist
- [ ] Game mode selection works
- [ ] Infinite waves generate correctly (tested to wave 100+)
- [ ] Wave difficulty progresses smoothly
- [ ] Leaderboard saves scores persistently
- [ ] Game over screen shows high score
- [ ] Wave counter displays correctly
- [ ] No crashes in 30+ minute endless sessions

### Commits for Task 4
```bash
# After each milestone:
git commit -m "Task 4: Add game mode selection screen"
git commit -m "Task 4: Implement infinite wave generation"
git commit -m "Task 4: Add leaderboard storage and display"
git commit -m "Task 4: Complete infinite waves mode - tested and balanced"
```

---

## Overall Testing Checklist

After all 4 tasks complete:

```
UI/UX Tests:
- [ ] All buttons are aligned and readable
- [ ] No text overflow or cutoff anywhere
- [ ] Window renders at 60 FPS consistently
- [ ] All menus respond to clicks without lag

Game Logic Tests:
- [ ] Starting a game works (all modes)
- [ ] Towers place and shoot correctly
- [ ] Enemies spawn and follow path
- [ ] Win/lose conditions trigger correctly
- [ ] Pause/unpause works
- [ ] Restart button works

Balance Tests:
- [ ] Classic mode: win rate 60-70% for skilled players
- [ ] Endless mode: waves get progressively harder
- [ ] Starting money allows 2-3 towers by wave 2
- [ ] Wave 5 requires strategic placement

Content Tests:
- [ ] All maps selectable and playable
- [ ] All tower types display correctly
- [ ] All enemy types spawn correctly
- [ ] Leaderboard shows scores (Endless mode)
```

---

## Expected Timeline

| Task | Time | Status |
|------|------|--------|
| Task 1: UI Fix | 0.5 hr | ✅ Start immediately |
| Task 2: Tower Visuals | 5 hrs | Start after Task 1 |
| Task 3: Difficulty | 6-8 hrs | Start after Task 2 |
| Task 4: Infinite Waves | 8 hrs | Start after Task 3 |
| **Total** | **19-22 hrs** | **Complete by May 25** |

**At 7-10 hours/week: 2-3 weeks of work**

---

## Conclusion

This implementation strategy provides specific, actionable steps for each task. Follow the order listed, test thoroughly between tasks, and don't move to the next task until acceptance criteria pass.

Key principles:
- Small, verifiable changes
- Test immediately after each change
- Commit working code frequently
- Iterate if something doesn't feel right
- Document decisions in commit messages

Good luck! 🎮
