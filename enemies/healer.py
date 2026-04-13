"""Healer enemy - support unit that heals nearby enemies."""

import pygame

from enemies.base import Enemy
from src.point import Point


class Healer(Enemy):
    """Support enemy that heals nearby enemies — moderate HP, slow speed, high bounty.

    Heals all enemies within 60 pixels by 15 HP every 2 seconds.
    """

    BASE_HP = 80.0
    BASE_SPEED = 1.5
    BASE_BOUNTY = 25
    HEAL_RADIUS = 60  # pixels
    HEAL_AMOUNT = 15
    HEAL_INTERVAL = 2000  # milliseconds

    def __init__(self,
                 pos: Point,
                 life_point: float = BASE_HP,
                 speed: float = BASE_SPEED,
                 level: int = 1,
                 bounty: int = BASE_BOUNTY):

        self.id = Enemy.get_next_uuid()
        size = (16, 16)
        self.pos = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self.previous_pos = 0
        self.life_point = life_point
        self.max_life_point = life_point
        self.speed = speed
        self.level = level
        self.size = size
        self.color = (144, 238, 144)  # light green
        self.bounty = bounty
        self.heal_timer = 0

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
            pygame.draw.rect(win, (0, 255, 100), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(win, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def draw(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w, h = self.size[0], self.size[1]

        self._draw_health_bar(win)

        # Green body
        body_rect = pygame.Rect(x + 2, y + 3, w - 4, h - 3)
        pygame.draw.rect(win, (144, 238, 144), body_rect)
        pygame.draw.rect(win, (50, 150, 50), body_rect, 2)

        # White cross (healing symbol)
        cx = x + w // 2
        cy = y + h // 2
        # Horizontal bar
        pygame.draw.line(win, (255, 255, 255), (cx - 4, cy), (cx + 4, cy), 2)
        # Vertical bar
        pygame.draw.line(win, (255, 255, 255), (cx, cy - 4), (cx, cy + 4), 2)

        # Pulsing aura (circle) - indicates healing radius
        pygame.draw.circle(win, (100, 200, 100), (cx, cy), 8, 1)
