"""Base Tower class with shared functionality."""

from typing import Tuple, List

import pygame

from enemies import Enemy
from src.point import Point


class Tower(object):
    range: float
    power: float
    cool_down_time: int
    level: int
    pos: pygame.Rect
    size: Tuple[int, int]
    color: Tuple[int, int, int]
    range_enable: bool
    cool_down: int
    tower_type: str = "Basic"
    cost: int = 100

    def draw(self, win: pygame.Surface):
        ...

    def update(self, dt: int, enemies: List[Enemy], *args, **kwargs):
        ...

    def handle_event(self, event: pygame.event.Event):
        ...

    def find_enemy(self):
        ...

    def shot(self, target: Point):
        ...

    def upgrade(self, *args, **kwargs):
        ...

    def mouse_functionality(self) -> None:
        ...

    def _distance_squared(self, enemy: Enemy) -> float:
        tcx = self.pos.x + (self.size[0] // 2)
        tcy = self.pos.y + (self.size[1] // 2)
        ecx = enemy.pos.x + (enemy.size[0] // 2)
        ecy = enemy.pos.y + (enemy.size[1] // 2)
        return (ecx - tcx) ** 2 + (ecy - tcy) ** 2

    def _draw_range_circle(self, win: pygame.Surface):
        if self.range_enable:
            cx = self.pos.x + (self.size[0] // 2)
            cy = self.pos.y + (self.size[1] // 2)
            r = int(self.range * 20)
            surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (0, 255, 0, 40), (r, r), r)
            pygame.draw.circle(surface, (0, 255, 0, 100), (r, r), r, 1)
            win.blit(surface, (cx - r, cy - r))
