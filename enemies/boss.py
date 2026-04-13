"""Boss enemy - end of wave boss."""

import pygame

from enemies.base import Enemy
from src.point import Point


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
