"""Tower Selector UI - allows players to select which tower to build."""

import pygame
from typing import Optional, Callable
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
        self.scroll_offset = 0  # For scrolling if too many towers

        self._build_tower_buttons()

    def _build_tower_buttons(self):
        """Create rectangular areas for each tower in the selector."""
        self.tower_buttons = []

        # Tower selector starts below the title and stats section
        # Assume 380px is used for title/stats, leaving space for towers
        towers_start_y = self.panel_y + 380
        tower_button_height = 60
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
        small_font = pygame.font.Font(None, 20)
        medium_font = pygame.font.Font(None, 24)

        # Draw tower selection header
        header_y = self.panel_y + 380
        header_text = medium_font.render("SELECT TOWER", True, (255, 215, 0))
        header_rect = header_text.get_rect(centerx=self.panel_x + self.panel_width // 2, top=header_y)
        win.blit(header_text, header_rect)

        # Draw divider line
        divider_y = header_y + 35
        pygame.draw.line(win, (80, 80, 100),
                        (self.panel_x + 10, divider_y),
                        (self.panel_x + self.panel_width - 10, divider_y), 1)

        # Draw each tower button
        for button_info in self.tower_buttons:
            self._draw_tower_button(win, button_info, small_font, medium_font)

    def _draw_tower_button(self, win: pygame.Surface, button_info: dict,
                          small_font: pygame.font.Font, medium_font: pygame.font.Font):
        """Draw a single tower selection button."""
        rect = button_info['rect']
        tower_info = button_info['tower_info']
        index = button_info['index']

        is_selected = (index == self.selected_index)

        # Button background - highlight if selected
        if is_selected:
            button_color = (100, 100, 150)  # Lighter blue for selected
            border_color = (200, 200, 255)  # Bright blue border
            border_width = 3
        else:
            button_color = (50, 50, 70)  # Dark blue for unselected
            border_color = (100, 100, 150)  # Muted border
            border_width = 1

        pygame.draw.rect(win, button_color, rect)
        pygame.draw.rect(win, border_color, rect, border_width)

        # Tower icon (small colored circle representing the tower)
        icon_x = rect.x + 15
        icon_y = rect.y + rect.height // 2
        tower_cls = tower_info['class']
        # Get the color from a temporary instance
        temp_tower = tower_cls.__new__(tower_cls)
        tower_color = getattr(temp_tower, 'color', (70, 130, 180))
        pygame.draw.circle(win, tower_color, (icon_x, icon_y), 8)
        pygame.draw.circle(win, (0, 0, 0), (icon_x, icon_y), 8, 1)

        # Tower name
        name_text = medium_font.render(tower_info['name'], True, (255, 255, 255))
        win.blit(name_text, (icon_x + 20, rect.y + 8))

        # Tower cost
        cost_color = (255, 215, 0)  # Gold
        cost_text = small_font.render(f"${tower_info['cost']}", True, cost_color)
        win.blit(cost_text, (icon_x + 20, rect.y + 30))

        # Tower stats (range and damage if available)
        tower_cls = tower_info['class']
        try:
            # Create temporary instance to get stats
            from src.point import Point
            temp = tower_cls(Point(0, 0))
            range_val = getattr(temp, 'range', 0)
            power_val = getattr(temp, 'power', 0)

            stats_text = f"Range: {range_val} | DMG: {power_val}"
            stats_rendered = small_font.render(stats_text, True, (180, 180, 200))
            win.blit(stats_rendered, (rect.right - 160, rect.y + 30))
        except:
            pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse clicks on tower buttons.

        Returns:
            True if a tower was selected, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

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
