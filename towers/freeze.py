"""FreezeTower - slows enemies down, no damage."""

from typing import List

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower


class FreezeTower(Tower):
    """Slows enemies by 60% for 1.5 seconds: range 3.0, no damage, cooldown 2000 ms, cost $175."""

    tower_type = "Freeze"
    cost = 210
    shape_style = "triangle"
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
        # Freeze tower - pointy pyramid shape
        center_x = self.pos.x + 10

        # Base
        base_rect = pygame.Rect(self.pos.x + 2, self.pos.y + 12, 16, 6)
        pygame.draw.rect(win, (100, 150, 200), base_rect)  # Dark blue

        # Pyramid point
        points = [
            (center_x, self.pos.y + 1),  # top
            (self.pos.x + 18, self.pos.y + 12),  # bottom right
            (self.pos.x + 2, self.pos.y + 12)   # bottom left
        ]
        pygame.draw.polygon(win, (150, 200, 255), points)  # Ice blue
        pygame.draw.polygon(win, (255, 0, 255), points, 1)  # Magenta border

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
