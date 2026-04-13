"""Dynamic Difficulty Manager for Tower Defense.

Replaces the flat linear wave scaling with exponential growth curves
and optional player-performance adaptation.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class WaveConfig:
    """Computed parameters for a single wave."""
    wave_number: int
    total_enemies: int
    spawn_interval: int          # milliseconds between spawns
    enemy_hp_multiplier: float   # multiplier applied to base enemy HP
    enemy_speed_multiplier: float
    bounty_multiplier: float
    enemy_composition: Dict[str, int] = field(default_factory=dict)


class DifficultyManager:
    """Calculates wave difficulty using exponential scaling.

    Difficulty presets affect the overall multiplier:
      easy   -> 0.75
      normal -> 1.00
      hard   -> 1.40
    """

    DIFFICULTY_MULTIPLIERS = {
        'easy': 0.75,
        'normal': 1.00,
        'hard': 1.40,
    }

    # Exponential growth constants (tuned for ~10 waves)
    ENEMY_COUNT_BASE = 5
    ENEMY_COUNT_GROWTH = 1.25    # each wave: base * growth^(wave-1)
    HP_GROWTH = 1.18             # 18% more HP per wave
    SPEED_GROWTH = 0.08          # +8% speed per wave (additive %)
    BOUNTY_GROWTH = 1.10         # 10% more gold per wave
    SPAWN_INTERVAL_BASE = 1800   # ms (1.8 s between spawns at wave 1)
    SPAWN_INTERVAL_MIN = 400     # ms minimum gap
    SPAWN_INTERVAL_DECAY = 0.88  # multiplied each wave

    def __init__(self, difficulty: str = 'normal', total_waves: int = 10):
        self.difficulty = difficulty
        self.total_waves = total_waves
        self._perf_factor = 1.0   # adjusted live based on player performance
        self._diff_mult = self.DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_difficulty(self, difficulty: str):
        """Change difficulty preset at runtime (e.g. from settings screen)."""
        self.difficulty = difficulty
        self._diff_mult = self.DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)

    def get_wave_config(self, wave_number: int) -> WaveConfig:
        """Return fully computed WaveConfig for *wave_number* (1-indexed)."""
        w = max(1, wave_number)
        combined = self._diff_mult * self._perf_factor

        total_enemies = max(3, int(
            self.ENEMY_COUNT_BASE * (self.ENEMY_COUNT_GROWTH ** (w - 1)) * combined
        ))

        spawn_interval = max(
            self.SPAWN_INTERVAL_MIN,
            int(self.SPAWN_INTERVAL_BASE * (self.SPAWN_INTERVAL_DECAY ** (w - 1)))
        )

        hp_mult = (self.HP_GROWTH ** (w - 1)) * combined
        speed_mult = 1.0 + (w - 1) * self.SPEED_GROWTH * combined
        bounty_mult = self.BOUNTY_GROWTH ** (w - 1)

        composition = self._build_composition(w, total_enemies)

        return WaveConfig(
            wave_number=w,
            total_enemies=total_enemies,
            spawn_interval=spawn_interval,
            enemy_hp_multiplier=hp_mult,
            enemy_speed_multiplier=speed_mult,
            bounty_multiplier=bounty_mult,
            enemy_composition=composition,
        )

    def record_wave_result(self, lives_lost: int, enemies_escaped: int,
                           total_enemies: int):
        """Adapt difficulty based on player performance after a wave.

        If the player is barely surviving (many escapes) ease off a little.
        If the player takes no damage at all, increase pressure.
        """
        if total_enemies == 0:
            return

        escape_ratio = enemies_escaped / total_enemies

        if escape_ratio > 0.4:
            # Player struggling — reduce factor slightly (min 0.80)
            self._perf_factor = max(0.80, self._perf_factor * 0.95)
        elif escape_ratio == 0 and lives_lost == 0:
            # Player dominating — increase factor slightly (max 1.30)
            self._perf_factor = min(1.30, self._perf_factor * 1.05)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_composition(self, wave: int, total: int) -> Dict[str, int]:
        """Determine enemy mix for this wave."""
        comp: Dict[str, int] = {}

        if wave >= 5 and wave % 5 == 0:
            # Boss wave: one boss + remaining soldiers
            comp['boss'] = 1
            remaining = total - 1
        else:
            remaining = total

        if wave >= 3:
            tank_count = min(remaining // 4, max(0, wave - 2))
            comp['tank'] = tank_count
            remaining -= tank_count

        if wave >= 5:
            scout_count = min(remaining // 3, max(0, wave - 4))
            comp['scout'] = scout_count
            remaining -= scout_count

        comp['soldier'] = max(1, remaining)
        return comp
