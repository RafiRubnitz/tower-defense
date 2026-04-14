"""MachineGunTower - short range, low damage, very fast fire."""

from typing import List

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower, get_bullet_class


class MachineGunTower(Tower):
    """Short range, low damage, very fast fire: range 3, damage 15, cooldown 100 ms, cost $150."""

    tower_type = "MachineGun"
    cost = 180
    shape_style = "rectangle"

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
        # Retro pixel-art style - simple outlined square with magenta border
        tower_rect = pygame.Rect(self.pos.x + 1, self.pos.y + 1, self.size[0] - 2, self.size[1] - 2)

        # Bright green fill for machine gun
        pygame.draw.rect(win, (150, 220, 100), tower_rect)
        # Magenta/pink border
        pygame.draw.rect(win, (255, 0, 255), tower_rect, 2)

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
