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


class Boss(Enemy):
    """End-of-wave boss — very high HP, slow speed, huge bounty.

    Visual: large dark red unit with crown indicator.
    """

    BASE_HP = 1000.0
    BASE_SPEED = 0.8
    BASE_BOUNTY = 100

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

        # Large dark red body
        body_rect = pygame.Rect(x + 2, y + 6, w - 4, h - 6)
        pygame.draw.rect(win, (139, 0, 0), body_rect)
        pygame.draw.rect(win, (80, 0, 0), body_rect, 2)

        # Crown spikes (gold)
        cx = x + w // 2
        crown_points = [
            (x + 3, y + 6),
            (x + 3, y + 1),
            (cx - 4, y + 5),
            (cx, y),
            (cx + 4, y + 5),
            (x + w - 3, y + 1),
            (x + w - 3, y + 6),
        ]
        pygame.draw.polygon(win, (255, 215, 0), crown_points)
        pygame.draw.polygon(win, (180, 150, 0), crown_points, 1)

        # Boss face detail
        eye_y = y + 12
        pygame.draw.circle(win, (255, 50, 50), (x + 9, eye_y), 3)
        pygame.draw.circle(win, (255, 50, 50), (x + w - 9, eye_y), 3)
        pygame.draw.circle(win, (0, 0, 0), (x + 9, eye_y), 1)
        pygame.draw.circle(win, (0, 0, 0), (x + w - 9, eye_y), 1)
