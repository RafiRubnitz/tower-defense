"""SniperTower - long range, high damage, slow fire."""

from typing import List

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower, get_bullet_class


class SniperTower(Tower):
    """Long range, high damage, slow cooldown: range 8, damage 200, cooldown 2000 ms, cost $200."""

    tower_type = "Sniper"
    cost = 200
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
        cx = self.pos.x + (self.size[0] // 2)
        cy = self.pos.y + (self.size[1] // 2)

        # Dark base
        base_rect = pygame.Rect(self.pos.x + 3, self.pos.y + 3, self.size[0] - 6, self.size[1] - 6)
        pygame.draw.rect(win, (60, 30, 30), base_rect)
        pygame.draw.rect(win, (120, 40, 40), base_rect, 2)

        # Turret
        pygame.draw.circle(win, (180, 50, 50), (cx, cy), 5)
        pygame.draw.circle(win, (120, 20, 20), (cx, cy), 5, 2)

        # Long barrel
        pygame.draw.line(win, (100, 30, 30), (cx, cy), (cx, cy - 11), 2)

        # Level indicator dot
        pygame.draw.circle(win, (255, 100, 100), (self.pos.x + 3, self.pos.y + 3), 2)

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
