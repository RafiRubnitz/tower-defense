"""Tests for Enemy base class."""
import pytest
from enemies.base import Enemy


class TestEnemyBase:
    """Tests for Enemy base class."""

    def test_enemy_has_required_attributes(self):
        """Test that Enemy has required type annotations."""
        required_attrs = {
            'id', 'life_point', 'speed', 'level',
            'size', 'color', 'pos', 'previous_pos'
        }
        assert required_attrs.issubset(set(Enemy.__annotations__.keys()))

    def test_enemy_has_uuid_class_variable(self):
        """Test that Enemy has _UUID class variable."""
        assert hasattr(Enemy, '_UUID')
        assert Enemy._UUID == 0

    def test_enemy_get_next_uuid(self):
        """Test get_next_uuid classmethod."""
        # Store initial UUID
        initial_uuid = Enemy._UUID

        # Get next UUID
        uuid1 = Enemy.get_next_uuid()
        assert uuid1 == initial_uuid + 1

        # Get another UUID
        uuid2 = Enemy.get_next_uuid()
        assert uuid2 == uuid1 + 1
        assert uuid2 > uuid1

    def test_enemy_get_next_uuid_increments(self):
        """Test that get_next_uuid increments correctly."""
        # Reset to 0
        Enemy._UUID = 0

        uuid1 = Enemy.get_next_uuid()
        assert uuid1 == 1

        uuid2 = Enemy.get_next_uuid()
        assert uuid2 == 2

        uuid3 = Enemy.get_next_uuid()
        assert uuid3 == 3

    def test_enemy_has_update_method(self):
        """Test that Enemy has update method."""
        assert hasattr(Enemy, 'update')
        assert callable(getattr(Enemy, 'update'))

    def test_enemy_has_draw_method(self):
        """Test that Enemy has draw method."""
        assert hasattr(Enemy, 'draw')
        assert callable(getattr(Enemy, 'draw'))

    def test_enemy_has_move_method(self):
        """Test that Enemy has move method."""
        assert hasattr(Enemy, 'move')
        assert callable(getattr(Enemy, 'move'))

    def test_enemy_has_hit_method(self):
        """Test that Enemy has hit method."""
        assert hasattr(Enemy, 'hit')
        assert callable(getattr(Enemy, 'hit'))

    def test_enemy_has_death_method(self):
        """Test that Enemy has death method."""
        assert hasattr(Enemy, 'death')
        assert callable(getattr(Enemy, 'death'))

    def test_enemy_is_object(self):
        """Test that Enemy inherits from object."""
        assert issubclass(Enemy, object)
