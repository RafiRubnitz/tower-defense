"""Tests for Point class."""
import pytest
from src.point import Point


class TestPoint:
    """Tests for Point class."""

    def test_point_creation(self):
        """Test Point creation."""
        p = Point(5, 10)
        assert p.x == 5
        assert p.y == 10

    def test_point_zero(self):
        """Test Point at origin."""
        p = Point(0, 0)
        assert p.x == 0
        assert p.y == 0

    def test_point_negative_coords(self):
        """Test Point with negative coordinates."""
        p = Point(-5, -10)
        assert p.x == -5
        assert p.y == -10

    def test_point_repr(self):
        """Test Point string representation."""
        p = Point(3, 4)
        assert repr(p) == "Point(3, 4)"

    def test_point_repr_negative(self):
        """Test Point repr with negative coordinates."""
        p = Point(-1, -2)
        assert repr(p) == "Point(-1, -2)"

    def test_point_equality(self):
        """Test Point equality comparison."""
        p1 = Point(5, 10)
        p2 = Point(5, 10)
        assert p1 == p2

    def test_point_inequality(self):
        """Test Point inequality."""
        p1 = Point(5, 10)
        p2 = Point(5, 11)
        assert not (p1 == p2)

    def test_point_inequality_different_x(self):
        """Test Point inequality with different x."""
        p1 = Point(5, 10)
        p2 = Point(6, 10)
        assert not (p1 == p2)

    def test_point_iadd_tuple(self):
        """Test Point in-place addition with tuple."""
        p = Point(5, 10)
        p += (3, 2)
        assert p.x == 8
        assert p.y == 12

    def test_point_iadd_negative(self):
        """Test Point in-place addition with negative tuple."""
        p = Point(5, 10)
        p += (-2, -3)
        assert p.x == 3
        assert p.y == 7

    def test_point_iadd_zero(self):
        """Test Point in-place addition with zero."""
        p = Point(5, 10)
        p += (0, 0)
        assert p.x == 5
        assert p.y == 10

    def test_point_iadd_returns_self(self):
        """Test that iadd returns self."""
        p = Point(5, 10)
        p += (1, 2)
        assert p.x == 6
        assert p.y == 12

    def test_multiple_iadd_operations(self):
        """Test multiple iadd operations."""
        p = Point(0, 0)
        p += (1, 1)
        assert p == Point(1, 1)
        p += (2, 3)
        assert p == Point(3, 4)
        p += (-1, -2)
        assert p == Point(2, 2)

    def test_point_large_coords(self):
        """Test Point with large coordinates."""
        p = Point(999999, 888888)
        assert p.x == 999999
        assert p.y == 888888

    def test_point_comparison_with_equal_coords(self):
        """Test multiple equal points."""
        p1 = Point(10, 20)
        p2 = Point(10, 20)
        p3 = Point(10, 20)
        assert p1 == p2 == p3
