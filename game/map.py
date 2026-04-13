"""Map class for the game grid."""

from typing import List, Tuple

import pygame

from enemies import Enemy
from towers import Tower
from src.point import Point
from game.fields import Filed, PathField


class Map(object):
    size: Tuple[int, int]
    path: List[PathField]
    grid: List[List[Filed]]
    towers: List[Tower]
    enemies: List[Enemy]
    field_pressed: Filed
    is_field_pressed: bool

    def __init__(self):
        self.size = (40, 30)
        self.path = []
        self.grid = []
        self.is_field_pressed = False
        self.field_pressed = Filed(-1,-1,20,20, (200,200,200))

        for col in range(self.size[0]):
            self.grid.append([])
            for row in range(self.size[1]):
                self.grid[col].append(Filed(col * 20, row * 20, 20, 20, (255, 255, 255)))

        for i in range(self.size[0] // 2):
            self.path.append(PathField(i * 20, (self.size[1] // 2) * 20, 20, 20))

        for i in range(self.size[1] // 2, self.size[1]):
            self.path.append(PathField(self.size[0] // 2 * 20, i * 20, 20, 20))

    def draw(self, win: pygame.Surface):
        self._draw_grid(win)
        self._draw_path(win)
        self._draw_parsed_field(win)

    def _draw_grid(self, win: pygame.Surface):
        grass_color = (34, 139, 34)
        for row in self.grid:
            for point in row:
                pygame.draw.rect(win, grass_color, point.pos)

        grid_line_color = (25, 120, 25)
        for col in range(0, self.size[0] * 20, 20):
            pygame.draw.line(win, grid_line_color, (col, 0), (col, self.size[1] * 20), 1)
        for row in range(0, self.size[1] * 20, 20):
            pygame.draw.line(win, grid_line_color, (0, row), (self.size[0] * 20, row), 1)

    def _draw_path(self, win: pygame.Surface):
        for point in self.path:
            pygame.draw.rect(win, point.color, point.pos)
            border_color = (70, 70, 70)
            pygame.draw.rect(win, border_color, point.pos, 2)

        for i, point in enumerate(self.path):
            center_x = point.pos.x + 10
            center_y = point.pos.y + 10

            if i < len(self.path) - 1:
                next_point = self.path[i + 1]
                next_center_x = next_point.pos.x + 10
                next_center_y = next_point.pos.y + 10

                if next_center_x > center_x or next_center_x < center_x:
                    pygame.draw.line(win, (200, 200, 50), (point.pos.x + 5, center_y), (point.pos.x + 15, center_y), 2)
                elif next_center_y > center_y or next_center_y < center_y:
                    pygame.draw.line(win, (200, 200, 50), (center_x, point.pos.y + 5), (center_x, point.pos.y + 15), 2)

        if self.path:
            start = self.path[0]
            end = self.path[-1]

            pygame.draw.rect(win, (0, 150, 0), (start.pos.x + 2, start.pos.y + 2, 16, 16))
            pygame.draw.rect(win, (0, 100, 0), (start.pos.x + 2, start.pos.y + 2, 16, 16), 2)
            pygame.draw.polygon(win, (100, 255, 100), [
                (start.pos.x + 10, start.pos.y + 4),
                (start.pos.x + 6, start.pos.y + 14),
                (start.pos.x + 10, start.pos.y + 10),
                (start.pos.x + 14, start.pos.y + 14)
            ])

            pygame.draw.rect(win, (150, 0, 0), (end.pos.x + 2, end.pos.y + 2, 16, 16))
            pygame.draw.rect(win, (100, 0, 0), (end.pos.x + 2, end.pos.y + 2, 16, 16), 2)
            pygame.draw.line(win, (255, 50, 50), (end.pos.x + 4, end.pos.y + 4), (end.pos.x + 16, end.pos.y + 16), 3)
            pygame.draw.line(win, (255, 50, 50), (end.pos.x + 16, end.pos.y + 4), (end.pos.x + 4, end.pos.y + 16), 3)

    def _draw_parsed_field(self, win: pygame.Surface) -> None:
        if self.is_field_pressed:
            pygame.draw.rect(win, self.field_pressed.color, self.field_pressed.pos)

    @classmethod
    def load_from_path_data(cls, path_data: list) -> "Map":
        """Create a Map with path loaded from DB path_data."""
        instance = cls.__new__(cls)
        instance.size = (40, 30)
        instance.path = []
        instance.grid = []
        instance.is_field_pressed = False
        instance.field_pressed = Filed(-1, -1, 20, 20, (200, 200, 200))

        for col in range(instance.size[0]):
            instance.grid.append([])
            for row in range(instance.size[1]):
                instance.grid[col].append(Filed(col * 20, row * 20, 20, 20, (255, 255, 255)))

        for col, row in path_data:
            instance.path.append(PathField(col * 20, row * 20, 20, 20))

        return instance

    def update(self, *args, **kwargs):
        ...

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            nx = mouse_pos[0] // 20 * 20
            ny = mouse_pos[1] // 20 * 20

            if not self.is_field_pressed:
                self.is_field_pressed = True
                self.field_pressed.pos.x = nx
                self.field_pressed.pos.y = ny
            elif self.field_pressed.pos.x == nx and self.field_pressed.pos.y == ny:
                self.is_field_pressed = False
                self.field_pressed.pos.x = -1
                self.field_pressed.pos.y = -1
            else:
                self.field_pressed.pos.x = nx
                self.field_pressed.pos.y = ny
