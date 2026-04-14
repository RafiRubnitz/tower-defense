"""SniperTower - long range, high damage, slow fire."""

from typing import List

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower, get_bullet_class


class SniperTower(Tower):
    """Long range, high damage, slow cooldown: range 8, damage 200, cooldown 2000 ms, cost $200."""

    tower_type = "Sniper"
    cost = 240
    shape_style = "diamond"

    def __init__(self, pos: Point):
        self.size = (20, 20)
        self.pos = pygame.Rect(pos.y, pos.x, self.size[0], self.size[1])
        self.range = 8.0
        self.power = 200
        self.level = 1
        self.color = (180, 50, 50)
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
        if bullets is not None:
            Bullet = get_bullet_class()
            cx = self.pos.x + (self.size[0] // 2)
            cy = self.pos.y + (self.size[1] // 2)
            bullets.append(Bullet(cx, cy, target, self.power, self.color, speed=18))
        else:
            target.life_point -= self.power

    def draw(self, win: pygame.Surface):
        # Sniper tower - tall and slim for long range
        base_rect = pygame.Rect(self.pos.x + 7, self.pos.y + 5, 6, 15)
        pygame.draw.rect(win, (100, 100, 100), base_rect)  # Gray base

        # Scope turret
        scope_rect = pygame.Rect(self.pos.x + 4, self.pos.y + 2, 12, 8)
        pygame.draw.rect(win, (180, 50, 50), scope_rect)  # Red scope
        pygame.draw.rect(win, (255, 0, 255), scope_rect, 1)  # Magenta border

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
