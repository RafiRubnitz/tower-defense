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
    {'class': BasicTower,       'name': 'Basic',      'cost': 120, 'key': '1'},  # Increased from 100
    {'class': SniperTower,      'name': 'Sniper',     'cost': 240, 'key': '2'},  # Increased from 200
    {'class': MachineGunTower,  'name': 'MachineGun', 'cost': 180, 'key': '3'},  # Increased from 150
    {'class': SplashTower,      'name': 'Splash',     'cost': 300, 'key': '4'},  # Increased from 250
    {'class': FreezeTower,      'name': 'Freeze',     'cost': 210, 'key': '5'},  # Increased from 175
    {'class': LaserTower,       'name': 'Laser',      'cost': 360, 'key': '6'},  # Increased from 300
]
