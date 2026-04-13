"""Bullet class for tower projectiles."""

from typing import Tuple

import pygame

from enemies import Enemy


class Bullet:
    def __init__(self, start_x: int, start_y: int, target: Enemy, damage: float, color: Tuple[int, int, int] = (0, 0, 0)):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.target = target
        self.damage = damage
        self.color = color
        self.speed = 10
        self.active = True

    def update(self) -> bool:
        """Update bullet position. Returns True if bullet hit target."""
        if not self.target or not self.active:
            return False

        target_x = self.target.pos.x + (self.target.size[0] // 2)
        target_y = self.target.pos.y + (self.target.size[1] // 2)

        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance < self.speed:
            self.x = target_x
            self.y = target_y
            self.active = False
            return True

        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        return False

    def draw(self, win: pygame.Surface):
        if self.active:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 4)
