"""Wave class for enemy spawning and management."""

from typing import List

import pygame

from enemies import Enemy, Soldier, Tank, Scout, Boss
from src.point import Point
from game.bullet import Bullet
from game.fields import Filed
from game.map import Map


class Wave:
    def __init__(self, map: Map, towers: List, round_ref):
        self.map = map
        self.enemies = []
        self.towers = towers
        self.round_ref = round_ref
        self.bullets = []
        self.spawn_timer = 0
        self.spawn_interval = 1000
        self.enemies_spawned = 0
        self.total_enemies = 10
        self.enemies_escaped = 0
        self.hp_multiplier: float = 1.0
        self.speed_multiplier: float = 1.0
        self.bounty_multiplier: float = 1.0
        self.enemy_composition: dict = {'soldier': 10}
        self._spawn_queue: list = []

    def draw(self, win: pygame.Surface):
        self.map.draw(win)
        self._draw_enemies(win)
        self._draw_bullets(win)

    def _draw_enemies(self, win: pygame.Surface):
        for enemy in self.enemies:
            enemy.draw(win)

    def _draw_bullets(self, win: pygame.Surface):
        for bullet in self.bullets:
            bullet.draw(win)

    def _build_spawn_queue(self):
        queue = []
        order = ['boss', 'tank', 'scout', 'soldier']
        for enemy_type in order:
            count = self.enemy_composition.get(enemy_type, 0)
            queue.extend([enemy_type] * count)
        while len(queue) < self.total_enemies:
            queue.append('soldier')
        return queue[:self.total_enemies]

    def _spawn_enemy(self) -> Enemy:
        if not hasattr(self, '_spawn_queue') or self._spawn_queue is None:
            self._spawn_queue = self._build_spawn_queue()

        idx = self.enemies_spawned
        enemy_type = self._spawn_queue[idx] if idx < len(self._spawn_queue) else 'soldier'

        spawn_x = self.map.path[0].pos.x - (20 * (idx + 2))
        spawn_y = self.map.path[0].pos.y
        pos = Point(spawn_x, spawn_y)

        if enemy_type == 'tank':
            return Tank(
                pos,
                life_point=Tank.BASE_HP * self.hp_multiplier,
                speed=Tank.BASE_SPEED * self.speed_multiplier,
                bounty=int(Tank.BASE_BOUNTY * self.bounty_multiplier),
            )
        elif enemy_type == 'scout':
            return Scout(
                pos,
                life_point=Scout.BASE_HP * self.hp_multiplier,
                speed=Scout.BASE_SPEED * self.speed_multiplier,
                bounty=int(Scout.BASE_BOUNTY * self.bounty_multiplier),
            )
        elif enemy_type == 'boss':
            return Boss(
                pos,
                life_point=Boss.BASE_HP * self.hp_multiplier,
                speed=Boss.BASE_SPEED * self.speed_multiplier,
                bounty=int(Boss.BASE_BOUNTY * self.bounty_multiplier),
            )
        else:
            return Soldier(
                pos,
                life_point=Soldier.BASE_HP * self.hp_multiplier,
                speed=Soldier.BASE_SPEED * self.speed_multiplier,
                bounty=int(Soldier.BASE_BOUNTY * self.bounty_multiplier),
            )

    def update(self, dt: int, *args, **kwargs):
        self.map.update(*args, **kwargs)

        if self.enemies_spawned < self.total_enemies:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                enemy = self._spawn_enemy()
                self.enemies.append(enemy)
                self.enemies_spawned += 1

        for tower in self.towers:
            tower.update(dt, enemies=self.enemies, bullets=self.bullets, *args, **kwargs)

        for bullet in self.bullets[:]:
            if bullet.update():
                if bullet.target and bullet.target.life_point > 0:
                    bullet.target.life_point -= bullet.damage
            else:
                if not bullet.active:
                    self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            if enemy.previous_pos >= len(self.map.path):
                continue

            target_path = self.map.path[enemy.previous_pos]
            dx = target_path.pos.x - enemy.pos.x
            dy = target_path.pos.y - enemy.pos.y
            distance = (dx * dx + dy * dy) ** 0.5

            if distance < enemy.speed:
                enemy.previous_pos += 1
                if enemy.previous_pos >= len(self.map.path):
                    self.enemies.remove(enemy)
                    self.round_ref.heart -= 1
                    self.enemies_escaped += 1
                    continue

            if distance > 0:
                enemy.pos.x += (dx / distance) * enemy.speed
                enemy.pos.y += (dy / distance) * enemy.speed

    def handle_event(self, event: pygame.event.Event):
        self.map.handle_event(event)

    def is_complete(self) -> bool:
        return self.enemies_spawned >= self.total_enemies and len(self.enemies) == 0
