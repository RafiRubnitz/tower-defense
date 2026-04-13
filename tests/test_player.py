"""Tests for Player class."""
import pytest
from player import Player


class TestPlayer:
    """Tests for Player class."""

    def test_player_has_money_annotation(self):
        """Test that Player has money type annotation."""
        assert 'money' in Player.__annotations__
        assert Player.__annotations__['money'] is int

    def test_player_has_heart_annotation(self):
        """Test that Player has heart type annotation."""
        assert 'heart' in Player.__annotations__
        assert Player.__annotations__['heart'] is int

    def test_player_is_object(self):
        """Test that Player inherits from object."""
        assert issubclass(Player, object)

    def test_player_has_annotations(self):
        """Test that Player has proper type annotations."""
        assert hasattr(Player, '__annotations__')
        assert len(Player.__annotations__) == 2

    def test_player_annotations_keys(self):
        """Test all expected annotation keys exist."""
        expected_keys = {'money', 'heart'}
        actual_keys = set(Player.__annotations__.keys())
        assert expected_keys == actual_keys
