"""LaserTower - fires through multiple enemies in a line."""

from typing import List
import math

import pygame

from enemy import Enemy
from src.point import Point
from towers.base import Tower


class LaserTower(Tower):
    """Long range, fires continuous beam through multiple enemies in a line: range 6.0, damage 30/tick, cooldown 200 ms, cost $300."""

    tower_type = "Laser"
    cost = 360
    shape_style = "cross"

    def __init__(self, pos: Point):
        self.size = (20, 20)
        self.pos = pygame.Rect(pos.y, pos.x, self.size[0], self.size[1])
        self.range = 6.0
        self.power = 30
        self.level = 1
        self.color = (255, 255, 0)  # bright yellow
        self.range_enable = False
        self.cool_down_time = 200
        self.cool_down = 0
        self._last_target = None  # track last fired target for visual

    def update(self, dt: int, enemies: List[Enemy], bullets: List = None, *args, **kwargs):
        self.mouse_functionality()
        self.cool_down -= dt
        if self.cool_down <= 0:
            range_sq = (self.range * 20) ** 2
            # Find first enemy in range
            for enemy in enemies:
                if self._distance_squared(enemy) <= range_sq:
                    self._fire_laser(enemy, enemies)
                    self._last_target = enemy
                    self.cool_down = self.cool_down_time
                    break

    def _fire_laser(self, primary: Enemy, all_enemies: List[Enemy]):
        """Fire laser through all enemies in a line from tower through primary target."""
        # Fire through all enemies in a straight line
        tower_cx = self.pos.x + (self.size[0] // 2)
        tower_cy = self.pos.y + (self.size[1] // 2)

        target_cx = primary.pos.x + (primary.size[0] // 2)
        target_cy = primary.pos.y + (primary.size[1] // 2)

        # Direction vector from tower to target
        dx = target_cx - tower_cx
        dy = target_cy - tower_cy
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 1:
            return

        # Normalize direction
        dx /= distance
        dy /= distance

        # Check all enemies for line intersection
        for enemy in all_enemies:
            ecx = enemy.pos.x + (enemy.size[0] // 2)
            ecy = enemy.pos.y + (enemy.size[1] // 2)

            # Project enemy center onto laser line
            ex = ecx - tower_cx
            ey = ecy - tower_cy
            dot = ex * dx + ey * dy

            # If projection is positive (in front of tower), check distance to line
            if dot >= 0:
                # Distance from point to line
                proj_x = tower_cx + dot * dx
                proj_y = tower_cy + dot * dy
                point_dist = math.sqrt((ecx - proj_x) ** 2 + (ecy - proj_y) ** 2)

                if point_dist < 12:  # Hit radius
                    enemy.life_point -= self.power

    def draw(self, win: pygame.Surface):
        cx = self.pos.x + (self.size[0] // 2)
        cy = self.pos.y + (self.size[1] // 2)

        # Laser tower - cross pattern with center core
        # Cross beams
        pygame.draw.line(win, (220, 220, 100), (self.pos.x + 2, cy), (self.pos.x + 18, cy), 2)
        pygame.draw.line(win, (220, 220, 100), (cx, self.pos.y + 2), (cx, self.pos.y + 18), 2)

        # Center core
        pygame.draw.circle(win, (255, 255, 0), (cx, cy), 5)  # Bright yellow
        pygame.draw.circle(win, (255, 0, 255), (cx, cy), 5, 1)  # Magenta border

        # Draw active laser beam to last target if available
        if self._last_target:
            target_cx = self._last_target.pos.x + (self._last_target.size[0] // 2)
            target_cy = self._last_target.pos.y + (self._last_target.size[1] // 2)

            # Draw pulsing laser line
            pygame.draw.line(win, (255, 255, 100), (cx, cy), (target_cx, target_cy), 2)

        self._draw_range_circle(win)

    def mouse_functionality(self) -> None:
        self.range_enable = self.pos.collidepoint(pygame.mouse.get_pos())
