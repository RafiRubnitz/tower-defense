"""Tower classes and registry for Tower Defense."""

from towers.base import Tower
from towers.basic import BasicTower
from towers.sniper import SniperTower
from towers.machine_gun import MachineGunTower
from towers.splash import SplashTower
from towers.freeze import FreezeTower
from towers.laser import LaserTower

# Re-export all tower classes
__all__ = [
    'Tower',
    'BasicTower',
    'SniperTower',
    'MachineGunTower',
    'SplashTower',
    'FreezeTower',
    'LaserTower',
    'TOWER_TYPES',
]

# Tower type registry used by placement UI
TOWER_TYPES = [
    {'class': BasicTower,       'name': 'Basic',      'cost': 100, 'key': '1'},
    {'class': SniperTower,      'name': 'Sniper',     'cost': 200, 'key': '2'},
    {'class': MachineGunTower,  'name': 'MachineGun', 'cost': 150, 'key': '3'},
    {'class': SplashTower,      'name': 'Splash',     'cost': 250, 'key': '4'},
    {'class': FreezeTower,      'name': 'Freeze',     'cost': 175, 'key': '5'},
    {'class': LaserTower,       'name': 'Laser',      'cost': 300, 'key': '6'},
]
