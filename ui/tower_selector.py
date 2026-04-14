"""Tower Selector UI - allows players to select which tower to build."""

import pygame
import math
from typing import Dict
from towers import TOWER_TYPES


class TowerSelector:
    """Manages tower selection UI panel during gameplay.

    Displays available towers with their stats and allows clicking to select.
    Currently selected tower is highlighted.
    """

    def __init__(self, panel_x: int, panel_y: int, panel_width: int, panel_height: int):
        """Initialize tower selector.

        Args:
            panel_x: X position of the UI panel
            panel_y: Y position of the UI panel
            panel_width: Width of the UI panel
            panel_height: Height of the UI panel
        """
        self.panel_x = panel_x
        self.panel_y = panel_y
        self.panel_width = panel_width
        self.panel_height = panel_height

        self.selected_index = 0  # Currently selected tower
        self.tower_buttons = []  # List of rects for each tower button
        self.hovered_index = -1  # For hover effects

        self._build_tower_buttons()

    def _build_tower_buttons(self):
        """Create rectangular areas for each tower in the selector."""
        self.tower_buttons = []

        # Tower selector starts below the title and stats section
        # Assume 380px is used for title/stats, leaving space for towers
        towers_start_y = self.panel_y + 380
        tower_button_height = 65
        tower_button_width = self.panel_width - 30

        for i, tower_info in enumerate(TOWER_TYPES):
            button_y = towers_start_y + (i * tower_button_height)

            # Only create buttons that fit in the panel
            if button_y + tower_button_height <= self.panel_y + self.panel_height - 10:
                button_rect = pygame.Rect(
                    self.panel_x + 15,
                    button_y,
                    tower_button_width,
                    tower_button_height
                )
                self.tower_buttons.append({
                    'rect': button_rect,
                    'index': i,
                    'tower_info': tower_info
                })

    def draw(self, win: pygame.Surface):
        """Draw the tower selector UI."""
        pygame.font.init()
        small_font = pygame.font.Font(None, 18)
        medium_font = pygame.font.Font(None, 24)
        bold_font = pygame.font.Font(None, 28)

        # Draw tower selection header with background box
        header_y = self.panel_y + 375
        header_height = 40

        # Header background
        pygame.draw.rect(win, (40, 40, 60),
                        (self.panel_x, header_y, self.panel_width, header_height))
        pygame.draw.rect(win, (100, 100, 150),
                        (self.panel_x, header_y, self.panel_width, header_height), 2)

        # Header text
        header_text = bold_font.render("SELECT TOWER", True, (255, 215, 0))
        header_rect = header_text.get_rect(centerx=self.panel_x + self.panel_width // 2,
                                          centery=header_y + header_height // 2)
        win.blit(header_text, header_rect)

        # Draw each tower button
        for button_info in self.tower_buttons:
            self._draw_tower_button(win, button_info, small_font, medium_font)

    def _draw_tower_button(self, win: pygame.Surface, button_info: Dict,
                          small_font: pygame.font.Font, medium_font: pygame.font.Font):
        """Draw a single tower selection button with shape-based icon."""
        rect = button_info['rect']
        tower_info = button_info['tower_info']
        index = button_info['index']

        is_selected = (index == self.selected_index)
        is_hovered = (index == self.hovered_index)

        # Button background - highlight if selected or hovered
        if is_selected:
            button_color = (80, 100, 150)  # Bright blue for selected
            border_color = (200, 200, 255)  # Bright blue border
            border_width = 3
        elif is_hovered:
            button_color = (70, 80, 120)  # Light blue for hovered
            border_color = (150, 150, 200)  # Light border
            border_width = 2
        else:
            button_color = (45, 45, 65)  # Dark blue for unselected
            border_color = (80, 80, 110)  # Muted border
            border_width = 1

        pygame.draw.rect(win, button_color, rect, border_radius=4)
        pygame.draw.rect(win, border_color, rect, border_width, border_radius=4)

        # Get tower class and properties
        tower_cls = tower_info['class']
        temp_tower = tower_cls.__new__(tower_cls)
        tower_color = getattr(temp_tower, 'color', (70, 130, 180))
        shape_style = getattr(temp_tower, 'shape_style', 'square')

        # Draw tower icon with shape
        icon_x = rect.x + 20
        icon_y = rect.y + rect.height // 2
        self._draw_tower_icon(win, icon_x, icon_y, tower_color, shape_style)

        # Tower name
        name_text = medium_font.render(tower_info['name'], True, (255, 255, 255))
        win.blit(name_text, (icon_x + 30, rect.y + 5))

        # Tower cost and stats on next line
        cost_color = (255, 215, 0) if is_selected else (200, 180, 100)
        cost_text = small_font.render(f"Cost: ${tower_info['cost']}", True, cost_color)
        win.blit(cost_text, (icon_x + 30, rect.y + 28))

        # Tower stats (range and damage)
        tower_cls = tower_info['class']
        try:
            from src.point import Point
            temp = tower_cls(Point(0, 0))
            range_val = getattr(temp, 'range', 0)
            power_val = getattr(temp, 'power', 0)

            stats_text = f"R:{range_val}  P:{power_val}"
            stats_color = (180, 200, 255) if is_selected else (140, 160, 200)
            stats_rendered = small_font.render(stats_text, True, stats_color)
            win.blit(stats_rendered, (icon_x + 30, rect.y + 43))
        except:
            pass

    def _draw_tower_icon(self, win: pygame.Surface, x: int, y: int,
                        color: tuple, shape_style: str):
        """Draw tower icon based on its shape style."""
        radius = 10

        if shape_style == "square":
            # Square - BasicTower
            pygame.draw.rect(win, color, (x - radius, y - radius, radius * 2, radius * 2))
            pygame.draw.rect(win, (255, 255, 255), (x - radius, y - radius, radius * 2, radius * 2), 1)

        elif shape_style == "diamond":
            # Diamond - SniperTower
            points = [
                (x, y - radius),      # top
                (x + radius, y),      # right
                (x, y + radius),      # bottom
                (x - radius, y)       # left
            ]
            pygame.draw.polygon(win, color, points)
            pygame.draw.polygon(win, (255, 255, 255), points, 1)

        elif shape_style == "circle":
            # Circle - SplashTower
            pygame.draw.circle(win, color, (x, y), radius)
            pygame.draw.circle(win, (255, 255, 255), (x, y), radius, 1)

        elif shape_style == "triangle":
            # Triangle pointing up - FreezeTower
            points = [
                (x, y - radius),           # top
                (x + radius, y + radius),  # bottom-right
                (x - radius, y + radius)   # bottom-left
            ]
            pygame.draw.polygon(win, color, points)
            pygame.draw.polygon(win, (255, 255, 255), points, 1)

        elif shape_style == "rectangle":
            # Wide rectangle - MachineGunTower
            pygame.draw.rect(win, color, (x - radius - 3, y - radius // 2, radius * 2 + 6, radius))
            pygame.draw.rect(win, (255, 255, 255), (x - radius - 3, y - radius // 2, radius * 2 + 6, radius), 1)

        elif shape_style == "cross":
            # Cross/Plus - LaserTower
            line_width = 2
            # Horizontal line
            pygame.draw.line(win, color, (x - radius, y), (x + radius, y), line_width)
            # Vertical line
            pygame.draw.line(win, color, (x, y - radius), (x, y + radius), line_width)
            # Corner marks
            offset = radius - 2
            pygame.draw.circle(win, color, (x + offset, y + offset), 2)
            pygame.draw.circle(win, color, (x + offset, y - offset), 2)
            pygame.draw.circle(win, color, (x - offset, y + offset), 2)
            pygame.draw.circle(win, color, (x - offset, y - offset), 2)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events on tower buttons.

        Returns:
            True if a tower was selected, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            # Check for hover
            mouse_pos = event.pos
            self.hovered_index = -1
            for button_info in self.tower_buttons:
                if button_info['rect'].collidepoint(mouse_pos):
                    self.hovered_index = button_info['index']
                    break

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = event.pos
            for button_info in self.tower_buttons:
                if button_info['rect'].collidepoint(mouse_pos):
                    self.selected_index = button_info['index']
                    return True

        return False

    def get_selected_tower_index(self) -> int:
        """Return the index of the currently selected tower."""
        return self.selected_index

    def get_selected_tower_cost(self) -> int:
        """Return the cost of the currently selected tower."""
        return TOWER_TYPES[self.selected_index]['cost']
