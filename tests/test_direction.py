"""Tests for Direction enum."""
import pytest
from src.direction import Direction


class TestDirection:
    """Tests for Direction enum."""

    def test_direction_up(self):
        """Test UP direction."""
        assert Direction.UP.x == -1
        assert Direction.UP.y == 0
        assert Direction.UP.value == (-1, 0)

    def test_direction_down(self):
        """Test DOWN direction."""
        assert Direction.DOWN.x == 1
        assert Direction.DOWN.y == 0
        assert Direction.DOWN.value == (1, 0)

    def test_direction_left(self):
        """Test LEFT direction."""
        assert Direction.LEFT.x == 0
        assert Direction.LEFT.y == -1
        assert Direction.LEFT.value == (0, -1)

    def test_direction_right(self):
        """Test RIGHT direction."""
        assert Direction.RIGHT.x == 0
        assert Direction.RIGHT.y == 1
        assert Direction.RIGHT.value == (0, 1)

    def test_direction_upleft(self):
        """Test UPLEFT direction."""
        assert Direction.UPLEFT.x == -1
        assert Direction.UPLEFT.y == -1
        assert Direction.UPLEFT.value == (-1, -1)

    def test_direction_upright(self):
        """Test UPRIGHT direction."""
        assert Direction.UPRIGHT.x == -1
        assert Direction.UPRIGHT.y == 1
        assert Direction.UPRIGHT.value == (-1, 1)

    def test_direction_downleft(self):
        """Test DOWNLEFT direction."""
        assert Direction.DOWNLEFT.x == 1
        assert Direction.DOWNLEFT.y == -1
        assert Direction.DOWNLEFT.value == (1, -1)

    def test_direction_downright(self):
        """Test DOWNRIGHT direction."""
        assert Direction.DOWNRIGHT.x == 1
        assert Direction.DOWNRIGHT.y == 1
        assert Direction.DOWNRIGHT.value == (1, 1)

    def test_all_directions_accessible(self):
        """Test that all directions are accessible."""
        directions = [
            Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT,
            Direction.UPLEFT, Direction.UPRIGHT, Direction.DOWNLEFT, Direction.DOWNRIGHT
        ]
        assert len(directions) == 8

    def test_direction_by_name(self):
        """Test accessing Direction by name."""
        assert Direction["UP"] == Direction.UP
        assert Direction["RIGHT"] == Direction.RIGHT
        assert Direction["DOWNRIGHT"] == Direction.DOWNRIGHT

    def test_x_property(self):
        """Test x property for various directions."""
        assert Direction.UP.x == -1
        assert Direction.DOWN.x == 1
        assert Direction.LEFT.x == 0
        assert Direction.RIGHT.x == 0

    def test_y_property(self):
        """Test y property for various directions."""
        assert Direction.UP.y == 0
        assert Direction.DOWN.y == 0
        assert Direction.LEFT.y == -1
        assert Direction.RIGHT.y == 1
