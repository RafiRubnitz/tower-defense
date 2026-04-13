"""Grid field classes for the game map."""

from typing import Tuple

import pygame


class Filed:
    pos: pygame.Rect
    color: Tuple[int, int, int]

    def __init__(self, col, row, width, height, color=(34, 139, 34)):  # Forest green grass
        self.pos = pygame.Rect(col, row, width, height)
        self.color = color


class PathField(Filed):

    def __init__(self, col, row, width, height, color=(105, 105, 105)):  # Gray road
        super().__init__(col, row, width, height, color)
