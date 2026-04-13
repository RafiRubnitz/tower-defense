from typing import Tuple


class Point(object):

    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __iadd__(self, other: Tuple[int, int]):
        self.x += other[0]
        self.y += other[1]
        return self

    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y



