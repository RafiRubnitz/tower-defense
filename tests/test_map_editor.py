"""Tests for map editor feature."""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from map_wave_generator import WaveGenerator


class TestWaveGenerator:
    """Tests for wave generation."""

    def test_wave_generator_creates_round_config(self):
        """Test that wave generator creates a round config."""
        gen = WaveGenerator()
        mock_db = Mock()
        mock_db.save_round_config.return_value = 42

        gen.generate_for_map(
            db=mock_db,
            map_id=1,
            map_name="Test Map",
            difficulty=1,
            total_waves=5,
        )

        mock_db.save_round_config.assert_called_once()
        assert mock_db.save_round_config.call_args[1]["map_id"] == 1
        assert mock_db.save_round_config.call_args[1]["total_waves"] == 5

    def test_wave_generator_creates_wave_configs(self):
        """Test that wave generator creates correct number of wave configs."""
        gen = WaveGenerator()
        mock_db = Mock()
        mock_db.save_round_config.return_value = 42

        gen.generate_for_map(
            db=mock_db,
            map_id=1,
            map_name="Test Map",
            difficulty=1,
            total_waves=5,
        )

        # Should call save_wave_config 5 times
        assert mock_db.save_wave_config.call_count == 5

    def test_wave_generator_returns_round_config_id(self):
        """Test that generate_for_map returns round config ID."""
        gen = WaveGenerator()
        mock_db = Mock()
        mock_db.save_round_config.return_value = 99

        result = gen.generate_for_map(
            db=mock_db,
            map_id=1,
            map_name="Test Map",
            difficulty=1,
            total_waves=5,
        )

        assert result == 99

    def test_wave_composition_soldiers_only_wave_1(self):
        """Test wave 1 has soldiers only."""
        gen = WaveGenerator()
        composition = gen._get_enemy_composition(wave_number=1, total_enemies=10)

        assert "Soldier" in composition
        assert composition["Soldier"] == 10
        assert len(composition) == 1

    def test_wave_composition_soldiers_only_wave_2(self):
        """Test wave 2 has soldiers only."""
        gen = WaveGenerator()
        composition = gen._get_enemy_composition(wave_number=2, total_enemies=10)

        assert "Soldier" in composition
        assert composition["Soldier"] == 10
        assert len(composition) == 1

    def test_wave_composition_mixed_wave_3(self):
        """Test wave 3 has soldiers and tanks."""
        gen = WaveGenerator()
        composition = gen._get_enemy_composition(wave_number=3, total_enemies=10)

        assert "Soldier" in composition
        assert "Tank" in composition
        assert composition["Soldier"] + composition["Tank"] == 10
        # 70% soldiers, 30% tanks
        assert composition["Soldier"] == 7
        assert composition["Tank"] == 3

    def test_wave_composition_mixed_wave_4(self):
        """Test wave 4 has soldiers and tanks."""
        gen = WaveGenerator()
        composition = gen._get_enemy_composition(wave_number=4, total_enemies=10)

        assert "Soldier" in composition
        assert "Tank" in composition
        total = composition["Soldier"] + composition["Tank"]
        assert total == 10

    def test_wave_composition_all_types_wave_5(self):
        """Test wave 5 has all enemy types."""
        gen = WaveGenerator()
        composition = gen._get_enemy_composition(wave_number=5, total_enemies=20)

        assert "Soldier" in composition
        assert "Tank" in composition
        assert "Scout" in composition
        assert "Boss" in composition
        total = sum(composition.values())
        assert total == 20

    def test_wave_composition_scaling(self):
        """Test that later waves have more varied enemy composition."""
        gen = WaveGenerator()

        wave_1_comp = gen._get_enemy_composition(1, 6)
        wave_5_comp = gen._get_enemy_composition(5, 20)

        # Wave 1 has only soldiers
        assert len(wave_1_comp) == 1

        # Wave 5 has multiple types
        assert len(wave_5_comp) > 1


class TestMapEditorGeometry:
    """Tests for map editor geometry functions."""

    def test_is_adjacent_right(self):
        """Test adjacency check - right neighbor."""
        from ui.map_editor import MapEditorScreen
        # Create a mock MapEditorScreen just to test the method
        mock_game = Mock()
        mock_db = Mock()
        editor = MapEditorScreen.__new__(MapEditorScreen)

        assert editor._is_adjacent((0, 0), (1, 0))

    def test_is_adjacent_left(self):
        """Test adjacency check - left neighbor."""
        from ui.map_editor import MapEditorScreen
        mock_game = Mock()
        mock_db = Mock()
        editor = MapEditorScreen.__new__(MapEditorScreen)

        assert editor._is_adjacent((1, 0), (0, 0))

    def test_is_adjacent_down(self):
        """Test adjacency check - down neighbor."""
        from ui.map_editor import MapEditorScreen
        editor = MapEditorScreen.__new__(MapEditorScreen)

        assert editor._is_adjacent((0, 0), (0, 1))

    def test_is_adjacent_up(self):
        """Test adjacency check - up neighbor."""
        from ui.map_editor import MapEditorScreen
        editor = MapEditorScreen.__new__(MapEditorScreen)

        assert editor._is_adjacent((0, 1), (0, 0))

    def test_is_not_adjacent_diagonal(self):
        """Test non-adjacency check - diagonal."""
        from ui.map_editor import MapEditorScreen
        editor = MapEditorScreen.__new__(MapEditorScreen)

        assert not editor._is_adjacent((0, 0), (1, 1))

    def test_is_not_adjacent_far(self):
        """Test non-adjacency check - far away."""
        from ui.map_editor import MapEditorScreen
        editor = MapEditorScreen.__new__(MapEditorScreen)

        assert not editor._is_adjacent((0, 0), (5, 5))


