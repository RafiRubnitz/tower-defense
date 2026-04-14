import sys
from typing import Optional

import pygame

from map import Map, Wave, Round
from player import Player
from src.game_state import GameState
from src.point import Point
from ui.menu import MenuManager


class Game:
    """Main game controller.

    Owns the main loop and routes events / drawing to either the
    MenuManager (when in a menu state) or the active Round (when playing).
    """

    win: pygame.Surface
    state: GameState
    menu: MenuManager
    current_round: Optional[Round]
    paused: bool

    def __init__(self, win: pygame.Surface):
        pygame.font.init()
        pygame.mixer.init()
        self.win = win
        self.clock = pygame.time.Clock()
        self.state = GameState.MAIN_MENU
        self.current_round = None
        self.paused = False

        # MenuManager receives a reference to this Game so it can call
        # start_game_from_menu() when the player confirms a map selection.
        self.menu = MenuManager(self, win)

    # ------------------------------------------------------------------
    # Public API called by MenuManager
    # ------------------------------------------------------------------

    def start_game_from_menu(self, map_id: int, settings: dict):
        """Load the selected map from the database and start a new round."""
        from database import Database
        db = Database()
        map_data = db.get_map(map_id)
        db.close()

        if map_data is None:
            # Fallback: use the default procedural map
            game_map = Map()
        else:
            game_map = Map.load_from_path_data(map_data['path'])

        lives = settings.get('lives', 10)
        money = settings.get('starting_money', 450)
        difficulty = settings.get('difficulty', 'normal')
        game_mode = settings.get('game_mode', 'classic')  # 'classic' or 'endless'

        self.current_round = Round(
            map_instance=game_map,
            starting_lives=lives,
            starting_money=money,
            return_to_menu=self._return_to_menu,
            difficulty=difficulty,
            total_waves=10,
            game_mode=game_mode,
        )
        self.state = GameState.PLAYING
        self.paused = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _return_to_menu(self):
        """Called by Round when the player clicks 'Main Menu'."""
        self.current_round = None
        self.state = GameState.MAIN_MENU
        self.menu.current_state = GameState.MAIN_MENU
        self.paused = False

    def _restart_round(self):
        """Restart the current round without going back to menu."""
        if self.current_round is not None:
            self.current_round.__init__(
                return_to_menu=self.current_round.return_to_menu
            )

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif self.state == GameState.PLAYING:
                    # Keyboard shortcuts only active during gameplay
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            self.paused = not self.paused
                        elif event.key == pygame.K_r:
                            self._restart_round()
                        elif event.key == pygame.K_ESCAPE:
                            self._return_to_menu()

                    if self.current_round is not None:
                        self.current_round.handle_event(event)

                else:
                    # All menu states — route events to MenuManager
                    self.menu.handle_event(event)

            # Update
            if self.state == GameState.PLAYING and not self.paused:
                if self.current_round is not None:
                    self.current_round.update(dt)

            # Draw
            self.win.fill((0, 0, 0))

            if self.state == GameState.PLAYING:
                if self.current_round is not None:
                    self.current_round.draw(self.win)

                if self.paused:
                    self._draw_pause_overlay()
            else:
                # Keep Game state in sync with MenuManager's internal navigation
                # (e.g. MAIN_MENU -> MAP_SELECTION -> SETTINGS transitions).
                # Only sync when we are still in a menu state so that
                # start_game_from_menu() setting PLAYING is never overwritten here.
                if self.menu.current_state != GameState.PLAYING:
                    self.state = self.menu.current_state
                self.menu.draw()

            pygame.display.update()

        pygame.quit()
        sys.exit()

    def _draw_pause_overlay(self):
        overlay = pygame.Surface(self.win.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.win.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.win.get_width() // 2,
                                          self.win.get_height() // 2))
        self.win.blit(text, text_rect)

        small_font = pygame.font.Font(None, 32)
        hint = small_font.render("Press SPACE to resume | ESC for menu", True, (180, 180, 180))
        hint_rect = hint.get_rect(center=(self.win.get_width() // 2,
                                          self.win.get_height() // 2 + 55))
        self.win.blit(hint, hint_rect)

    # ------------------------------------------------------------------
    # Legacy stubs (kept so nothing breaks if called externally)
    # ------------------------------------------------------------------

    def load_map(self):
        ...

    def start_wave(self):
        ...

    def get_mouse_pressed(self) -> None | Point:
        if pygame.event.get(pygame.MOUSEBUTTONUP):
            x, y = pygame.mouse.get_pos()
            return Point(x, y)
        return None
