"""MachineGunTower - short range, low damage, very fast fire."""

from typing import List

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower, get_bullet_class


class MachineGunTower(Tower):
    """Short range, low damage, very fast fire: range 3, damage 15, cooldown 100 ms, cost $150."""

    tower_type = "MachineGun"
    cost = 150

    def __init__(self, pos: Point):
        self.size = (20, 20)
        self.pos = pygame.Rect(pos.y, pos.x, self.size[0], self.size[1])
        self.range = 3.0
        self.power = 15
        self.level = 1
        self.color = (50, 200, 50)
        self.range_enable = False
        self.cool_down_time = 100
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
            bullets.append(Bullet(cx, cy, target, self.power, self.color, speed=14))
        else:
            target.life_point -= self.power

    def draw(self, win: pygame.Surface):
        cx = self.pos.x + (self.size[0] // 2)
        cy = self.pos.y + (self.size[1] // 2)

        # Green base
        base_rect = pygame.Rect(self.pos.x + 2, self.pos.y + 2, self.size[0] - 4, self.size[1] - 4)
        pygame.draw.rect(win, (20, 80, 20), base_rect)
        pygame.draw.rect(win, (40, 160, 40), base_rect, 2)

        # Turret
        pygame.draw.circle(win, (50, 200, 50), (cx, cy), 5)
        pygame.draw.circle(win, (20, 100, 20), (cx, cy), 5, 2)

        # Triple barrel dots
        for offset in (-3, 0, 3):
            barrel_x = cx + offset
            pygame.draw.line(win, (20, 100, 20), (barrel_x, cy), (barrel_x, cy - 7), 2)

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
