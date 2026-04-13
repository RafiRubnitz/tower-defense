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

    def __init__(self,
                 pos: Point,
                 life_point: float = 100,
                 speed: float = 2.0,
                 level: int = 1,
                 size: Tuple[int, int] = (20, 20),
                 color: Tuple[int, int, int] = (220, 20, 60),  # Crimson red for enemies
                 bounty: int = 15):

        self.id = Enemy.get_next_uuid()
        self.pos = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self.previous_pos = 0
        self.life_point = life_point
        self.speed = speed
        self.level = level
        self.size = size
        self.color = color
        self.bounty = bounty
        # Soldier colors
        self.uniform_color = (220, 20, 60)  # Crimson
        self.helmet_color = (50, 50, 50)  # Dark gray helmet
        self.skin_color = (255, 200, 150)  # Skin tone

    def update(self, direction: Direction, *args, **kwargs):
        self.move(direction)
        if self.life_point <= 0:
            self.death()

    def move(self, direction: Direction):

        self.pos.x += self.speed * direction.x
        self.pos.y += self.speed * direction.y

    def death(self):
        self.pos = pygame.Rect(0, 0, self.size[0], self.size[1])

    def draw(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w, h = self.size[0], self.size[1]

        # Draw health bar background (red)
        bar_width = w + 4
        bar_height = 4
        bar_x = x - 2
        bar_y = y - 8
        pygame.draw.rect(win, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Draw current health (green)
        health_ratio = self.life_point / (100 * self.level)  # Base HP is 100 * level
        health_width = int(bar_width * health_ratio)
        if health_width > 0:
            pygame.draw.rect(win, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

        # Draw health bar border
        pygame.draw.rect(win, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

        # Draw soldier body (uniform)
        body_rect = pygame.Rect(x + 4, y + 8, w - 8, h - 8)
        pygame.draw.rect(win, self.uniform_color, body_rect)
        pygame.draw.rect(win, (0, 0, 0), body_rect, 2)

        # Draw helmet (circle on top)
        helmet_center = (x + w // 2, y + 6)
        pygame.draw.circle(win, self.helmet_color, helmet_center, 6)
        pygame.draw.circle(win, (0, 0, 0), helmet_center, 6, 2)

        # Draw small face detail
        face_y = y + 5
        pygame.draw.circle(win, self.skin_color, (x + w // 2, face_y), 3)





