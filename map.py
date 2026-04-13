from typing import List, Tuple, Optional

import pygame

from enemy import Enemy, Soldier, Tank, Scout, Boss
from src.difficulty import DifficultyManager
from src.direction import Direction
from src.point import Point
from tower import Tower, BasicTower, SniperTower, MachineGunTower, SplashTower, TOWER_TYPES
from ui.tower_selector import TowerSelector


def get_wave_difficulty_multiplier(wave_number: int) -> float:
    """Return difficulty multiplier for given wave (1-indexed).

    Progressive difficulty scaling:
    - Wave 1: 1.0x (baseline)
    - Wave 2: 1.25x (+25%)
    - Wave 3: 1.30x (+30%)
    - Wave 4: 1.35x (+35%)
    - Wave 5: 1.40x (+40%)
    """
    multipliers = {
        1: 1.0,
        2: 1.25,
        3: 1.30,
        4: 1.35,
        5: 1.40,
    }
    return multipliers.get(wave_number, 1.0)


class Bullet:
    def __init__(self, start_x: int, start_y: int, target: Enemy, damage: float,
                 color: Tuple[int, int, int] = (0, 0, 0), speed: int = 10):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.target = target
        self.damage = damage
        self.color = color
        self.speed = speed
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

    @classmethod
    def load_from_path_data(cls, path_data: list) -> "Map":
        """Create a Map with path loaded from DB path_data (list of [col, row] pairs)."""
        instance = cls.__new__(cls)
        instance.size = (40, 30)
        instance.path = []
        instance.grid = []
        instance.is_field_pressed = False
        instance.field_pressed = Filed(-1, -1, 20, 20, (200, 200, 200))

        for col in range(instance.size[0]):
            instance.grid.append([])
            for row in range(instance.size[1]):
                instance.grid[col].append(Filed(col * 20, row * 20, 20, 20, (255, 255, 255)))

        for col, row in path_data:
            instance.path.append(PathField(col * 20, row * 20, 20, 20))

        return instance

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
    wave_number: int

    def __init__(self, map: Map, towers: List[Tower], round_ref: "Round", wave_number: int = 1):
        self.map = map
        self.enemies = []
        self.towers = towers
        self.round_ref = round_ref
        self.bullets = []
        self.spawn_timer = 0
        self.spawn_interval = 1000  # milliseconds between spawns
        self.enemies_spawned = 0
        self.total_enemies = 10
        self.enemies_escaped = 0
        self.wave_number = wave_number
        # Difficulty multipliers (set by DifficultyManager via Round.__init__)
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
        """Build ordered list of enemy types based on composition."""
        queue = []
        order = ['boss', 'tank', 'scout', 'soldier']
        for enemy_type in order:
            count = self.enemy_composition.get(enemy_type, 0)
            queue.extend([enemy_type] * count)
        # Fill remainder with soldiers if composition doesn't cover total
        while len(queue) < self.total_enemies:
            queue.append('soldier')
        return queue[:self.total_enemies]

    def _spawn_enemy(self) -> Enemy:
        """Create the next enemy using wave's difficulty multipliers and composition."""
        # Build queue on first spawn
        if not hasattr(self, '_spawn_queue') or self._spawn_queue is None:
            self._spawn_queue = self._build_spawn_queue()

        idx = self.enemies_spawned
        enemy_type = self._spawn_queue[idx] if idx < len(self._spawn_queue) else 'soldier'

        spawn_x = self.map.path[0].pos.x - (20 * (idx + 2))
        spawn_y = self.map.path[0].pos.y
        pos = Point(spawn_x, spawn_y)

        if enemy_type == 'tank':
            enemy = Tank(
                pos,
                life_point=Tank.BASE_HP * self.hp_multiplier,
                speed=Tank.BASE_SPEED * self.speed_multiplier,
                bounty=int(Tank.BASE_BOUNTY * self.bounty_multiplier),
            )
        elif enemy_type == 'scout':
            enemy = Scout(
                pos,
                life_point=Scout.BASE_HP * self.hp_multiplier,
                speed=Scout.BASE_SPEED * self.speed_multiplier,
                bounty=int(Scout.BASE_BOUNTY * self.bounty_multiplier),
            )
        elif enemy_type == 'boss':
            enemy = Boss(
                pos,
                life_point=Boss.BASE_HP * self.hp_multiplier,
                speed=Boss.BASE_SPEED * self.speed_multiplier,
                bounty=int(Boss.BASE_BOUNTY * self.bounty_multiplier),
            )
        else:
            enemy = Soldier(
                pos,
                life_point=Soldier.BASE_HP * self.hp_multiplier,
                speed=Soldier.BASE_SPEED * self.speed_multiplier,
                bounty=int(Soldier.BASE_BOUNTY * self.bounty_multiplier),
            )

        # Initialize slow effect attributes
        enemy.slow_factor = 1.0
        enemy.slow_timer = 0

        return enemy

    def update(self, dt: int, *args, **kwargs):
        self.map.update(*args, **kwargs)

        # Spawn enemies over time (spawn_interval is in milliseconds)
        if self.enemies_spawned < self.total_enemies:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                enemy = self._spawn_enemy()
                self.enemies.append(enemy)
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
            # Apply slow effect duration
            if hasattr(enemy, 'slow_timer') and enemy.slow_timer > 0:
                enemy.slow_timer -= dt
                if enemy.slow_timer <= 0:
                    enemy.slow_factor = 1.0
                    enemy.slow_timer = 0

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
                # Apply slow_factor to movement speed
                slow_factor = getattr(enemy, 'slow_factor', 1.0)
                enemy.pos.x += (dx / distance) * enemy.speed * slow_factor
                enemy.pos.y += (dy / distance) * enemy.speed * slow_factor

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
    round_state_id: Optional[int]
    round_config_id: Optional[int]
    start_time: float
    time_elapsed: int

    def __init__(self, round_state_id: Optional[int] = None, round_config_id: Optional[int] = None,
                 map_instance: Optional[Map] = None, starting_lives: int = 10,
                 starting_money: int = 450, return_to_menu=None,
                 difficulty: str = 'normal', total_waves: int = 10):
        self.map = map_instance if map_instance is not None else Map()
        self.towers = []
        self.heart = starting_lives
        self.money = starting_money
        self.score = 0
        self.current_wave = 0
        self.waves = []
        self.game_over = False
        self.victory = False
        self.total_waves = total_waves
        self.ui_panel_width = 180
        self.restart_button_rect = None
        self.menu_button_rect = None
        self.round_state_id = round_state_id
        self.round_config_id = round_config_id
        self.start_time = pygame.time.get_ticks() / 1000
        self.time_elapsed = 0
        self.return_to_menu = return_to_menu  # callable: () -> None

        # Tower type selection (index into TOWER_TYPES list)
        self.selected_tower_idx = 0  # default: BasicTower
        self.tower_cost = TOWER_TYPES[self.selected_tower_idx]['cost']

        # Tower selector UI
        panel_x = self.map.size[0] * 20
        panel_y = 0
        panel_width = self.ui_panel_width
        panel_height = 600  # Standard window height
        self.tower_selector = TowerSelector(panel_x, panel_y, panel_width, panel_height)

        # Dynamic difficulty manager
        self.difficulty_manager = DifficultyManager(difficulty=difficulty, total_waves=total_waves)
        self._prev_wave_lives = starting_lives
        self._prev_wave_escaped = 0

        # Create waves using dynamic difficulty
        for i in range(self.total_waves):
            wave_number = i + 1
            wave_cfg = self.difficulty_manager.get_wave_config(wave_number)
            wave = Wave(self.map, self.towers, self, wave_number=wave_number)
            wave.total_enemies = wave_cfg.total_enemies
            wave.spawn_interval = wave_cfg.spawn_interval
            wave.hp_multiplier = wave_cfg.enemy_hp_multiplier
            wave.speed_multiplier = wave_cfg.enemy_speed_multiplier
            wave.bounty_multiplier = wave_cfg.bounty_multiplier
            wave.enemy_composition = wave_cfg.enemy_composition
            self.waves.append(wave)

        self.start_wave()

    @classmethod
    def load_from_db(cls, db, round_state_id: int) -> Optional["Round"]:
        """Load a round from database"""
        state = db.get_round_state(round_state_id)
        if not state:
            return None

        round_config_id = state['round_config_id']
        config = db.get_round_config(round_config_id)
        if not config:
            return None

        # Get map
        map_data = db.get_map(config['map_id'])
        if not map_data:
            return None

        # Create round with saved state
        round_instance = cls.__new__(cls)
        round_instance.map = Map()
        round_instance.map.path = []
        for px, py in map_data['path']:
            round_instance.map.path.append(PathField(px * 20, py * 20, 20, 20))
        round_instance.towers = []
        round_instance.heart = state['current_lives']
        round_instance.money = state['current_money']
        round_instance.score = state['current_score']
        round_instance.current_wave = state['current_wave']
        round_instance.waves = []
        round_instance.game_over = False
        round_instance.victory = False
        round_instance.total_waves = config['total_waves']
        round_instance.tower_cost = config['tower_cost']
        round_instance.ui_panel_width = 180
        round_instance.restart_button_rect = None
        round_instance.round_state_id = round_state_id
        round_instance.round_config_id = round_config_id
        round_instance.start_time = pygame.time.get_ticks() / 1000 - state['time_elapsed_seconds']
        round_instance.time_elapsed = state['time_elapsed_seconds']

        # Restore towers
        for tower_data in state['towers_placed']:
            tower = BasicTower(Point(tower_data['y'] * 20, tower_data['x'] * 20))
            tower.level = tower_data.get('level', 1)
            round_instance.towers.append(tower)

        # Create waves
        for i in range(round_instance.total_waves):
            wave_number = i + 1
            wave = Wave(round_instance.map, round_instance.towers, round_instance, wave_number=wave_number)
            wave.total_enemies = 5 + (i * 3)
            wave.spawn_interval = max(30, 60 - (i * 5))
            wave.enemies_spawned = 0 if i > round_instance.current_wave else (5 + (i * 3) if i < round_instance.current_wave else 0)
            if i < round_instance.current_wave:
                wave.enemies = []
            round_instance.waves.append(wave)

        return round_instance

    def save_to_db(self, db) -> int:
        """Save current round state to database"""
        self.time_elapsed = int(pygame.time.get_ticks() / 1000 - self.start_time)

        # Convert towers to serializable format
        towers_data = []
        for tower in self.towers:
            towers_data.append({
                'x': tower.pos.x // 20,
                'y': tower.pos.y // 20,
                'type': 'basic',
                'level': tower.level
            })

        # Count enemies killed
        enemies_killed = sum(wave.enemies_spawned - len(wave.enemies) for wave in self.waves)

        if self.round_state_id is None:
            # New save
            self.round_state_id = db.save_round_state(
                self.round_config_id or 1,
                self.current_wave,
                self.money,
                self.heart,
                self.score,
                towers_data,
                enemies_killed,
                self.time_elapsed
            )
        else:
            # Update existing save
            db.update_round_state(
                self.round_state_id,
                current_wave=self.current_wave,
                current_money=self.money,
                current_lives=self.heart,
                current_score=self.score,
                towers_placed=towers_data,
                enemies_killed_total=enemies_killed,
                time_elapsed_seconds=self.time_elapsed
            )

        return self.round_state_id

    def record_tower_placement(self, db, tower_type: str, grid_x: int, grid_y: int, cost: int):
        """Record tower placement in database"""
        if self.round_state_id is not None:
            db.record_tower_placement(self.round_state_id, tower_type, grid_x, grid_y, cost)

    def complete_wave_in_db(self, db, wave_number: int, enemies_killed: int,
                            time_taken: int, money_earned: int, damage_taken: int):
        """Record wave completion in database"""
        if self.round_state_id is not None:
            db.complete_wave(self.round_state_id, wave_number, enemies_killed,
                           time_taken, money_earned, damage_taken)
            db.start_wave_tracking(self.round_state_id, wave_number + 1)

    def finalize_round_in_db(self, db, victory: bool):
        """Mark round as complete in database and save to game_stats"""
        if self.round_state_id is not None:
            db.complete_round_state(self.round_state_id, victory)
            db.save_game_result(
                db.get_round_config(self.round_config_id)['map_id'] if self.round_config_id else 1,
                self.round_config_id or 1,
                self.score,
                self.current_wave + 1 if victory else self.current_wave,
                victory,
                enemies_killed=sum(wave.enemies_spawned - len(wave.enemies) for wave in self.waves),
                towers_built=len(self.towers),
                play_time=self.time_elapsed
            )

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
            finished_wave = self.waves[self.current_wave]
            lives_lost = self._prev_wave_lives - self.heart
            self.difficulty_manager.record_wave_result(
                lives_lost=lives_lost,
                enemies_escaped=finished_wave.enemies_escaped,
                total_enemies=finished_wave.total_enemies,
            )
            self._prev_wave_lives = self.heart

            self.current_wave += 1
            if self.current_wave >= self.total_waves:
                self.victory = True
                self.current_wave = self.total_waves - 1  # Keep index in bounds

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

        # Draw tower selector UI
        self.tower_selector.draw(win)

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
        button_rect = pygame.Rect(win.get_width() // 2 - 110, win.get_height() // 2 + 50, 200, 50)
        pygame.draw.rect(win, (50, 50, 50), button_rect)
        pygame.draw.rect(win, (100, 100, 100), button_rect, 3)
        pygame.draw.rect(win, (70, 70, 70), button_rect, 1)

        restart_text = button_font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=button_rect.center)
        win.blit(restart_text, restart_rect)

        # Main Menu button
        menu_button_rect = pygame.Rect(win.get_width() // 2 + 120, win.get_height() // 2 + 50, 200, 50)
        pygame.draw.rect(win, (40, 40, 80), menu_button_rect)
        pygame.draw.rect(win, (80, 80, 160), menu_button_rect, 3)

        menu_text = button_font.render("Main Menu", True, (200, 200, 255))
        menu_rect = menu_text.get_rect(center=menu_button_rect.center)
        win.blit(menu_text, menu_rect)

        # Store button rects for collision detection
        self.restart_button_rect = button_rect
        self.menu_button_rect = menu_button_rect

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
        button_rect = pygame.Rect(win.get_width() // 2 - 110, win.get_height() // 2 + 50, 200, 50)
        pygame.draw.rect(win, (50, 50, 50), button_rect)
        pygame.draw.rect(win, (100, 100, 100), button_rect, 3)
        pygame.draw.rect(win, (70, 70, 70), button_rect, 1)

        restart_text = button_font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=button_rect.center)
        win.blit(restart_text, restart_rect)

        # Main Menu button
        menu_button_rect = pygame.Rect(win.get_width() // 2 + 120, win.get_height() // 2 + 50, 200, 50)
        pygame.draw.rect(win, (40, 40, 80), menu_button_rect)
        pygame.draw.rect(win, (80, 80, 160), menu_button_rect, 3)

        menu_text = button_font.render("Main Menu", True, (200, 200, 255))
        menu_rect = menu_text.get_rect(center=menu_button_rect.center)
        win.blit(menu_text, menu_rect)

        # Store button rects for collision detection
        self.restart_button_rect = button_rect
        self.menu_button_rect = menu_button_rect

    def handle_event(self, event: pygame.event.Event):
        self.waves[self.current_wave].handle_event(event)

        # End-screen button clicks (game over or victory)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.game_over or self.victory:
                mouse_pos = pygame.mouse.get_pos()

                # Restart button: re-initialise this round in place
                if self.restart_button_rect and self.restart_button_rect.collidepoint(mouse_pos):
                    self.__init__(return_to_menu=self.return_to_menu)
                    return

                # Main Menu button: notify the Game to return to menu
                if (self.menu_button_rect and self.menu_button_rect.collidepoint(mouse_pos)
                        and self.return_to_menu is not None):
                    self.return_to_menu()
                    return

        # Tower selector click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left click
            if self.tower_selector.handle_event(event):
                # Tower was selected, update our state
                self.selected_tower_idx = self.tower_selector.get_selected_tower_index()
                self.tower_cost = self.tower_selector.get_selected_tower_cost()
                return  # Don't try to place a tower if we just selected one

        # Tower placement
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left click
            if not self.game_over and not self.victory:
                self.try_place_tower()

    def try_place_tower(self, db=None):
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

        # Place the selected tower type
        tower_info = TOWER_TYPES[self.selected_tower_idx]
        tower_cls = tower_info['class']
        self.towers.append(tower_cls(Point(grid_y, grid_x)))
        self.money -= self.tower_cost

        # Record in database if db is available
        if db is not None and self.round_state_id is not None:
            self.record_tower_placement(db, tower_info['name'].lower(),
                                        grid_x // 20, grid_y // 20, self.tower_cost)
