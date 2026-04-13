"""Tower classes for Tower Defense.

Hierarchy:
  Tower          — abstract base
  BasicTower     — balanced all-rounder ($100)
  SniperTower    — long range, high damage, slow fire ($200)
  MachineGunTower — short range, low damage, very fast fire ($150)
  SplashTower    — area-of-effect damage on hit ($250)
"""

from typing import Tuple, List

import pygame

from enemy import Enemy
from src.point import Point

# Import Bullet from map module (will be available at runtime)
def get_bullet_class():
    from map import Bullet
    return Bullet


class Tower(object):
    range: float
    power: float
    cool_down_time: int
    level: int
    pos: pygame.Rect
    size: Tuple[int, int]
    color: Tuple[int, int, int]
    range_enable: bool
    cool_down: int
    # Tower type label shown in UI
    tower_type: str = "Basic"
    cost: int = 100

    def draw(self, win: pygame.Surface):
        ...

    def update(self, dt: int, enemies: List[Enemy], *args, **kwargs):
        ...

    def handle_event(self, event: pygame.event.Event):
        ...

    def find_enemy(self):
        ...

    def shot(self, target: Point):
        ...

    def upgrade(self, *args, **kwargs):
        ...

    def mouse_functionality(self) -> None:
        ...

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _distance_squared(self, enemy: Enemy) -> float:
        tcx = self.pos.x + (self.size[0] // 2)
        tcy = self.pos.y + (self.size[1] // 2)
        ecx = enemy.pos.x + (enemy.size[0] // 2)
        ecy = enemy.pos.y + (enemy.size[1] // 2)
        return (ecx - tcx) ** 2 + (ecy - tcy) ** 2

    def _draw_range_circle(self, win: pygame.Surface):
        if self.range_enable:
            cx = self.pos.x + (self.size[0] // 2)
            cy = self.pos.y + (self.size[1] // 2)
            r = int(self.range * 20)
            surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (0, 255, 0, 40), (r, r), r)
            pygame.draw.circle(surface, (0, 255, 0, 100), (r, r), r, 1)
            win.blit(surface, (cx - r, cy - r))


class BasicTower(Tower):
    """Balanced all-rounder: range 3.5, damage 50, cooldown 600 ms."""

    tower_type = "Basic"
    cost = 100

    def __init__(self, pos: Point):
        self.size = (20, 20)
        self.pos = pygame.Rect(pos.y, pos.x, self.size[0], self.size[1])
        self.range = 3.5
        self.power = 50
        self.level = 1
        self.color = (70, 130, 180)
        self.base_color = (139, 69, 19)
        self.turret_color = (47, 79, 79)
        self.range_enable = False
        self.cool_down_time = 600
        self.cool_down = 0

    def upgrade(self):
        ...

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
            bullets.append(Bullet(cx, cy, target, self.power, self.color))
        else:
            target.life_point -= self.power

    def draw(self, win: pygame.Surface):
        cx = self.pos.x + (self.size[0] // 2)
        cy = self.pos.y + (self.size[1] // 2)

        base_rect = pygame.Rect(self.pos.x + 2, self.pos.y + 2, self.size[0] - 4, self.size[1] - 4)
        pygame.draw.rect(win, self.base_color, base_rect)
        pygame.draw.rect(win, (0, 0, 0), base_rect, 2)

        pygame.draw.circle(win, self.turret_color, (cx, cy), 6)
        pygame.draw.circle(win, (0, 0, 0), (cx, cy), 6, 2)

        pygame.draw.line(win, (30, 30, 30), (cx, cy), (cx, cy - 8), 3)

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.range_enable = self.pos.collidepoint(mouse_pos)


class SniperTower(Tower):
    """Long range, high damage, slow cooldown: range 8, damage 200, cooldown 2000 ms."""

    tower_type = "Sniper"
    cost = 200

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


class MachineGunTower(Tower):
    """Short range, low damage, very fast fire: range 3, damage 15, cooldown 100 ms."""

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


class SplashTower(Tower):
    """AoE damage: range 4, damage 80 in splash radius 40 px, cooldown 1000 ms."""

    tower_type = "Splash"
    cost = 250
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


# Tower type registry used by the placement UI
TOWER_TYPES = [
    {'class': BasicTower,      'name': 'Basic',      'cost': 100, 'key': '1'},
    {'class': SniperTower,     'name': 'Sniper',     'cost': 200, 'key': '2'},
    {'class': MachineGunTower, 'name': 'MachineGun', 'cost': 150, 'key': '3'},
    {'class': SplashTower,     'name': 'Splash',     'cost': 250, 'key': '4'},
]
