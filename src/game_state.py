from enum import Enum


class GameState(Enum):
    """Enum for different game states"""
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"
