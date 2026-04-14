from enum import Enum


class GameState(Enum):
    """Enum for different game states"""
    MAIN_MENU = "main_menu"
    MAP_SELECTION = "map_selection"
    SETTINGS = "settings"
    MAP_EDITOR = "map_editor"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"