class TestMapEditorValidation:
    """Tests for map editor validation."""

    def test_validate_path_too_short(self):
        """Test validation fails for path < 5 cells."""
        from ui.map_editor import MapEditorScreen

        editor = MapEditorScreen.__new__(MapEditorScreen)
        editor.path = [(0, 0), (1, 0), (2, 0)]

        valid, msg = editor._validate_path()
        assert not valid
        assert "too short" in msg.lower()

    def test_validate_path_min_length(self):
        """Test validation passes for path with 5 cells."""
        from ui.map_editor import MapEditorScreen

        editor = MapEditorScreen.__new__(MapEditorScreen)
        editor.path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]

        valid, msg = editor._validate_path()
        assert valid

    def test_validate_path_normal_length(self):
        """Test validation passes for longer path."""
        from ui.map_editor import MapEditorScreen

        editor = MapEditorScreen.__new__(MapEditorScreen)
        editor.path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)]

        valid, msg = editor._validate_path()
        assert valid

    def test_validate_path_has_gaps(self):
        """Test validation fails if path has gaps."""
        from ui.map_editor import MapEditorScreen

        editor = MapEditorScreen.__new__(MapEditorScreen)
        # Create path with a gap (not all consecutive pairs are adjacent)
        editor.path = [(0, 0), (1, 0), (3, 0), (3, 1), (3, 2)]  # Gap at (1,0) to (3,0)

        valid, msg = editor._validate_path()
        assert not valid
        assert "gaps" in msg.lower()


class TestDatabaseIntegration:
    """Tests for database integration."""

    def test_save_map_creates_entry(self):
        """Test that save_map creates DB entry."""
        # This test would need a real database or extensive mocking
        # For now we'll just verify the structure
        from database import Database

        db = Database(":memory:")  # Use in-memory DB for testing

        map_id = db.save_map(
            name="Test Map",
            path=[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
            obstacles=[],
            width=40,
            height=30,
            is_builtin=False,
            difficulty=1,
        )

        assert isinstance(map_id, int)
        assert map_id > 0

    def test_save_map_and_retrieve(self):
        """Test that saved map can be retrieved."""
        from database import Database

        db = Database(":memory:")

        path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        map_id = db.save_map(
            name="Test Map",
            path=path,
            obstacles=[],
            width=40,
            height=30,
            is_builtin=False,
            difficulty=1,
        )

        retrieved = db.get_map(map_id)

        assert retrieved is not None
        assert retrieved["name"] == "Test Map"
        # Path is stored as JSON and returned as list of lists
        assert retrieved["path"] == [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        assert retrieved["difficulty"] == 1

    def test_save_map_duplicate_name_updates(self):
        """Test that saving map with duplicate name updates the existing map."""
        from database import Database

        db = Database(":memory:")

        map_id1 = db.save_map(
            name="Test Map",
            path=[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
            obstacles=[],
            width=40,
            height=30,
            is_builtin=False,
            difficulty=1,
        )

        # Save again with same name - should update, not create new
        map_id2 = db.save_map(
            name="Test Map",
            path=[(0, 0), (1, 0), (5, 5)],  # Different path
            obstacles=[],
            width=40,
            height=30,
            is_builtin=False,
            difficulty=2,
        )

        # Should return same ID
        assert map_id1 == map_id2

        # Verify the map was updated
        retrieved = db.get_map(map_id1)
        assert retrieved["path"] == [[0, 0], [1, 0], [5, 5]]
        assert retrieved["difficulty"] == 2

    def test_wave_configs_saved_correctly(self):
        """Test that wave configs are saved correctly."""
        from database import Database

        db = Database(":memory:")

        # Create map
        map_id = db.save_map(
            name="Test Map",
            path=[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
            obstacles=[],
            width=40,
            height=30,
            is_builtin=False,
            difficulty=1,
        )

        # Create round config
        round_config_id = db.save_round_config(
            name="Test Config",
            map_id=map_id,
            total_waves=3,
            starting_money=450,
            starting_lives=10,
            tower_cost=100,
            difficulty_multiplier=1.0,
        )

        # Create wave configs
        db.save_wave_config(
            round_config_id=round_config_id,
            wave_number=1,
            total_enemies=6,
            spawn_interval=30,
            enemy_composition={"Soldier": 6},
        )

        # Retrieve and verify
        waves = db.get_wave_configs(round_config_id)
        assert len(waves) == 1
        assert waves[0]["wave_number"] == 1
        assert waves[0]["total_enemies"] == 6
        assert waves[0]["enemy_composition"]["Soldier"] == 6
