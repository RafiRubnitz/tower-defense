import sys
from typing import List

import pygame

from map import Map, Wave, Round
from player import Player
from src.point import Point


class Game:
    win: pygame.Surface
    player: Player
    maps: List[Map]
    current_map: Map
    current_wave: Wave
    current_round: Round
    paused: bool


    def __init__(self, win: pygame.Surface):
        self.win = win
        self.clock = pygame.time.Clock()
        self.current_round = Round()
        self.paused = False

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        # Restart game
                        self.current_round = Round()

                self.current_round.handle_event(event)

            if not self.paused:
                self.current_round.update(dt)

            self.win.fill((255, 255, 255))
            self.current_round.draw(self.win)

            pygame.display.update()

        pygame.quit()
        sys.exit()

    def load_map(self):
        ...

    def start_wave(self):
        ...

    def get_mouse_pressed(self) -> None | Point:

        if pygame.event.get(pygame.MOUSEBUTTONUP):
            x, y = pygame.mouse.get_pos()
            return Point(x, y)
        return None

