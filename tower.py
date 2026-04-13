from typing import Tuple, List

import pygame

from enemies import Enemy
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


class BasicTower(Tower):

    def __init__(self, pos: Point):
        self.size = (20, 20)
        self.pos = pygame.Rect(pos.y, pos.x, self.size[0], self.size[1])
        self.range = 3.5
        self.power = 50
        self.level = 1
        self.color = (70, 130, 180)  # Steel blue tower
        self.base_color = (139, 69, 19)  # Brown base
        self.turret_color = (47, 79, 79)  # Dark slate gray turret
        self.range_enable = False
        self.cool_down_time = 600
        self.cool_down = 0

    def upgrade(self):
        ...

    def update(self, dt: int, enemies: List[Enemy], bullets: List = None, *args, **kwargs):
        self.mouse_functionality()
        self.cool_down -= dt
        if self.cool_down <= 0:
            for enemy in enemies:
                # Calculate distance from tower center to enemy center
                tower_center_x = self.pos.x + (self.size[0] // 2)
                tower_center_y = self.pos.y + (self.size[1] // 2)
                enemy_center_x = enemy.pos.x + (enemy.size[0] // 2)
                enemy_center_y = enemy.pos.y + (enemy.size[1] // 2)

                dx = enemy_center_x - tower_center_x
                dy = enemy_center_y - tower_center_y
                distance_squared = dx * dx + dy * dy

                # Range is in grid units (20px per unit)
                range_squared = (self.range * 20) ** 2

                if distance_squared <= range_squared:
                    self.shot(enemy, bullets, tower_center_x, tower_center_y)
                    self.cool_down = self.cool_down_time
                    break

    def shot(self, target: Enemy, bullets: List = None, tower_center_x: int = None, tower_center_y: int = None):
        if bullets is not None and tower_center_x is not None and tower_center_y is not None:
            Bullet = get_bullet_class()
            bullets.append(Bullet(tower_center_x, tower_center_y, target, self.power, self.color))
        else:
            target.life_point -= self.power
            print(f"Enemy: {target.id} hit, life point: {target.life_point}")

    def draw(self, win) -> None:
        center_x = self.pos.x + (self.size[0] // 2)
        center_y = self.pos.y + (self.size[1] // 2)

        # Draw tower base (square with rounded corners effect)
        base_rect = pygame.Rect(self.pos.x + 2, self.pos.y + 2, self.size[0] - 4, self.size[1] - 4)
        pygame.draw.rect(win, self.base_color, base_rect)
        pygame.draw.rect(win, (0, 0, 0), base_rect, 2)  # Border

        # Draw turret (circle in the center)
        pygame.draw.circle(win, self.turret_color, (center_x, center_y), 6)
        pygame.draw.circle(win, (0, 0, 0), (center_x, center_y), 6, 2)  # Turret border

        # Draw cannon barrel (small line pointing toward last target or up)
        barrel_end_x = center_x
        barrel_end_y = center_y - 8
        pygame.draw.line(win, (30, 30, 30), (center_x, center_y), (barrel_end_x, barrel_end_y), 3)

        # Draw range indicator when hovered
        if self.range_enable:
            range_surface = pygame.Surface((self.range * 40, self.range * 40), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (0, 255, 0, 50),
                               (int(self.range * 20), int(self.range * 20)),
                               int(self.range * 20))
            win.blit(range_surface,
                     (center_x - int(self.range * 20), center_y - int(self.range * 20)))

    def mouse_functionality(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.range_enable = self.pos.collidepoint(mouse_pos)
