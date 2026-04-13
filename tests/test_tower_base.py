"""Tests for Tower base class."""
import pytest
from towers.base import Tower


class TestTower:
    """Tests for Tower class."""

    def test_tower_has_required_attributes(self):
        """Test that Tower has required type annotations."""
        required_attrs = {
            'range', 'power', 'cool_down_time', 'level',
            'pos', 'size', 'color', 'range_enable', 'cool_down'
        }
        assert required_attrs.issubset(set(Tower.__annotations__.keys()))

    def test_tower_has_default_type(self):
        """Test that Tower has default tower_type."""
        assert Tower.tower_type == "Basic"

    def test_tower_has_default_cost(self):
        """Test that Tower has default cost."""
        assert Tower.cost == 100

    def test_tower_has_draw_method(self):
        """Test that Tower has draw method."""
        assert hasattr(Tower, 'draw')
        assert callable(getattr(Tower, 'draw'))

    def test_tower_has_update_method(self):
        """Test that Tower has update method."""
        assert hasattr(Tower, 'update')
        assert callable(getattr(Tower, 'update'))

    def test_tower_has_handle_event_method(self):
        """Test that Tower has handle_event method."""
        assert hasattr(Tower, 'handle_event')
        assert callable(getattr(Tower, 'handle_event'))

    def test_tower_has_find_enemy_method(self):
        """Test that Tower has find_enemy method."""
        assert hasattr(Tower, 'find_enemy')
        assert callable(getattr(Tower, 'find_enemy'))

    def test_tower_has_shot_method(self):
        """Test that Tower has shot method."""
        assert hasattr(Tower, 'shot')
        assert callable(getattr(Tower, 'shot'))

    def test_tower_has_upgrade_method(self):
        """Test that Tower has upgrade method."""
        assert hasattr(Tower, 'upgrade')
        assert callable(getattr(Tower, 'upgrade'))

    def test_tower_has_mouse_functionality_method(self):
        """Test that Tower has mouse_functionality method."""
        assert hasattr(Tower, 'mouse_functionality')
        assert callable(getattr(Tower, 'mouse_functionality'))

    def test_tower_has_distance_squared_method(self):
        """Test that Tower has _distance_squared method."""
        assert hasattr(Tower, '_distance_squared')
        assert callable(getattr(Tower, '_distance_squared'))

    def test_tower_is_object(self):
        """Test that Tower inherits from object."""
        assert issubclass(Tower, object)
