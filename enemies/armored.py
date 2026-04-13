"""ArmoredSoldier enemy - unit with armor shield."""

import pygame

from enemies.base import Enemy
from src.point import Point


class ArmoredSoldier(Enemy):
    """Heavy infantry with armor shield — takes reduced damage.

    Has 150 HP + 80 armor. Armor absorbs damage first, then HP.
    Visual: dark grey body with blue shield ring (disappears when armor breaks).
    """

    BASE_HP = 150.0
    BASE_SPEED = 1.2
    BASE_BOUNTY = 35
    BASE_ARMOR = 80.0

    def __init__(self,
                 pos: Point,
                 life_point: float = BASE_HP,
                 speed: float = BASE_SPEED,
                 level: int = 1,
                 bounty: int = BASE_BOUNTY):

        self.id = Enemy.get_next_uuid()
        size = (20, 20)
        self.pos = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self.previous_pos = 0
        self.life_point = life_point
        self.max_life_point = life_point
        self.speed = speed
        self.level = level
        self.size = size
        self.color = (60, 60, 60)  # dark grey
        self.bounty = bounty
        self.armor_hp = self.BASE_ARMOR
        self.max_armor = self.BASE_ARMOR

    def take_damage(self, damage: float) -> None:
        """Apply damage to armor first, then health."""
        if self.armor_hp > 0:
            # Armor absorbs damage
            self.armor_hp -= damage
            if self.armor_hp < 0:
                # Overflow damage goes to health
                overflow = abs(self.armor_hp)
                self.armor_hp = 0
                self.life_point -= overflow
        else:
            # Armor is broken, full damage to health
            self.life_point -= damage

    def death(self):
        self.pos = pygame.Rect(0, 0, self.size[0], self.size[1])

    def _draw_health_bar(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w = self.size[0]
        bar_width = w + 4
        bar_height = 5
        bar_x = x - 2
        bar_y = y - 9

        # Background (red - damage taken)
        pygame.draw.rect(win, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Armor bar (blue)
        armor_ratio = max(0.0, self.armor_hp / self.max_armor)
        armor_width = int(bar_width * armor_ratio)
        if armor_width > 0:
            pygame.draw.rect(win, (0, 100, 255), (bar_x, bar_y, armor_width, bar_height))

        # Health bar (green) - shown after armor
        health_ratio = max(0.0, self.life_point / self.max_life_point)
        health_width = int(bar_width * health_ratio * (1 - armor_ratio))
        if health_width > 0:
            pygame.draw.rect(win, (0, 200, 100), (bar_x + armor_width, bar_y, health_width, bar_height))

        # Border
        pygame.draw.rect(win, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def draw(self, win: pygame.Surface):
        x, y = self.pos.x, self.pos.y
        w, h = self.size[0], self.size[1]

        self._draw_health_bar(win)

        # Dark grey body
        body_rect = pygame.Rect(x + 2, y + 4, w - 4, h - 4)
        pygame.draw.rect(win, (60, 60, 60), body_rect)
        pygame.draw.rect(win, (30, 30, 30), body_rect, 2)

        # Shield ring (blue) - only visible if armor is present
        if self.armor_hp > 0:
            cx = x + w // 2
            cy = y + h // 2
            pygame.draw.circle(win, (0, 100, 255), (cx, cy), 10, 2)
            # Inner ring to show armor health
            armor_ratio = self.armor_hp / self.max_armor
            inner_radius = int(8 * armor_ratio)
            if inner_radius > 0:
                pygame.draw.circle(win, (100, 150, 255), (cx, cy), inner_radius, 1)
