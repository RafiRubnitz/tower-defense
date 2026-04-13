"""FreezeTower - slows enemies down, no damage."""

from typing import List

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower


class FreezeTower(Tower):
    """Slows enemies by 60% for 1.5 seconds: range 3.0, no damage, cooldown 2000 ms, cost $175."""

    tower_type = "Freeze"
    cost = 175
    SLOW_FACTOR = 0.4  # enemies move at 40% speed
    SLOW_DURATION = 1500  # milliseconds

    def __init__(self, pos: Point):
        self.size = (20, 20)
        self.pos = pygame.Rect(pos.y, pos.x, self.size[0], self.size[1])
        self.range = 3.0
        self.power = 0  # no damage
        self.level = 1
        self.color = (100, 200, 255)  # icy blue
        self.range_enable = False
        self.cool_down_time = 2000
        self.cool_down = 0

    def update(self, dt: int, enemies: List[Enemy], bullets: List = None, *args, **kwargs):
        self.mouse_functionality()
        self.cool_down -= dt
        if self.cool_down <= 0:
            range_sq = (self.range * 20) ** 2
            for enemy in enemies:
                if self._distance_squared(enemy) <= range_sq:
                    self.shot(enemy, bullets)
                    self.cool_down = self.cool_down_time
                    break

    def shot(self, target: Enemy, bullets: List = None, *args, **kwargs):
        """Apply slow effect to target enemy."""
        target.slow_factor = self.SLOW_FACTOR
        target.slow_timer = self.SLOW_DURATION

    def draw(self, win: pygame.Surface):
        cx = self.pos.x + (self.size[0] // 2)
        cy = self.pos.y + (self.size[1] // 2)

        # Icy blue base
        base_rect = pygame.Rect(self.pos.x + 2, self.pos.y + 2, self.size[0] - 4, self.size[1] - 4)
        pygame.draw.rect(win, (50, 150, 200), base_rect)
        pygame.draw.rect(win, (100, 200, 255), base_rect, 2)

        # Turret
        pygame.draw.circle(win, (100, 200, 255), (cx, cy), 6)
        pygame.draw.circle(win, (50, 150, 200), (cx, cy), 6, 2)

        # Snowflake-style barrel (two perpendicular lines)
        pygame.draw.line(win, (150, 220, 255), (cx - 5, cy), (cx + 5, cy), 2)
        pygame.draw.line(win, (150, 220, 255), (cx, cy - 5), (cx, cy + 5), 2)

        # Ice particle dots
        for offset in [(-5, -5), (5, -5), (-5, 5), (5, 5)]:
            px = cx + offset[0]
            py = cy + offset[1]
            pygame.draw.circle(win, (150, 220, 255), (px, py), 1)

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
