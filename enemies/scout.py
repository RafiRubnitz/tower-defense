"""Scout enemy - fast lightweight unit."""

import pygame

from enemies.base import Enemy
from src.point import Point


class Scout(Enemy):
    """Fast lightweight unit — low HP, high speed, moderate bounty."""

    BASE_HP = 50.0
    BASE_SPEED = 4.0
    BASE_BOUNTY = 20

    def __init__(self,
                 pos: Point,
                 life_point: float = BASE_HP,
                 speed: float = BASE_SPEED,
                 level: int = 1,
                 bounty: int = BASE_BOUNTY):

        self.id = Enemy.get_next_uuid()
        size = (14, 14)
        self.pos = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self.previous_pos = 0
        self.life_point = life_point
        self.max_life_point = life_point
        self.speed = speed
        self.level = level
        self.size = size
        self.color = (255, 165, 0)
        self.bounty = bounty

    def death(self):
        self.pos = pygame.Rect(0, 0, self.size[0], self.size[1])

    def _draw_health_bar(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w = self.size[0]
        bar_width = w + 4
        bar_height = 3
        bar_x = x - 2
        bar_y = y - 7
        pygame.draw.rect(win, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = max(0.0, self.life_point / self.max_life_point)
        health_width = int(bar_width * health_ratio)
        if health_width > 0:
            pygame.draw.rect(win, (255, 200, 0), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(win, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def draw(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w, h = self.size[0], self.size[1]

        self._draw_health_bar(win)

        # Diamond body shape
        cx, cy = x + w // 2, y + h // 2
        pygame.draw.polygon(win, (255, 165, 0), [
            (cx, y + 1),
            (x + w - 1, cy),
            (cx, y + h - 1),
            (x + 1, cy),
        ])
        pygame.draw.polygon(win, (200, 100, 0), [
            (cx, y + 1),
            (x + w - 1, cy),
            (cx, y + h - 1),
            (x + 1, cy),
        ], 2)
