"""Tower classes for Tower Defense game."""

from towers.base import Tower
from towers.basic import BasicTower

TOWER_TYPES = [
    {'class': BasicTower, 'name': 'Basic', 'cost': 100, 'key': '1'},
]

__all__ = ['Tower', 'BasicTower', 'TOWER_TYPES']
