from typing import List, Tuple

import pygame

from enemy import Enemy, Soldier
from src.direction import Direction
from src.point import Point
from tower import Tower, BasicTower


class Bullet:
    def __init__(self, start_x: int, start_y: int, target: Enemy, damage: float, color: Tuple[int, int, int] = (0, 0, 0)):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.target = target
        self.damage = damage
        self.color = color
        self.speed = 10
        self.active = True

    def update(self) -> bool:
        """Update bullet position. Returns True if bullet hit target."""
        if not self.target or not self.active:
            return False

        target_x = self.target.pos.x + (self.target.size[0] // 2)
        target_y = self.target.pos.y + (self.target.size[1] // 2)

        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance < self.speed:
            self.x = target_x
            self.y = target_y
            self.active = False
            return True

        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        return False

    def draw(self, win: pygame.Surface):
        if self.active:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 4)


class Filed:
    pos: pygame.Rect
    color: Tuple[int, int, int]

    def __init__(self, col, row, width, height, color=(34, 139, 34)):  # Forest green grass
        self.pos = pygame.Rect(col, row, width, height)
        self.color = color


class PathField(Filed):

    def __init__(self, col, row, width, height, color=(105, 105, 105)):  # Gray road
        super().__init__(col, row, width, height, color)


class Map(object):
    size: Tuple[int, int]
    path: List[PathField]
    grid: List[List[Filed]]
    towers: List[Tower]
    enemies: List[Enemy]
    field_pressed: Filed
    is_field_pressed: bool

    def __init__(self):
        self.size = (40, 30)
        self.path = []
        self.grid = []
        self.is_field_pressed = False
        self.field_pressed = Filed(-1,-1,20,20, (200,200,200))

        for col in range(self.size[0]):
            self.grid.append([])
            for row in range(self.size[1]):
                self.grid[col].append(Filed(col * 20, row * 20, 20, 20, (255, 255, 255)))

        for i in range(self.size[0] // 2):
            self.path.append(PathField(i * 20, (self.size[1] // 2) * 20, 20, 20))

        for i in range(self.size[1] // 2, self.size[1]):
            self.path.append(PathField(self.size[0] // 2 * 20, i * 20, 20, 20))

    def draw(self, win: pygame.Surface):
        self._draw_grid(win)
        self._draw_path(win)
        self._draw_parsed_field(win)

    def _draw_grid(self, win: pygame.Surface):
        # Draw grass background for entire map
        grass_color = (34, 139, 34)  # Forest green
        for row in self.grid:
            for point in row:
                pygame.draw.rect(win, grass_color, point.pos)

        # Draw grid lines for visual clarity
        grid_line_color = (25, 120, 25)  # Darker green
        for col in range(0, self.size[0] * 20, 20):
            pygame.draw.line(win, grid_line_color, (col, 0), (col, self.size[1] * 20), 1)
        for row in range(0, self.size[1] * 20, 20):
            pygame.draw.line(win, grid_line_color, (0, row), (self.size[0] * 20, row), 1)

    def _draw_path(self, win: pygame.Surface):
        # First pass: draw all road tiles
        for point in self.path:
            # Draw road base
            pygame.draw.rect(win, point.color, point.pos)
            # Add road border
            border_color = (70, 70, 70)
            pygame.draw.rect(win, border_color, point.pos, 2)

        # Second pass: draw center line markings
        for i, point in enumerate(self.path):
            center_x = point.pos.x + 10
            center_y = point.pos.y + 10

            # Draw dashed center line
            if i < len(self.path) - 1:
                next_point = self.path[i + 1]
                next_center_x = next_point.pos.x + 10
                next_center_y = next_point.pos.y + 10

                # Determine direction
                if next_center_x > center_x:  # Moving right
                    pygame.draw.line(win, (200, 200, 50), (point.pos.x + 5, center_y), (point.pos.x + 15, center_y), 2)
                elif next_center_x < center_x:  # Moving left
                    pygame.draw.line(win, (200, 200, 50), (point.pos.x + 5, center_y), (point.pos.x + 15, center_y), 2)
                elif next_center_y > center_y:  # Moving down
                    pygame.draw.line(win, (200, 200, 50), (center_x, point.pos.y + 5), (center_x, point.pos.y + 15), 2)
                elif next_center_y < center_y:  # Moving up
                    pygame.draw.line(win, (200, 200, 50), (center_x, point.pos.y + 5), (center_x, point.pos.y + 15), 2)

        # Draw start and end markers
        if self.path:
            start = self.path[0]
            end = self.path[-1]

            # Start flag (green)
            pygame.draw.rect(win, (0, 150, 0), (start.pos.x + 2, start.pos.y + 2, 16, 16))
            pygame.draw.rect(win, (0, 100, 0), (start.pos.x + 2, start.pos.y + 2, 16, 16), 2)
            # Start arrow
            pygame.draw.polygon(win, (100, 255, 100), [
                (start.pos.x + 10, start.pos.y + 4),
                (start.pos.x + 6, start.pos.y + 14),
                (start.pos.x + 10, start.pos.y + 10),
                (start.pos.x + 14, start.pos.y + 14)
            ])

            # End marker (red X)
            pygame.draw.rect(win, (150, 0, 0), (end.pos.x + 2, end.pos.y + 2, 16, 16))
            pygame.draw.rect(win, (100, 0, 0), (end.pos.x + 2, end.pos.y + 2, 16, 16), 2)
            pygame.draw.line(win, (255, 50, 50), (end.pos.x + 4, end.pos.y + 4), (end.pos.x + 16, end.pos.y + 16), 3)
            pygame.draw.line(win, (255, 50, 50), (end.pos.x + 16, end.pos.y + 4), (end.pos.x + 4, end.pos.y + 16), 3)

    def _draw_parsed_field(self, win: pygame.Surface) -> None:
        if self.is_field_pressed:
            pygame.draw.rect(win, self.field_pressed.color, self.field_pressed.pos)

    def update(self, *args, **kwargs):
        ...

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            nx = mouse_pos[0] // 20 * 20
            ny = mouse_pos[1] // 20 * 20

            if not self.is_field_pressed:
                self.is_field_pressed = True
                self.field_pressed.pos.x = nx
                self.field_pressed.pos.y = ny
            elif self.field_pressed.pos.x == nx and self.field_pressed.pos.y == ny:
                self.is_field_pressed = False
                self.field_pressed.pos.x = -1
                self.field_pressed.pos.y = -1
            else:
                self.field_pressed.pos.x = nx
                self.field_pressed.pos.y = ny


class Wave:
    map: Map
    enemies: List[Enemy]
    towers: List[Tower]
    bullets: List[Bullet]
    round_ref: "Round"

    def __init__(self, map: Map, towers: List[Tower], round_ref: "Round"):
        self.map = map
        self.enemies = []
        self.towers = towers
        self.round_ref = round_ref
        self.bullets = []
        self.spawn_timer = 0
        self.spawn_interval = 60  # frames between spawns
        self.enemies_spawned = 0
        self.total_enemies = 10

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

    def update(self, dt: int, *args, **kwargs):
        self.map.update(*args, **kwargs)

        # Spawn enemies over time
        if self.enemies_spawned < self.total_enemies:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                # Spawn enemies to the left of the first path position
                spawn_x = self.map.path[0].pos.x - (20 * (self.enemies_spawned + 2))
                spawn_y = self.map.path[0].pos.y
                self.enemies.append(Soldier(Point(spawn_x, spawn_y)))
                self.enemies_spawned += 1

        for tower in self.towers:
            tower.update(dt, enemies=self.enemies, bullets=self.bullets, *args, **kwargs)

        # Update bullets
        for bullet in self.bullets[:]:
            if bullet.update():
                # Bullet hit target
                if bullet.target and bullet.target.life_point > 0:
                    bullet.target.life_point -= bullet.damage
            else:
                # Remove inactive bullets
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
                    continue

            if distance > 0:
                enemy.pos.x += (dx / distance) * enemy.speed
                enemy.pos.y += (dy / distance) * enemy.speed

    def handle_event(self, event: pygame.event.Event):
        self.map.handle_event(event)

    def is_complete(self) -> bool:
        return self.enemies_spawned >= self.total_enemies and len(self.enemies) == 0


class Round:
    map: Map
    waves: List[Wave]
    towers: List[Tower]
    current_wave: int
    heart: int
    money: int
    score: int
    game_over: bool
    victory: bool
    total_waves: int
    ui_panel_width: int

    def __init__(self):
        self.map = Map()
        self.towers = []
        self.heart = 10
        self.money = 450
        self.score = 0
        self.current_wave = 0
        self.waves = []
        self.game_over = False
        self.victory = False
        self.total_waves = 5
        self.tower_cost = 100
        self.ui_panel_width = 180  # Width of the UI panel on the right
        self.restart_button_rect = None  # Will be set when game over/victory is drawn

        # Create waves
        for i in range(self.total_waves):
            wave = Wave(self.map, self.towers, self)
            wave.total_enemies = 5 + (i * 3)  # Increase enemies per wave
            wave.spawn_interval = max(30, 60 - (i * 5))  # Faster spawns per wave
            self.waves.append(wave)

        # Start first wave
        self.start_wave()

    def start_wave(self):
        if self.current_wave < len(self.waves):
            pass  # Wave already initialized

    def update(self, dt: int, *args, **kwargs):
        if self.game_over or self.victory:
            return

        self.waves[self.current_wave].update(dt, *args, **kwargs)

        # Check for dead enemies and award money
        for enemy in self.waves[self.current_wave].enemies[:]:
            if enemy.life_point <= 0:
                self.waves[self.current_wave].enemies.remove(enemy)
                self.money += enemy.bounty
                self.score += enemy.level * 10

        # Check if wave is complete
        if self.waves[self.current_wave].is_complete():
            self.current_wave += 1
            if self.current_wave >= self.total_waves:
                self.victory = True
                self.current_wave = self.total_waves - 1  # Keep index in bounds
            else:
                # Start next wave after delay
                pass

        # Check game over
        if self.heart <= 0:
            self.game_over = True

    def draw(self, win: pygame.Surface):
        self.waves[self.current_wave].draw(win)
        self._draw_towers(win)
        self._draw_tower_preview(win)  # Draw ghost tower preview
        self._draw_ui(win)
        if self.game_over:
            self._draw_game_over(win)
        elif self.victory:
            self._draw_victory(win)

    def _draw_ui(self, win: pygame.Surface):
        pygame.font.init()
        font = pygame.font.Font(None, 32)
        title_font = pygame.font.Font(None, 40)
        small_font = pygame.font.Font(None, 24)

        # UI panel dimensions
        panel_x = self.map.size[0] * 20
        panel_width = self.ui_panel_width
        panel_height = win.get_height()

        # Draw panel background with gradient effect
        panel_rect = pygame.Rect(panel_x, 0, panel_width, panel_height)
        pygame.draw.rect(win, (40, 40, 50), panel_rect)  # Dark background
        pygame.draw.rect(win, (60, 60, 80), pygame.Rect(panel_x, 0, panel_width - 1, panel_height))  # Slightly lighter fill

        # Panel border
        pygame.draw.line(win, (100, 100, 120), (panel_x, 0), (panel_x, panel_height), 3)
        pygame.draw.line(win, (100, 100, 120), (panel_x + panel_width - 1, 0), (panel_x + panel_width - 1, panel_height), 2)

        # Title
        title_text = title_font.render("TOWER", True, (255, 215, 0))
        title_rect = title_text.get_rect(centerx=panel_x + panel_width // 2, top=20)
        win.blit(title_text, title_rect)

        title_text2 = title_font.render("DEFENSE", True, (255, 215, 0))
        title_rect2 = title_text2.get_rect(centerx=panel_x + panel_width // 2, top=55)
        win.blit(title_text2, title_rect2)

        # Separator line
        pygame.draw.line(win, (80, 80, 100), (panel_x + 10, 95), (panel_x + panel_width - 10, 95), 2)

        # Stats section
        stats_y = 110
        stat_spacing = 55

        # Draw money with icon
        money_icon = pygame.Rect(panel_x + 15, stats_y, 20, 20)
        pygame.draw.circle(win, (255, 215, 0), (panel_x + 25, stats_y + 10), 12)
        pygame.draw.circle(win, (180, 150, 0), (panel_x + 25, stats_y + 10), 12, 2)
        money_text = font.render(f"${self.money}", True, (255, 255, 100))
        win.blit(money_text, (panel_x + 45, stats_y + 2))

        # Draw lives with heart icon
        lives_y = stats_y + stat_spacing
        pygame.draw.polygon(win, (255, 60, 60), [
            (panel_x + 25, lives_y + 8),
            (panel_x + 20, lives_y + 4),
            (panel_x + 20, lives_y),
            (panel_x + 22, lives_y - 3),
            (panel_x + 25, lives_y),
            (panel_x + 28, lives_y - 3),
            (panel_x + 30, lives_y),
            (panel_x + 30, lives_y + 4)
        ])
        pygame.draw.polygon(win, (180, 40, 40), [
            (panel_x + 25, lives_y + 8),
            (panel_x + 20, lives_y + 4),
            (panel_x + 20, lives_y),
            (panel_x + 22, lives_y - 3),
            (panel_x + 25, lives_y),
            (panel_x + 28, lives_y - 3),
            (panel_x + 30, lives_y),
            (panel_x + 30, lives_y + 4)
        ], 2)
        lives_text = font.render(f"x {self.heart}", True, (255, 100, 100))
        win.blit(lives_text, (panel_x + 45, lives_y + 2))

        # Draw wave
        wave_y = lives_y + stat_spacing
        wave_text = font.render(f"Wave: {self.current_wave + 1}/{self.total_waves}", True, (100, 150, 255))
        win.blit(wave_text, (panel_x + 15, wave_y + 2))

        # Draw score
        score_y = wave_y + stat_spacing
        score_text = font.render(f"Score: {self.score}", True, (100, 255, 100))
        win.blit(score_text, (panel_x + 15, score_y + 2))

        # Separator line
        sep_y = score_y + stat_spacing
        pygame.draw.line(win, (80, 80, 100), (panel_x + 10, sep_y), (panel_x + panel_width - 10, sep_y), 2)

        # Tower info
        tower_y = sep_y + 40
        tower_info_text = small_font.render("Tower Cost:", True, (180, 180, 180))
        win.blit(tower_info_text, (panel_x + 15, tower_y))

        tower_cost_text = font.render(f"${self.tower_cost}", True, (255, 200, 100))
        win.blit(tower_cost_text, (panel_x + 15, tower_y + 25))

        # Instructions
        instr_y = tower_y + 70
        instr_text = small_font.render("Click to place", True, (120, 120, 140))
        win.blit(instr_text, (panel_x + 15, instr_y))

        instr_text2 = small_font.render("towers on the", True, (120, 120, 140))
        win.blit(instr_text2, (panel_x + 15, instr_y + 20))

        instr_text3 = small_font.render("grass areas.", True, (120, 120, 140))
        win.blit(instr_text3, (panel_x + 15, instr_y + 40))

        instr_text4 = small_font.render("Press SPACE", True, (120, 120, 140))
        win.blit(instr_text4, (panel_x + 15, instr_y + 70))

        instr_text5 = small_font.render("to pause", True, (120, 120, 140))
        win.blit(instr_text5, (panel_x + 15, instr_y + 90))

    def _draw_towers(self, win: pygame.Surface):
        for tower in self.towers:
            tower.draw(win)

    def _draw_tower_preview(self, win: pygame.Surface):
        """Draw ghost tower preview at mouse position"""
        if self.game_over or self.victory:
            return

        mouse_pos = pygame.mouse.get_pos()
        # Only show preview if mouse is over the map area (not UI panel)
        if mouse_pos[0] >= self.map.size[0] * 20:
            return

        grid_x = (mouse_pos[0] // 20) * 20
        grid_y = (mouse_pos[1] // 20) * 20

        # Check if placement is valid
        can_place = True
        can_afford = self.money >= self.tower_cost

        # Check if on path
        for path_field in self.map.path:
            if path_field.pos.x == grid_x and path_field.pos.y == grid_y:
                can_place = False
                break

        # Check if tower already exists
        for tower in self.towers:
            if tower.pos.x == grid_x and tower.pos.y == grid_y:
                can_place = False
                break

        # Determine preview color
        if can_afford and can_place:
            preview_color = (0, 255, 0, 100)  # Green for valid
            border_color = (0, 200, 0)
        elif not can_afford:
            preview_color = (255, 255, 0, 100)  # Yellow for can't afford
            border_color = (200, 200, 0)
        else:
            preview_color = (255, 0, 0, 100)  # Red for invalid
            border_color = (200, 0, 0)

        # Draw ghost tower
        ghost_rect = pygame.Rect(grid_x + 2, grid_y + 2, 16, 16)
        ghost_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.rect(ghost_surface, preview_color, (2, 2, 16, 16))
        pygame.draw.rect(ghost_surface, border_color, (2, 2, 16, 16), 2)
        pygame.draw.circle(ghost_surface, border_color, (10, 10), 6)
        win.blit(ghost_surface, (grid_x, grid_y))

        # Draw range circle if valid placement
        if can_afford and can_place:
            range_surface = pygame.Surface((140, 140), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (0, 255, 0, 30), (70, 70), 70)
            win.blit(range_surface, (grid_x - 50, grid_y - 50))

    def _draw_game_over(self, win: pygame.Surface):
        # Semi-transparent overlay
        overlay = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        win.blit(overlay, (0, 0))

        pygame.font.init()
        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 36)
        button_font = pygame.font.Font(None, 48)

        # GAME OVER text with glow effect
        for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
            text = font.render("GAME OVER", True, (150, 0, 0))
            text_rect = text.get_rect(center=(win.get_width() // 2 + offset[0], win.get_height() // 2 - 30 + offset[1]))
            win.blit(text, text_rect)

        text = font.render("GAME OVER", True, (255, 50, 50))
        text_rect = text.get_rect(center=(win.get_width() // 2, win.get_height() // 2 - 30))
        win.blit(text, text_rect)

        # Final score
        score_text = small_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(win.get_width() // 2, win.get_height() // 2 + 20))
        win.blit(score_text, score_rect)

        # Restart button
        button_rect = pygame.Rect(win.get_width() // 2 - 100, win.get_height() // 2 + 50, 200, 50)
        pygame.draw.rect(win, (50, 50, 50), button_rect)
        pygame.draw.rect(win, (100, 100, 100), button_rect, 3)
        pygame.draw.rect(win, (70, 70, 70), button_rect, 1)

        restart_text = button_font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=button_rect.center)
        win.blit(restart_text, restart_rect)

        # Store button rect for collision detection
        self.restart_button_rect = button_rect

    def _draw_victory(self, win: pygame.Surface):
        # Semi-transparent overlay
        overlay = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        win.blit(overlay, (0, 0))

        pygame.font.init()
        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 36)
        button_font = pygame.font.Font(None, 48)

        # VICTORY text with glow effect
        for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
            text = font.render("VICTORY!", True, (180, 150, 0))
            text_rect = text.get_rect(center=(win.get_width() // 2 + offset[0], win.get_height() // 2 - 30 + offset[1]))
            win.blit(text, text_rect)

        text = font.render("VICTORY!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(win.get_width() // 2, win.get_height() // 2 - 30))
        win.blit(text, text_rect)

        # Final score
        score_text = small_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(win.get_width() // 2, win.get_height() // 2 + 20))
        win.blit(score_text, score_rect)

        # Restart button
        button_rect = pygame.Rect(win.get_width() // 2 - 100, win.get_height() // 2 + 50, 200, 50)
        pygame.draw.rect(win, (50, 50, 50), button_rect)
        pygame.draw.rect(win, (100, 100, 100), button_rect, 3)
        pygame.draw.rect(win, (70, 70, 70), button_rect, 1)

        restart_text = button_font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=button_rect.center)
        win.blit(restart_text, restart_rect)

        # Store button rect for collision detection
        self.restart_button_rect = button_rect

    def handle_event(self, event: pygame.event.Event):
        self.waves[self.current_wave].handle_event(event)

        # Restart button click (game over or victory)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if (self.game_over or self.victory) and hasattr(self, 'restart_button_rect'):
                if self.restart_button_rect and self.restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # Restart game
                    self.__init__()
                    return

        # Tower placement
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left click
            if not self.game_over and not self.victory:
                self.try_place_tower()

    def try_place_tower(self):
        mouse_pos = pygame.mouse.get_pos()
        grid_x = (mouse_pos[0] // 20) * 20
        grid_y = (mouse_pos[1] // 20) * 20

        # Check if we can afford the tower
        if self.money < self.tower_cost:
            return

        # Check if position is on path
        for path_field in self.map.path:
            if path_field.pos.x == grid_x and path_field.pos.y == grid_y:
                return  # Can't place on path

        # Check if position already has a tower
        for tower in self.towers:
            if tower.pos.x == grid_x and tower.pos.y == grid_y:
                return  # Can't place on existing tower

        # Place the tower
        self.towers.append(BasicTower(Point(grid_y, grid_x)))
        self.money -= self.tower_cost
