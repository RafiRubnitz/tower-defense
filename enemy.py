from typing import Tuple

import pygame

from src.direction import Direction
from src.point import Point


class Enemy(object):

    _UUID: int = 0

    id: int
    life_point: float
    speed: int
    level: int
    size: Tuple[int, int]
    color: Tuple[int, int, int]
    pos: pygame.Rect
    previous_pos: int

    @classmethod
    def get_next_uuid(cls) -> int:
        cls._UUID += 1
        return cls._UUID

    def update(self, *args, **kwargs):
        ...

    def draw(self, win: pygame.Surface):
        ...

    def move(self, direction: Direction):
        ...

    def hit(self):
        ...

    def death(self):
        ...


class Soldier(Enemy):
    """Basic infantry unit — balanced stats."""

    BASE_HP = 150.0  # Increased from 100
    BASE_SPEED = 2.5  # Increased from 2.0
    BASE_BOUNTY = 14  # Reduced by 10% from 15

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

        # Retro style soldier - body with helmet
        body_rect = pygame.Rect(x + 1, y + 6, w - 2, h - 8)
        pygame.draw.rect(win, (220, 20, 60), body_rect)  # Uniform color

        # Helmet on top
        helmet_rect = pygame.Rect(x + 2, y + 1, w - 4, 5)
        pygame.draw.rect(win, (80, 80, 80), helmet_rect)

        # Black outline
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(x, y, w, h), 1)


class Tank(Enemy):
    """Heavy armored unit — high HP, slow speed, high bounty."""

    BASE_HP = 450.0  # Increased 50% from 300
    BASE_SPEED = 1.25  # Increased 25% from 1.0
    BASE_BOUNTY = 27  # Reduced by 10% from 30

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

        # Heavy tank - thick armor
        armor_rect = pygame.Rect(x + 1, y + 1, w - 2, h - 2)
        pygame.draw.rect(win, (80, 120, 80), armor_rect)  # Dark green armor
        # Turret
        turret_rect = pygame.Rect(x + 5, y + 4, 12, 12)
        pygame.draw.rect(win, (100, 150, 100), turret_rect)
        # Black outline
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(x, y, w, h), 2)


class Scout(Enemy):
    """Fast lightweight unit — low HP, high speed, moderate bounty."""

    BASE_HP = 75.0  # Increased 50% from 50
    BASE_SPEED = 5.0  # Increased 25% from 4.0
    BASE_BOUNTY = 18  # Reduced by 10% from 20

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

        # Fast scout - small and nimble
        body_rect = pygame.Rect(x + 1, y + 2, w - 2, h - 4)
        pygame.draw.rect(win, (255, 165, 0), body_rect)  # Orange
        # Head marker
        head_rect = pygame.Rect(x + 3, y + 1, w - 6, 2)
        pygame.draw.rect(win, (255, 200, 0), head_rect)
        # Black outline
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(x, y, w, h), 1)


class Boss(Enemy):
    """End-of-wave boss — very high HP, slow speed, huge bounty.

    Visual: large dark red unit with crown indicator.
    """

    BASE_HP = 1500.0  # Increased 50% from 1000
    BASE_SPEED = 1.0  # Increased 25% from 0.8
    BASE_BOUNTY = 90  # Reduced by 10% from 100

    def __init__(self,
                 pos: Point,
                 life_point: float = BASE_HP,
                 speed: float = BASE_SPEED,
                 level: int = 1,
                 bounty: int = BASE_BOUNTY):

        self.id = Enemy.get_next_uuid()
        size = (28, 28)
        self.pos = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self.previous_pos = 0
        self.life_point = life_point
        self.max_life_point = life_point
        self.speed = speed
        self.level = level
        self.size = size
        self.color = (139, 0, 0)
        self.bounty = bounty

    def death(self):
        self.pos = pygame.Rect(0, 0, self.size[0], self.size[1])

    def _draw_health_bar(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w = self.size[0]
        bar_width = w + 6
        bar_height = 6
        bar_x = x - 3
        bar_y = y - 12
        pygame.draw.rect(win, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_ratio = max(0.0, self.life_point / self.max_life_point)
        health_width = int(bar_width * health_ratio)
        if health_width > 0:
            pygame.draw.rect(win, (255, 50, 50), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(win, (255, 215, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def draw(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w, h = self.size[0], self.size[1]

        self._draw_health_bar(win)

        # Simple retro style - filled square with black outline
        enemy_rect = pygame.Rect(x + 1, y + 1, w - 2, h - 2)
        pygame.draw.rect(win, (200, 50, 50), enemy_rect)
        pygame.draw.rect(win, (0, 0, 0), enemy_rect, 1)
