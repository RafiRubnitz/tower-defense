---
task_id: map_editor
priority: HIGH
title: Map Editor - Draw custom maps with auto-generated waves
status: COMPLETED
---

## Summary
Custom map editor feature fully implemented. Players can draw maps on a 40x30 grid by clicking cells in sequence, name them, save to DB, and auto-generate wave configurations. Custom maps appear in map selection alongside built-in maps.

## Architecture

### New Files
- `ui/map_editor.py` - Interactive map drawing UI (MapEditorScreen class)
- `map_wave_generator.py` - Auto-generates and saves wave configs to DB
- `tests/test_map_editor.py` - 23 test cases covering all functionality

### Modified Files
- `src/game_state.py` - Added MAP_EDITOR state
- `ui/menu.py` - Added "Create Map" button and event handling
- `game.py` - Route MAP_EDITOR events and drawing, lazy initialize MapEditorScreen

## Feature Flow

1. **Main Menu** → Click "Create Map" button
   - Transitions to MAP_EDITOR state
   - Initializes MapEditorScreen (lazy, on first event)

2. **Map Editor UI** - 40x30 grid with right control panel
   - **Drawing**: Click cells in sequence to draw path
   - Each cell must be adjacent to previous (4-directional, no diagonals)
   - Path shows as gray cells with yellow connecting lines
   - Green border on start cell, red border on end cell
   - **Input**: Name text field (max 25 chars)
   - **Actions**: 
     - Save: Validates path (min 5 cells, no gaps), saves map + generates waves
     - Clear: Reset path
     - Back: Return to MAP_SELECTION without saving
   - **Feedback**: Error messages (red text) show validation failures for 1 second

3. **Auto Wave Generation** (WaveGenerator)
   - Creates round_config for map (difficulty_multiplier based on difficulty)
   - Generates 5 wave_configs with scaling enemy composition:
     - Wave 1-2: Soldiers only
     - Wave 3-4: 70% Soldiers, 30% Tanks
     - Wave 5: 50% Soldiers, 25% Tanks, 20% Scouts, 5% Boss
   - Saves all to DB

4. **Return to Map Selection**
   - Custom map now appears in selection list
   - Can be played like built-in maps

## Technical Details

### Path Data Format
- Stored in DB as JSON: `[[0,15], [1,15], ..., [20,29]]`
- Grid coordinates (col, row), NOT pixel coordinates
- Convert to pixels: `(col * 20, row * 20)`

### Validation Rules
- Path minimum 5 cells
- All consecutive cells must be adjacent (Manhattan distance = 1)
- No reversing (cell cannot be re-added to path)

### Wave Generation Logic
- Uses existing `calculate_wave_enemy_count()` and `calculate_wave_enemy_hp()` from map.py
- Spawn interval: `max(30, 120 - wave_num * 15)` (faster in later waves)
- Round config: 450 money, 10 lives, 100 tower cost, 1.0 base difficulty

### Integration Points
- MapEditorScreen.save_map() calls db.save_map() + wave_generator.generate_for_map()
- Game._init_map_editor() lazy-loads MapEditorScreen on first MAP_EDITOR event
- Game routes MAP_EDITOR events/updates/draws; handles state transitions
- MenuManager._on_create_map_click() sets state to MAP_EDITOR

## Tests Completed
- [x] Wave generator creates round and wave configs
- [x] Wave enemy composition scales correctly by wave number
- [x] Path adjacency validation (4-directional)
- [x] Path length validation (min 5 cells)
- [x] Path gap detection
- [x] Map persistence (save/retrieve from DB)
- [x] Duplicate map name handling (updates existing)
- [x] Wave config save and retrieval
- All 23 tests pass

## Code Patterns
- MapEditorScreen: pygame UI pattern (handle_event, update, draw)
- WaveGenerator: Dependency injection (db passed to methods)
- Tests: pytest with in-memory SQLite DB for integration tests
- Error handling: Validation errors shown to user, exceptions caught in save

## UI Layout
```
[40x30 Grid] [Control Panel]
- 800x600    - Name input
             - Path cell count
             - Save button
             - Clear button  
             - Back button
             - Error message (red)
```

## Edge Cases Handled
- Non-adjacent cell click → Shows "Must connect to last cell" error
- Path too short → "Path too short (3/5)" error
- Duplicate map name → Updates existing map (DB behavior)
- Save error → Shows "Save failed: ..." with partial error text
- Name input active → Text field highlighted blue
