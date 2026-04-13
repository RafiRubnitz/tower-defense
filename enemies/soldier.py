"""Soldier enemy - basic infantry unit."""

from typing import Tuple

import pygame

from src.direction import Direction
from src.point import Point
from enemies.base import Enemy


class Soldier(Enemy):
    """Basic infantry unit — balanced stats."""

    BASE_HP = 100.0
    BASE_SPEED = 2.0
    BASE_BOUNTY = 15

    def __init__(self,
                 pos: Point,
                 life_point: float = BASE_HP,
                 speed: float = BASE_SPEED,
                 level: int = 1,
                 size: Tuple[int, int] = (18, 18),
                 color: Tuple[int, int, int] = (220, 20, 60),
                 bounty: int = BASE_BOUNTY):

        self.id = Enemy.get_next_uuid()
        self.pos = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self.previous_pos = 0
        self.life_point = life_point
        self.max_life_point = life_point
        self.speed = speed
        self.level = level
        self.size = size
        self.color = color
        self.bounty = bounty
        self.uniform_color = (220, 20, 60)
        self.helmet_color = (50, 50, 50)
        self.skin_color = (255, 200, 150)

    def update(self, direction: Direction, *args, **kwargs):
        self.move(direction)
        if self.life_point <= 0:
            self.death()

    def move(self, direction: Direction):
        self.pos.x += self.speed * direction.x
        self.pos.y += self.speed * direction.y

    def death(self):
        self.pos = pygame.Rect(0, 0, self.size[0], self.size[1])

    def _draw_health_bar(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w = self.size[0]
        bar_width = w + 4
        bar_height = 4
        bar_x = x - 2
        bar_y = y - 8
        pygame.draw.rect(win, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = max(0.0, self.life_point / self.max_life_point)
        health_width = int(bar_width * health_ratio)
        if health_width > 0:
            pygame.draw.rect(win, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(win, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def draw(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w, h = self.size[0], self.size[1]

        self._draw_health_bar(win)

        # Body
        body_rect = pygame.Rect(x + 3, y + 7, w - 6, h - 7)
        pygame.draw.rect(win, self.uniform_color, body_rect)
        pygame.draw.rect(win, (0, 0, 0), body_rect, 2)

        # Helmet
        helmet_center = (x + w // 2, y + 5)
        pygame.draw.circle(win, self.helmet_color, helmet_center, 5)
        pygame.draw.circle(win, (0, 0, 0), helmet_center, 5, 2)

        # Face
        pygame.draw.circle(win, self.skin_color, (x + w // 2, y + 4), 3)
