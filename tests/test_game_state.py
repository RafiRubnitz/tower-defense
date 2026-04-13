"""Tests for GameState enum."""
import pytest
from src.game_state import GameState


class TestGameState:
    """Tests for GameState enum."""

    def test_game_state_main_menu(self):
        """Test MAIN_MENU state exists."""
        assert GameState.MAIN_MENU.value == "main_menu"

    def test_game_state_map_selection(self):
        """Test MAP_SELECTION state exists."""
        assert GameState.MAP_SELECTION.value == "map_selection"

    def test_game_state_settings(self):
        """Test SETTINGS state exists."""
        assert GameState.SETTINGS.value == "settings"

    def test_game_state_playing(self):
        """Test PLAYING state exists."""
        assert GameState.PLAYING.value == "playing"

    def test_game_state_paused(self):
        """Test PAUSED state exists."""
        assert GameState.PAUSED.value == "paused"

    def test_game_state_game_over(self):
        """Test GAME_OVER state exists."""
        assert GameState.GAME_OVER.value == "game_over"

    def test_game_state_victory(self):
        """Test VICTORY state exists."""
        assert GameState.VICTORY.value == "victory"

    def test_all_game_states_unique(self):
        """Test that all GameState values are unique."""
        values = [state.value for state in GameState]
        assert len(values) == len(set(values))

    def test_game_state_is_enum(self):
        """Test that GameState is an Enum."""
        from enum import Enum
        assert issubclass(GameState, Enum)

    def test_game_state_by_name(self):
        """Test accessing GameState by name."""
        assert GameState["MAIN_MENU"] == GameState.MAIN_MENU
        assert GameState["PLAYING"] == GameState.PLAYING

    def test_game_state_by_value(self):
        """Test accessing GameState by value."""
        assert GameState("main_menu") == GameState.MAIN_MENU
        assert GameState("playing") == GameState.PLAYING
