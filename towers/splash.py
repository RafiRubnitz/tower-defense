"""SplashTower - area of effect damage."""

from typing import List, Tuple

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower, get_bullet_class


class SplashTower(Tower):
    """AoE damage: range 4, damage 80 in splash radius 40 px, cooldown 1000 ms, cost $250."""

    tower_type = "Splash"
    cost = 300
    shape_style = "circle"
    SPLASH_RADIUS = 40  # pixels

    def __init__(self, pos: Point):
        self.size = (20, 20)
        self.pos = pygame.Rect(pos.y, pos.x, self.size[0], self.size[1])
        self.range = 4.0
        self.power = 80
        self.level = 1
        self.color = (200, 100, 50)
        self.range_enable = False
        self.cool_down_time = 1000
        self.cool_down = 0
        self._last_target_pos: Tuple[int, int] = (0, 0)

    def update(self, dt: int, enemies: List[Enemy], bullets: List = None, *args, **kwargs):
        self.mouse_functionality()
        self.cool_down -= dt
        if self.cool_down <= 0:
            range_sq = (self.range * 20) ** 2
            for enemy in enemies:
                if self._distance_squared(enemy) <= range_sq:
                    self._fire_splash(enemy, enemies, bullets)
                    self.cool_down = self.cool_down_time
                    break

    def _fire_splash(self, primary: Enemy, all_enemies: List[Enemy], bullets: List):
        """Deal damage to all enemies within SPLASH_RADIUS of the primary target."""
        if bullets is not None:
            Bullet = get_bullet_class()
            cx = self.pos.x + (self.size[0] // 2)
            cy = self.pos.y + (self.size[1] // 2)
            # Single visible bullet for the primary target
            bullets.append(Bullet(cx, cy, primary, self.power, self.color, speed=8))

        # Splash damage to nearby enemies (applied immediately)
        target_cx = primary.pos.x + primary.size[0] // 2
        target_cy = primary.pos.y + primary.size[1] // 2
        self._last_target_pos = (target_cx, target_cy)
        splash_r_sq = self.SPLASH_RADIUS ** 2
        for enemy in all_enemies:
            ecx = enemy.pos.x + enemy.size[0] // 2
            ecy = enemy.pos.y + enemy.size[1] // 2
            if (ecx - target_cx) ** 2 + (ecy - target_cy) ** 2 <= splash_r_sq:
                if enemy is not primary:
                    enemy.life_point -= self.power * 0.6  # 60% splash damage

    def draw(self, win: pygame.Surface):
        cx = self.pos.x + (self.size[0] // 2)
        cy = self.pos.y + (self.size[1] // 2)

        # Orange base
        base_rect = pygame.Rect(self.pos.x + 1, self.pos.y + 1, self.size[0] - 2, self.size[1] - 2)
        pygame.draw.rect(win, (100, 50, 20), base_rect)
        pygame.draw.rect(win, (180, 80, 30), base_rect, 2)

        # Mortar barrel (wide short barrel pointing up)
        pygame.draw.circle(win, (200, 100, 50), (cx, cy), 6)
        pygame.draw.circle(win, (120, 60, 20), (cx, cy), 6, 2)
        pygame.draw.rect(win, (80, 40, 10), pygame.Rect(cx - 3, cy - 7, 6, 7))

        # Spark dots (aesthetic)
        for spark_offset in [(-6, -6), (6, -6), (-6, 6), (6, 6)]:
            sx = self.pos.x + self.size[0] // 2 + spark_offset[0]
            sy = self.pos.y + self.size[1] // 2 + spark_offset[1]
            pygame.draw.circle(win, (255, 150, 50), (sx, sy), 2)

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
