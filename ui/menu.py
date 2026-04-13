from enum import Enum
from typing import Optional, Callable, List, Dict
import pygame


class GameState(Enum):
    """מצבי משחק שונים"""
    MAIN_MENU = "main_menu"
    MAP_SELECTION = "map_selection"
    SETTINGS = "settings"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class Button:
    """מחלקה לכפתור"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, callback: Callable = None,
                 font_size: int = 36,
                 base_color: tuple = (80, 80, 100),
                 hover_color: tuple = (120, 120, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False
        self.enabled = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """טפל באירועים, החזר True אם הכפתור נלחץ"""
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.hovered and self.callback:
                self.callback()
                return True
        return False

    def draw(self, win: pygame.Surface):
        """צייר את הכפתור"""
        if not self.enabled:
            color = (50, 50, 50)
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.base_color

        # צייר רקע עם עיגול בפינות
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        pygame.draw.rect(win, (150, 150, 180), self.rect, 2, border_radius=8)

        # צייר טקסט במרכז
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)


class Label:
    """מחלקה לתווית טקסט"""

    def __init__(self, x: int, y: int, text: str,
                 font_size: int = 24, color: tuple = (255, 255, 255),
                 center: bool = False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.center = center

    def set_text(self, text: str):
        self.text = text

    def draw(self, win: pygame.Surface):
        text_surface = self.font.render(self.text, True, self.color)
        if self.center:
            text_rect = text_surface.get_rect(center=(self.x, self.y))
        else:
            text_rect = text_surface.get_rect(topleft=(self.x, self.y))
        win.blit(text_surface, text_rect)


class MenuManager:
    """מנהל את כל המסכים והתפריטים"""

    def __init__(self, game, win: pygame.Surface):
        self.game = game
        self.win = win
        self.current_state = GameState.MAIN_MENU
        self.buttons: Dict[str, Button] = {}
        self.labels: Dict[str, Label] = {}
        self.selected_map_id: Optional[int] = None
        self.selected_config_id: Optional[int] = None

        # הגדרות UI
        self.screen_width = win.get_width()
        self.screen_height = win.get_height()

        # אתחול מסכים
        self._init_main_menu()
        self._init_map_selection()
        self._init_settings()

    def _init_main_menu(self):
        """אתחול תפריט ראשי"""
        # כפתורים
        button_width = 250
        button_height = 50
        start_x = (self.screen_width - button_width) // 2

        self.buttons['btn_play'] = Button(
            start_x, 200, button_width, button_height,
            "Play", self._on_play_click
        )
        self.buttons['btn_maps'] = Button(
            start_x, 270, button_width, button_height,
            "Select Map", self._on_maps_click
        )
        self.buttons['btn_settings'] = Button(
            start_x, 340, button_width, button_height,
            "Settings", self._on_settings_click
        )
        self.buttons['btn_quit'] = Button(
            start_x, 410, button_width, button_height,
            "Quit", self._on_quit_click
        )

        # תוויות
        self.labels['title'] = Label(
            self.screen_width // 2, 80,
            "TOWER DEFENSE",
            font_size=72, color=(255, 215, 0), center=True
        )
        self.labels['subtitle'] = Label(
            self.screen_width // 2, 140,
            "=== ====== ===",
            font_size=36, color=(200, 200, 200), center=True
        )

        # High score label
        self._update_high_score()

    def _update_high_score(self):
        """עדכון תווית הניקוד הגבוה"""
        from database import Database
        db = Database()
        high_scores = db.get_high_scores(1)
        db.close()

        if high_scores:
            score_text = f"High Score: {high_scores[0]['score']}"
        else:
            score_text = "High Score: --"

        self.labels['high_score'] = Label(
            self.screen_width // 2, 520,
            score_text,
            font_size=28, color=(100, 255, 100), center=True
        )

    def _init_map_selection(self):
        """אתחול מסך בחירת מפה"""
        button_width = 200
        button_height = 45
        start_x = (self.screen_width - button_width) // 2

        # כפתור חזרה
        self.buttons['btn_back_maps'] = Button(
            20, 20, 120, 40,
            "< Back", self._on_back_from_maps,
            font_size=28
        )

        # כפתור התחל
        self.buttons['btn_start_game'] = Button(
            start_x, 500, button_width, button_height,
            "Start Game", self._on_start_game_click,
            font_size=32
        )
        self.buttons['btn_start_game'].enabled = False  # מבוטל עד לבחירת מפה

        # כפתורי בחירת מפה יווצרו דינמית
        self.map_buttons: List[Button] = []

        # תוויות
        self.labels['map_title'] = Label(
            self.screen_width // 2, 40,
            "Select Map",
            font_size=48, color=(255, 215, 0), center=True
        )

    def _init_settings(self):
        """אתחול מסך הגדרות"""
        button_width = 200
        button_height = 45
        start_x = (self.screen_width - button_width) // 2

        # כפתור חזרה
        self.buttons['btn_back_settings'] = Button(
            20, 20, 120, 40,
            "< Back", self._on_back_from_settings,
            font_size=28
        )

        # כפתורי הגדרות
        self.buttons['btn_difficulty'] = Button(
            start_x, 150, button_width, button_height,
            "Difficulty: Normal", self._on_difficulty_click,
            font_size=32
        )

        self.buttons['btn_lives'] = Button(
            start_x, 230, button_width, button_height,
            "Lives: 10", self._on_lives_click,
            font_size=32
        )

        self.buttons['btn_money'] = Button(
            start_x, 310, button_width, button_height,
            "Starting Money: 450", self._on_money_click,
            font_size=28
        )

        # תוויות
        self.labels['settings_title'] = Label(
            self.screen_width // 2, 60,
            "Settings",
            font_size=48, color=(255, 215, 0), center=True
        )

        # הגדרות שמורות
        self.settings = {
            'difficulty': 'normal',  # easy, normal, hard
            'lives': 10,
            'starting_money': 450
        }

        # טעינת הגדרות שמורות
        self._load_settings()

    def _load_settings(self):
        """טעינת הגדרות מה-DB"""
        from database import Database
        db = Database()

        self.settings['difficulty'] = db.get_setting('difficulty', 'normal')
        self.settings['lives'] = int(db.get_setting('lives', '10'))
        self.settings['starting_money'] = int(db.get_setting('starting_money', '450'))

        db.close()
        self._update_settings_ui()

    def _save_settings(self):
        """שמירת הגדרות ל-DB"""
        from database import Database
        db = Database()

        db.save_setting('difficulty', self.settings['difficulty'])
        db.save_setting('lives', str(self.settings['lives']))
        db.save_setting('starting_money', str(self.settings['starting_money']))

        db.close()

    def _update_settings_ui(self):
        """עדכון UI של ההגדרות"""
        diff_display = self.settings['difficulty'].capitalize()
        self.buttons['btn_difficulty'].text = f"Difficulty: {diff_display}"

        self.buttons['btn_lives'].text = f"Lives: {self.settings['lives']}"
        self.buttons['btn_money'].text = f"Starting Money: ${self.settings['starting_money']}"

    def _on_difficulty_click(self):
        """שינוי רמת קושי"""
        difficulties = ['easy', 'normal', 'hard']
        current_idx = difficulties.index(self.settings['difficulty'])
        self.settings['difficulty'] = difficulties[(current_idx + 1) % 3]
        self._update_settings_ui()
        self._save_settings()

    def _on_lives_click(self):
        """שינוי כמות לבות"""
        options = [5, 10, 15, 20]
        current_idx = options.index(self.settings['lives']) if self.settings['lives'] in options else 1
        self.settings['lives'] = options[(current_idx + 1) % len(options)]
        self._update_settings_ui()
        self._save_settings()

    def _on_money_click(self):
        """שינוי כסף התחלתי"""
        options = [200, 350, 450, 600, 800]
        current_idx = options.index(self.settings['starting_money']) if self.settings['starting_money'] in options else 2
        self.settings['starting_money'] = options[(current_idx + 1) % len(options)]
        self._update_settings_ui()
        self._save_settings()

    # ========== Event Handlers ==========

    def _on_play_click(self):
        """כפתור Play נלחץ"""
        self.current_state = GameState.MAP_SELECTION
        self._refresh_map_buttons()

    def _on_maps_click(self):
        """כפתור Select Map נלחץ"""
        self.current_state = GameState.MAP_SELECTION
        self._refresh_map_buttons()

    def _on_settings_click(self):
        """כפתור Settings נלחץ"""
        self.current_state = GameState.SETTINGS

    def _on_quit_click(self):
        """כפתור Quit נלחץ"""
        import sys
        pygame.quit()
        sys.exit()

    def _on_back_from_maps(self):
        """חזרה מתפריט המפות"""
        self.current_state = GameState.MAIN_MENU
        self._update_high_score()

    def _on_back_from_settings(self):
        """חזרה מהגדרות"""
        self.current_state = GameState.MAIN_MENU

    def _on_map_selected(self, map_id: int, map_name: str):
        """מפה נבחרה"""
        self.selected_map_id = map_id
        self.buttons['btn_start_game'].enabled = True
        self.buttons['btn_start_game'].text = f"Start: {map_name}"

    def _on_start_game_click(self):
        """התחלת משחק"""
        if self.selected_map_id:
            # העבר את הבחירה למשחק
            self.game.start_game_from_menu(
                map_id=self.selected_map_id,
                settings=self.settings.copy()
            )

    def handle_event(self, event: pygame.event.Event):
        """טפל באירועים לפי המצב הנוכחי"""
        if self.current_state == GameState.MAIN_MENU:
            for button in self.buttons.values():
                if button in [self.buttons['btn_play'],
                             self.buttons['btn_maps'],
                             self.buttons['btn_settings'],
                             self.buttons['btn_quit']]:
                    button.handle_event(event)

        elif self.current_state == GameState.MAP_SELECTION:
            self.buttons['btn_back_maps'].handle_event(event)
            self.buttons['btn_start_game'].handle_event(event)

            for btn in self.map_buttons:
                btn.handle_event(event)

        elif self.current_state == GameState.SETTINGS:
            self.buttons['btn_back_settings'].handle_event(event)
            self.buttons['btn_difficulty'].handle_event(event)
            self.buttons['btn_lives'].handle_event(event)
            self.buttons['btn_money'].handle_event(event)

    def draw(self):
        """צייר את המסך הנוכחי"""
        if self.current_state == GameState.MAIN_MENU:
            self._draw_main_menu()
        elif self.current_state == GameState.MAP_SELECTION:
            self._draw_map_selection()
        elif self.current_state == GameState.SETTINGS:
            self._draw_settings()

    def _draw_main_menu(self):
        """צייר תפריט ראשי"""
        # רקע כהה
        self.win.fill((30, 30, 40))

        # צייר כפתורים
        for key in ['btn_play', 'btn_maps', 'btn_settings', 'btn_quit']:
            self.buttons[key].draw(self.win)

        # צייר תוויות
        self.labels['title'].draw(self.win)
        self.labels['subtitle'].draw(self.win)
        self._update_high_score()
        self.labels['high_score'].draw(self.win)

    def _refresh_map_buttons(self):
        """רענון כפתורי בחירת המפות"""
        from database import Database
        db = Database()
        maps = db.get_all_maps()
        db.close()

        self.map_buttons = []
        button_width = 350
        button_height = 45
        start_x = (self.screen_width - button_width) // 2
        start_y = 100

        for i, map_info in enumerate(maps):
            difficulty_str = "★" * map_info['difficulty']
            builtin_str = " [BUILTIN]" if map_info['is_builtin'] else ""
            btn_text = f"{map_info['name']}{builtin_str} ({difficulty_str})"

            btn = Button(
                start_x, start_y + i * (button_height + 10),
                button_width, button_height,
                btn_text,
                lambda mid=map_info['id'], mname=map_info['name']:
                self._on_map_selected(mid, mname),
                font_size=28
            )
            self.map_buttons.append(btn)

    def _draw_map_selection(self):
        """צייר מסך בחירת מפות"""
        self.win.fill((30, 30, 40))

        # כפתורים
        self.buttons['btn_back_maps'].draw(self.win)
        self.buttons['btn_start_game'].draw(self.win)

        # תווית
        self.labels['map_title'].draw(self.win)

        # כפתורי מפות
        for btn in self.map_buttons:
            btn.draw(self.win)

    def _draw_settings(self):
        """צייר מסך הגדרות"""
        self.win.fill((30, 30, 40))

        # כפתורים
        self.buttons['btn_back_settings'].draw(self.win)
        self.buttons['btn_difficulty'].draw(self.win)
        self.buttons['btn_lives'].draw(self.win)
        self.buttons['btn_money'].draw(self.win)

        # תווית
        self.labels['settings_title'].draw(self.win)

        # הסברים
        help_label = Label(
            self.screen_width // 2, 450,
            "Click buttons to cycle through options",
            font_size=24, color=(150, 150, 150), center=True
        )
        help_label.draw(self.win)
