---
task_id: 2
priority: CRITICAL
title: Map Selection Screen - Choose from available maps
status: COMPLETED
---

## Summary
Enhanced existing map selection screen with a visual mini-map preview panel. Left column shows clickable map list; right side renders path layout preview with start/end markers, difficulty, and path length. Base map selection existed; this task adds real map visualization.

## Changes
- ui/menu.py: Added _draw_map_preview() method with mini-map rendering
- ui/menu.py: Stored selected_map_data on selection for preview
- ui/menu.py: Reorganized layout (left list, right preview)

## Commits
- 1912aff: task/2: Enhance Map Selection Screen with visual map preview

## Tests Completed
- [x] Feature works as intended
- [x] No regressions
- [x] Code follows project patterns
