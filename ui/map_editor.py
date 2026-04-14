"""Interactive map editor for creating custom maps."""
import json
from typing import List, Optional, Tuple

import pygame

from map_wave_generator import WaveGenerator
from src.game_state import GameState


class MapEditorScreen:
    """Interactive UI for drawing custom maps."""

    GRID_COLS = 40
    GRID_ROWS = 30
    CELL_SIZE = 20
    GRID_WIDTH = GRID_COLS * CELL_SIZE  # 800
    GRID_HEIGHT = GRID_ROWS * CELL_SIZE  # 600
    PANEL_WIDTH = 180
    MIN_PATH_LENGTH = 5

    # Colors
    COLOR_GRASS = (34, 139, 34)
    COLOR_PATH = (105, 105, 105)
    COLOR_GRID_LINE = (200, 200, 200)
    COLOR_ERROR = (255, 0, 0)
    COLOR_TEXT = (255, 255, 255)
    COLOR_BG = (20, 20, 20)
    COLOR_PANEL_BG = (40, 40, 40)
    COLOR_BUTTON = (70, 130, 180)
    COLOR_BUTTON_HOVER = (100, 160, 210)

    def __init__(self, game, db, screen_size: Tuple[int, int]):
        """Initialize map editor.

        Args:
            game: Game instance (for state transitions)
            db: Database instance
            screen_size: (width, height) of screen
        """
        self.game = game
        self.db = db
        self.screen_width, self.screen_height = screen_size
        self.wave_generator = WaveGenerator()

        # Grid and path
        self.path: List[Tuple[int, int]] = []  # List of (col, row) tuples
        self.error_message = ""
        self.error_frame = 0

        # UI state
        self.name_input = ""
        self.name_input_active = True
        self.mouse_pos = (0, 0)
        self.hovered_cell: Optional[Tuple[int, int]] = None

        # Buttons: (rect, label, action)
        self._setup_buttons()

    def _setup_buttons(self):
        """Create button areas in right panel."""
        panel_x = self.GRID_WIDTH
        button_width = self.PANEL_WIDTH - 20
        button_x = panel_x + 10

        self.buttons = {
            "save": pygame.Rect(button_x, 300, button_width, 40),
            "clear": pygame.Rect(button_x, 350, button_width, 40),
            "back": pygame.Rect(button_x, 400, button_width, 40),
        }

        self.name_input_rect = pygame.Rect(panel_x + 10, 50, button_width, 30)

    def handle_event(self, event: pygame.event.EventType) -> Optional[GameState]:
        """Handle events. Returns new state or None."""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self.hovered_cell = self._cell_from_mouse(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_click(event.pos)

        elif event.type == pygame.KEYDOWN:
            if self.name_input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                elif event.key == pygame.K_RETURN:
                    self.name_input_active = False
                elif event.unicode.isprintable() and len(self.name_input) < 25:
                    self.name_input += event.unicode

        return None

    def _handle_click(self, pos: Tuple[int, int]) -> Optional[GameState]:
        """Handle mouse click."""
        # Check buttons
        if self.buttons["save"].collidepoint(pos):
            return self._try_save()
        if self.buttons["clear"].collidepoint(pos):
            self.path.clear()
            self.error_message = ""
            return None
        if self.buttons["back"].collidepoint(pos):
            return GameState.MAP_SELECTION

        # Check name input
        if self.name_input_rect.collidepoint(pos):
            self.name_input_active = True
            return None

        # Click grid cell
        cell = self._cell_from_mouse(pos)
        if cell and pos[0] < self.GRID_WIDTH:
            return self._add_path_cell(cell)

        return None

    def _cell_from_mouse(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert mouse position to grid cell (col, row). Returns None if outside grid."""
        if pos[0] < 0 or pos[0] >= self.GRID_WIDTH or pos[1] < 0 or pos[1] >= self.GRID_HEIGHT:
            return None
        col = pos[0] // self.CELL_SIZE
        row = pos[1] // self.CELL_SIZE
        return (col, row)

    def _add_path_cell(self, cell: Tuple[int, int]) -> Optional[GameState]:
        """Add cell to path if valid."""
        if not self.path:
            # First cell
            self.path.append(cell)
            self.error_message = ""
        elif self._is_adjacent(self.path[-1], cell):
            if cell not in self.path:  # No reversing
                self.path.append(cell)
                self.error_message = ""
            else:
                self.error_message = "Already in path"
                self.error_frame = 60
        else:
            self.error_message = "Must connect to last cell"
            self.error_frame = 60

        return None

    def _is_adjacent(self, a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        """Check if two cells are adjacent (4-directional, not diagonal)."""
        col1, row1 = a
        col2, row2 = b
        dx = abs(col1 - col2)
        dy = abs(row1 - row2)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def _try_save(self) -> Optional[GameState]:
        """Validate and save map."""
        if not self.name_input.strip():
            self.error_message = "Enter map name"
            self.error_frame = 60
            return None

        valid, msg = self._validate_path()
        if not valid:
            self.error_message = msg
            self.error_frame = 60
            return None

        # Save map
        path_data = self.path  # List of (col, row) tuples
        try:
            map_id = self.db.save_map(
                name=self.name_input.strip(),
                path=path_data,
                obstacles=[],
                width=self.GRID_COLS,
                height=self.GRID_ROWS,
                is_builtin=False,
                difficulty=1,
            )

            # Generate and save wave configs
            self.wave_generator.generate_for_map(
                db=self.db,
                map_id=map_id,
                map_name=self.name_input.strip(),
                difficulty=1,
                total_waves=5,
            )

            return GameState.MAP_SELECTION

        except Exception as e:
            self.error_message = f"Save failed: {str(e)[:30]}"
            self.error_frame = 120
            return None

    def _validate_path(self) -> Tuple[bool, str]:
        """Validate path. Returns (valid, error_message)."""
        if len(self.path) < self.MIN_PATH_LENGTH:
            return False, f"Path too short ({len(self.path)}/{self.MIN_PATH_LENGTH})"

        # Check connectivity (already enforced during drawing, but double-check)
        for i in range(1, len(self.path)):
            if not self._is_adjacent(self.path[i - 1], self.path[i]):
                return False, "Path has gaps"

        return True, ""

    def update(self):
        """Update state (e.g., error message timeout)."""
        if self.error_frame > 0:
            self.error_frame -= 1
        else:
            self.error_message = ""

    def draw(self, win: pygame.Surface):
        """Draw editor screen."""
        # Clear
        win.fill(self.COLOR_BG)

        # Draw grid
        self._draw_grid(win)

        # Draw path
        self._draw_path(win)

        # Draw panel
        self._draw_panel(win)

    def _draw_grid(self, win: pygame.Surface):
        """Draw grid background."""
        # Fill grass
        pygame.draw.rect(win, self.COLOR_GRASS, (0, 0, self.GRID_WIDTH, self.GRID_HEIGHT))

        # Grid lines
        for col in range(self.GRID_COLS + 1):
            x = col * self.CELL_SIZE
            pygame.draw.line(win, self.COLOR_GRID_LINE, (x, 0), (x, self.GRID_HEIGHT), 1)
        for row in range(self.GRID_ROWS + 1):
            y = row * self.CELL_SIZE
            pygame.draw.line(win, self.COLOR_GRID_LINE, (0, y), (self.GRID_WIDTH, y), 1)

        # Highlight hovered cell
        if self.hovered_cell and self.hovered_cell[0] < self.GRID_WIDTH // self.CELL_SIZE:
            col, row = self.hovered_cell
            rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(win, (255, 255, 0), rect, 2)

    def _draw_path(self, win: pygame.Surface):
        """Draw current path."""
        if not self.path:
            return

        # Draw all path cells
        for col, row in self.path:
            rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(win, self.COLOR_PATH, rect)

        # Draw path line connecting cells
        if len(self.path) > 1:
            points = [
                (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE // 2)
                for col, row in self.path
            ]
            pygame.draw.lines(win, (200, 200, 0), points, 3)

        # Draw start marker (green)
        if self.path:
            col, row = self.path[0]
            rect = pygame.Rect(col * self.CELL_SIZE + 2, row * self.CELL_SIZE + 2, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
            pygame.draw.rect(win, (0, 255, 0), rect, 2)

        # Draw end marker (red)
        if len(self.path) > 1:
            col, row = self.path[-1]
            rect = pygame.Rect(col * self.CELL_SIZE + 2, row * self.CELL_SIZE + 2, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
            pygame.draw.rect(win, (255, 0, 0), rect, 2)

    def _draw_panel(self, win: pygame.Surface):
        """Draw right control panel."""
        panel_x = self.GRID_WIDTH
        panel_rect = pygame.Rect(panel_x, 0, self.PANEL_WIDTH, self.screen_height)
        pygame.draw.rect(win, self.COLOR_PANEL_BG, panel_rect)

        font_small = pygame.font.Font(None, 20)
        font_label = pygame.font.Font(None, 16)

        y = 10
        label = font_label.render("Map Name:", True, self.COLOR_TEXT)
        win.blit(label, (panel_x + 10, y))
        y += 25

        # Name input
        input_color = (100, 100, 255) if self.name_input_active else (100, 100, 100)
        pygame.draw.rect(win, input_color, self.name_input_rect, 2)
        name_display = self.name_input if self.name_input else "|"
        text = font_small.render(name_display[-20:], True, self.COLOR_TEXT)
        win.blit(text, (self.name_input_rect.x + 5, self.name_input_rect.y + 5))

        y = 100
        path_label = font_label.render(f"Path: {len(self.path)} cells", True, self.COLOR_TEXT)
        win.blit(path_label, (panel_x + 10, y))

        # Draw buttons
        self._draw_button(win, "save", "Save Map")
        self._draw_button(win, "clear", "Clear")
        self._draw_button(win, "back", "Back")

        # Error message
        if self.error_message:
            error_text = font_small.render(self.error_message, True, self.COLOR_ERROR)
            win.blit(error_text, (panel_x + 10, self.screen_height - 60))

    def _draw_button(self, win: pygame.Surface, key: str, label: str):
        """Draw button."""
        rect = self.buttons[key]
        hovered = rect.collidepoint(self.mouse_pos)
        color = self.COLOR_BUTTON_HOVER if hovered else self.COLOR_BUTTON
        pygame.draw.rect(win, color, rect)
        pygame.draw.rect(win, self.COLOR_TEXT, rect, 2)

        font = pygame.font.Font(None, 18)
        text = font.render(label, True, self.COLOR_TEXT)
        text_rect = text.get_rect(center=rect.center)
        win.blit(text, text_rect)
