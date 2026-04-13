"""Tank enemy - heavy armored unit."""

from typing import Tuple

import pygame

from src.point import Point
from enemies.base import Enemy


class Tank(Enemy):
    """Heavy armored unit — high HP, slow speed, high bounty."""

    BASE_HP = 300.0
    BASE_SPEED = 1.0
    BASE_BOUNTY = 30

    def __init__(self,
                 pos: Point,
                 life_point: float = BASE_HP,
                 speed: float = BASE_SPEED,
                 level: int = 1,
                 bounty: int = BASE_BOUNTY):

        self.id = Enemy.get_next_uuid()
        size = (22, 22)
        self.pos = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self.previous_pos = 0
        self.life_point = life_point
        self.max_life_point = life_point
        self.speed = speed
        self.level = level
        self.size = size
        self.color = (60, 80, 60)
        self.bounty = bounty

    def death(self):
        self.pos = pygame.Rect(0, 0, self.size[0], self.size[1])

    def _draw_health_bar(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w = self.size[0]
        bar_width = w + 4
        bar_height = 5
        bar_x = x - 2
        bar_y = y - 9
        pygame.draw.rect(win, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = max(0.0, self.life_point / self.max_life_point)
        health_width = int(bar_width * health_ratio)
        if health_width > 0:
            pygame.draw.rect(win, (0, 200, 100), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(win, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def draw(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w, h = self.size[0], self.size[1]

        self._draw_health_bar(win)

        # Tank body (dark green)
        body_rect = pygame.Rect(x + 1, y + 4, w - 2, h - 4)
        pygame.draw.rect(win, (60, 80, 60), body_rect)
        pygame.draw.rect(win, (20, 40, 20), body_rect, 2)

        # Tracks (dark stripes on sides)
        pygame.draw.rect(win, (30, 30, 30), pygame.Rect(x, y + 6, 4, h - 8))
        pygame.draw.rect(win, (30, 30, 30), pygame.Rect(x + w - 4, y + 6, 4, h - 8))

        # Turret (circle)
        turret_center = (x + w // 2, y + h // 2)
        pygame.draw.circle(win, (80, 100, 80), turret_center, 6)
        pygame.draw.circle(win, (20, 40, 20), turret_center, 6, 2)

        # Cannon barrel
        pygame.draw.rect(win, (20, 40, 20), pygame.Rect(x + w // 2 - 1, y + 2, 3, 8))
