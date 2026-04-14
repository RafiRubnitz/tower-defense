---
task_id: 1
priority: MEDIUM
title: Fix Map Selection UI Layout
status: COMPLETED
---

## Summary
Fixed map selection screen layout issue where "Start Game" button text would overflow when map names were long. Increased button width from 200px to 280px to accommodate longer text without truncation.

## Changes
- `ui/menu.py:224` - Increased `button_width` from 200 to 280 in `_init_map_selection()`
  - Button now centers properly with new dimensions
  - Map names fit completely without text overflow

## Solution Details
The issue was in the `_init_map_selection()` method where the start button was created with a fixed width of 200px. When the map name was long, the button text "Start: {map_name}" would overflow or get truncated.

By increasing the width to 280px:
- Longer map names now fit completely on the button
- Center alignment automatically adjusts due to formula: `(screen_width - button_width) // 2`
- No breaking changes to other UI elements

## Commits
- a229406: task/1 - Increase map selection button width from 200px to 280px

## Tests Completed
- [x] Game starts without errors
- [x] Map selection screen displays correctly
- [x] Button centers properly on screen
- [x] Text no longer overflows for long map names
- [x] Layout consistent with longest map names in database
