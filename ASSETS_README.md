# Tower Defense Game Assets

This document describes the assets added to the game's main menu.

## Generated Assets

All assets are automatically generated and located in the `assets/` directory:

### Images
- **`assets/images/menu_background.png`** - Tower defense themed menu background
  - 980x600 pixels (matches window size)
  - Features: gradient background, subtle grid pattern, decorative tower elements
  - Created with: Pillow (PIL)

### Sounds
- **`assets/sounds/menu_music.wav`** - Background ambient music for menu
  - 10 seconds looping (seamless)
  - 22050 Hz sample rate, mono, 16-bit
  - Low frequency ambient tone (60 Hz) at 30% volume
  - Created with: Python wave module

- **`assets/sounds/button_click.wav`** - Sound effect for button clicks
  - 0.1 second duration
  - Descending pitch (800 Hz to 300 Hz)
  - Fade-out envelope
  - 22050 Hz sample rate, mono, 16-bit
  - Created with: Python wave module

## Features Implemented

### Menu Background
- The background displays on all menu screens (main menu, map selection, settings)
- Features tower defense game elements (grid, decorative towers with range indicators)
- Falls back to solid color if image cannot be loaded

### Background Music
- Plays automatically when entering the main menu
- Loops continuously at 30% volume
- Stops when starting a game
- Resumes when returning to menu

### Button Click Sounds
- Play at 50% volume when any button is clicked
- Works on all menu buttons (main menu, map selection, settings)

## Generation

To regenerate assets, run:
```bash
python generate_assets.py
```

This is useful if you want to modify asset generation parameters.

## Technical Details

### Asset Loading
- Assets are loaded relative to the project root directory
- The MenuManager handles missing assets gracefully (fallback to default colors)
- pygame.mixer is initialized in game.py for sound support

### Sound Management
- `_play_menu_music()` - Starts looping menu music
- `_stop_menu_music()` - Stops menu music (called when game starts)
- `play_button_sound()` - Plays click sound effect (called when button is clicked)

## Customization

To customize the generated assets, modify the functions in `generate_assets.py`:
- `create_menu_background()` - Change colors, grid size, tower positions
- `create_menu_music()` - Change frequency, duration, volume
- `create_button_click_sound()` - Change pitch, duration, frequency range
