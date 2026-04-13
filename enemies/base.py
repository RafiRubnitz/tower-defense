from typing import Tuple

import pygame


class Enemy(object):

    _UUID: int = 0

    id: int
    life_point: float
    speed: int
    level: int
    size: Tuple[int, int]
    color: Tuple[int, int, int]
    pos: pygame.Rect
    previous_pos: int

    @classmethod
    def get_next_uuid(cls) -> int:
        cls._UUID += 1
        return cls._UUID

    def update(self, *args, **kwargs):
        ...

    def draw(self, win: pygame.Surface):
        ...

    def move(self, direction):
        ...

    def hit(self):
        ...

    def death(self):
        ...
