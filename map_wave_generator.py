"""Auto-generate waves for custom maps."""
from typing import Dict, List

from map import calculate_wave_enemy_count, calculate_wave_enemy_hp


class WaveGenerator:
    """Generate and save wave configurations for custom maps."""

    def __init__(self):
        pass

    def generate_for_map(
        self,
        db,
        map_id: int,
        map_name: str,
        difficulty: int = 1,
        total_waves: int = 5,
    ) -> int:
        """Auto-generate wave configs for a custom map and save to DB.

        Args:
            db: Database instance
            map_id: ID of the map
            map_name: Name of the map
            difficulty: Difficulty level (1-5)
            total_waves: Number of waves to generate (default 5)

        Returns:
            round_config_id: ID of the created round config
        """
        # Create round config
        difficulty_multiplier = 1.0 + (difficulty - 1) * 0.15
        round_config_id = db.save_round_config(
            name=f"{map_name} Config",
            map_id=map_id,
            total_waves=total_waves,
            starting_money=450,
            starting_lives=10,
            tower_cost=100,
            difficulty_multiplier=difficulty_multiplier,
        )

        # Generate wave configs
        for wave_num in range(1, total_waves + 1):
            total_enemies = calculate_wave_enemy_count(wave_num, base_count=6)
            enemy_composition = self._get_enemy_composition(wave_num, total_enemies)
            spawn_interval = max(30, 120 - wave_num * 15)  # Faster spawns in later waves

            db.save_wave_config(
                round_config_id=round_config_id,
                wave_number=wave_num,
                total_enemies=total_enemies,
                spawn_interval=spawn_interval,
                enemy_composition=enemy_composition,
            )

        return round_config_id

    def _get_enemy_composition(self, wave_number: int, total_enemies: int) -> Dict[str, int]:
        """Determine enemy composition by wave.

        Wave 1-2: Soldiers only
        Wave 3-4: Mix Soldiers + Tanks
        Wave 5+: Mix all types
        """
        if wave_number <= 2:
            return {"Soldier": total_enemies}

        if wave_number <= 4:
            soldier_count = int(total_enemies * 0.7)
            tank_count = total_enemies - soldier_count
            return {"Soldier": soldier_count, "Tank": tank_count}

        # Wave 5+: All types
        soldier_count = int(total_enemies * 0.5)
        tank_count = int(total_enemies * 0.25)
        scout_count = int(total_enemies * 0.2)
        boss_count = max(1, total_enemies - soldier_count - tank_count - scout_count)

        return {
            "Soldier": soldier_count,
            "Tank": tank_count,
            "Scout": scout_count,
            "Boss": boss_count,
        }
