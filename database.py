import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class Database:
    """מחלקה לניהול Database של המשחק"""

    def __init__(self, db_path: str = "tower_defense.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._insert_builtin_data()

    def _create_tables(self):
        """יצירת כל הטבלאות אם לא קיימות"""
        self.cursor.executescript('''
            -- טבלת מפות
            CREATE TABLE IF NOT EXISTS maps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                width INTEGER DEFAULT 40,
                height INTEGER DEFAULT 30,
                path_data TEXT NOT NULL,
                obstacles TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_builtin BOOLEAN DEFAULT 0,
                difficulty INTEGER DEFAULT 1
            );

            -- טבלת הגדרות סיבוב
            CREATE TABLE IF NOT EXISTS round_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                map_id INTEGER,
                name TEXT NOT NULL,
                total_waves INTEGER DEFAULT 5,
                starting_money INTEGER DEFAULT 450,
                starting_lives INTEGER DEFAULT 10,
                tower_cost INTEGER DEFAULT 100,
                difficulty_multiplier REAL DEFAULT 1.0,
                FOREIGN KEY (map_id) REFERENCES maps(id)
            );

            -- טבלת הגדרות גלים
            CREATE TABLE IF NOT EXISTS wave_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                round_config_id INTEGER,
                wave_number INTEGER,
                total_enemies INTEGER,
                spawn_interval INTEGER,
                enemy_composition TEXT,
                FOREIGN KEY (round_config_id) REFERENCES round_configs(id)
            );

            -- טבלת סטטיסטיקות משחק
            CREATE TABLE IF NOT EXISTS game_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                map_id INTEGER,
                round_config_id INTEGER,
                score INTEGER DEFAULT 0,
                waves_completed INTEGER DEFAULT 0,
                enemies_killed INTEGER DEFAULT 0,
                towers_built INTEGER DEFAULT 0,
                play_time_seconds INTEGER DEFAULT 0,
                date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                victory BOOLEAN DEFAULT 0,
                FOREIGN KEY (map_id) REFERENCES maps(id),
                FOREIGN KEY (round_config_id) REFERENCES round_configs(id)
            );

            -- טבלת הישגים
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                condition_type TEXT,
                condition_value INTEGER,
                unlocked BOOLEAN DEFAULT 0,
                unlocked_at TIMESTAMP
            );

            -- טבלת הגדרות שחקן
            CREATE TABLE IF NOT EXISTS player_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT NOT NULL UNIQUE,
                setting_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- טבלת מצבי סיבוב (active/paused games)
            CREATE TABLE IF NOT EXISTS round_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                round_config_id INTEGER,
                current_wave INTEGER DEFAULT 0,
                current_money INTEGER,
                current_lives INTEGER,
                current_score INTEGER,
                towers_placed TEXT DEFAULT '[]',
                enemies_killed_total INTEGER DEFAULT 0,
                time_elapsed_seconds INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (round_config_id) REFERENCES round_configs(id)
            );

            -- טבלת התקדמות גלים (wave-by-wave tracking)
            CREATE TABLE IF NOT EXISTS wave_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                round_state_id INTEGER,
                wave_number INTEGER,
                completed BOOLEAN DEFAULT 0,
                enemies_spawned INTEGER DEFAULT 0,
                enemies_killed INTEGER DEFAULT 0,
                time_taken_seconds INTEGER DEFAULT 0,
                money_earned INTEGER DEFAULT 0,
                damage_taken INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                FOREIGN KEY (round_state_id) REFERENCES round_states(id)
            );

            -- טבלת פעולות מגדלים (tower placement/removal history)
            CREATE TABLE IF NOT EXISTS tower_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                round_state_id INTEGER,
                action_type TEXT,
                tower_type TEXT,
                grid_x INTEGER,
                grid_y INTEGER,
                cost INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (round_state_id) REFERENCES round_states(id)
            );
        ''')
        self.conn.commit()

    def _insert_builtin_data(self):
        """הוספת מפות ברירת מחדל אם לא קיימות"""
        # בדיקה אם כבר יש מפות
        self.cursor.execute("SELECT COUNT(*) FROM maps WHERE is_builtin = 1")
        if self.cursor.fetchone()[0] > 0:
            return

        # L-Path (המפה הקיימת)
        l_path = [(i, 15) for i in range(0, 20)] + [(20, j) for j in range(15, 30)]
        self.save_map("Classic L-Path", l_path, width=40, height=30,
                      is_builtin=True, difficulty=1)

        # Z-Path
        z_path = []
        for i in range(0, 40):
            z_path.append((i, 5))
        for i in range(0, 40):
            z_path.append((39 - i, 15))
        for i in range(0, 40):
            z_path.append((i, 25))
        self.save_map("Zigzag Challenge", z_path, width=40, height=30,
                      is_builtin=True, difficulty=2)

        # Spiral
        spiral = []
        cx, cy = 20, 15
        for layer in range(4):
            # ימינה
            for x in range(cx - layer, cx + layer + 1):
                if 0 <= x < 40 and 0 <= cy - layer < 30:
                    spiral.append((x, cy - layer))
            # למטה
            for y in range(cy - layer, cy + layer + 1):
                if 0 <= cx + layer < 40 and 0 <= y < 30:
                    spiral.append((cx + layer, y))
            # שמאלה
            for x in range(cx + layer, cx - layer - 1, -1):
                if 0 <= x < 40 and 0 <= cy + layer < 30:
                    spiral.append((x, cy + layer))
            # למעלה
            for y in range(cy + layer, cy - layer - 1, -1):
                if 0 <= cx - layer < 40 and 0 <= y < 30:
                    spiral.append((cx - layer, y))
        self.save_map("Spiral Madness", spiral, width=40, height=30,
                      is_builtin=True, difficulty=3)

        # Figure-8
        figure8 = []
        for i in range(20):
            figure8.append((i, 10))
        for i in range(10, 20):
            figure8.append((20, i))
        for i in range(20, 40):
            figure8.append((i, 20))
        for i in range(20, 10, -1):
            figure8.append((39, i))
        for i in range(39, -1, -1):
            figure8.append((i, 10))
        self.save_map("Figure-8 Loop", figure8, width=40, height=30,
                      is_builtin=True, difficulty=2)

        # יצירת round configs למפות ברירת המחדל
        self.cursor.execute("SELECT id FROM maps WHERE is_builtin = 1")
        map_ids = [r[0] for r in self.cursor.fetchall()]

        for map_id in map_ids:
            self.cursor.execute("SELECT name FROM maps WHERE id = ?", (map_id,))
            map_name = self.cursor.fetchone()[0]

            config_id = self.save_round_config(
                name=f"{map_name} - Standard",
                map_id=map_id,
                total_waves=10,
                starting_money=450,
                starting_lives=10,
                tower_cost=100
            )

            # יצירת הגדרות גלים עם כיוונון איזון משחק
            # Recommended wave configuration parameters
            WAVE_CONFIGS = {
                1: {"total_enemies": 6, "spawn_interval": 400, "composition": {"soldier": 6}},
                2: {"total_enemies": 8, "spawn_interval": 350, "composition": {"soldier": 8}},
                3: {"total_enemies": 10, "spawn_interval": 300, "composition": {"soldier": 7, "tank": 3}},
                4: {"total_enemies": 13, "spawn_interval": 250, "composition": {"soldier": 8, "tank": 5}},
                5: {"total_enemies": 17, "spawn_interval": 200, "composition": {"soldier": 10, "tank": 5, "scout": 2}},
            }

            for wave in range(1, 11):
                if wave <= 5:
                    # Use recommended parameters for waves 1-5
                    wave_cfg = WAVE_CONFIGS[wave]
                    total_enemies = wave_cfg["total_enemies"]
                    spawn_interval = wave_cfg["spawn_interval"]
                    enemy_comp = wave_cfg["composition"]
                else:
                    # For waves 6-10, scale the wave 5 config exponentially
                    base_cfg = WAVE_CONFIGS[5]
                    scale = 1.25 ** (wave - 5)
                    total_enemies = max(17, int(base_cfg["total_enemies"] * scale))
                    spawn_interval = max(150, int(base_cfg["spawn_interval"] * (0.9 ** (wave - 5))))

                    # Build composition with scaled enemy types
                    enemy_comp = {}
                    enemy_comp["soldier"] = max(1, int(base_cfg["composition"]["soldier"] * scale))
                    enemy_comp["tank"] = max(0, int(base_cfg["composition"]["tank"] * scale))
                    enemy_comp["scout"] = max(0, int(base_cfg["composition"]["scout"] * scale))
                    if wave % 5 == 0:
                        enemy_comp["boss"] = 1

                self.save_wave_config(
                    round_config_id=config_id,
                    wave_number=wave,
                    total_enemies=total_enemies,
                    spawn_interval=spawn_interval,
                    enemy_composition=enemy_comp
                )

        # הוספת הישגים ברירת מחדל
        achievements = [
            ("First Blood", "הרוג אויב ראשון", "kills", 1),
            ("Tower Builder", "בנה 10 מגדלים", "towers_built", 10),
            ("Wave Survivor", "שרוד 5 גלים", "waves_completed", 5),
            ("Money Maker", "הרוג 100 אויבים", "kills", 100),
            ("Victory!", "נצח במשחק", "victory", 1),
            ("High Scorer", "הגעה ל-1000 נקודות", "score", 1000),
        ]

        for name, desc, cond_type, cond_val in achievements:
            self.cursor.execute('''
                INSERT OR IGNORE INTO achievements (name, description, condition_type, condition_value)
                VALUES (?, ?, ?, ?)
            ''', (name, desc, cond_type, cond_val))

        self.conn.commit()

    # ========== Map Methods ==========

    def save_map(self, name: str, path: List[Tuple[int, int]],
                 obstacles: List[Tuple[int, int]] = None,
                 width: int = 40, height: int = 30,
                 is_builtin: bool = False, difficulty: int = 1) -> int:
        """שמירת מפה חדשה ל-DB"""
        path_json = json.dumps(path)
        obstacles_json = json.dumps(obstacles) if obstacles else '[]'

        try:
            self.cursor.execute('''
                INSERT INTO maps (name, width, height, path_data, obstacles, is_builtin, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, width, height, path_json, obstacles_json, is_builtin, difficulty))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # מפה עם אותו שם כבר קיימת
            self.cursor.execute('''
                UPDATE maps
                SET width = ?, height = ?, path_data = ?, obstacles = ?,
                    is_builtin = ?, difficulty = ?
                WHERE name = ?
            ''', (width, height, path_json, obstacles_json, is_builtin, difficulty, name))
            self.conn.commit()
            self.cursor.execute("SELECT id FROM maps WHERE name = ?", (name,))
            return self.cursor.fetchone()[0]

    def get_map(self, map_id: int) -> Optional[Dict]:
        """קבלת מפה לפי ID"""
        self.cursor.execute('SELECT * FROM maps WHERE id = ?', (map_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'name': row['name'],
                'width': row['width'],
                'height': row['height'],
                'path': json.loads(row['path_data']),
                'obstacles': json.loads(row['obstacles']),
                'is_builtin': bool(row['is_builtin']),
                'difficulty': row['difficulty']
            }
        return None

    def get_map_by_name(self, name: str) -> Optional[Dict]:
        """קבלת מפה לפי שם"""
        self.cursor.execute('SELECT * FROM maps WHERE name = ?', (name,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'name': row['name'],
                'width': row['width'],
                'height': row['height'],
                'path': json.loads(row['path_data']),
                'obstacles': json.loads(row['obstacles']),
                'is_builtin': bool(row['is_builtin']),
                'difficulty': row['difficulty']
            }
        return None

    def get_all_maps(self) -> List[Dict]:
        """קבלת כל המפות"""
        self.cursor.execute('SELECT id, name, difficulty, is_builtin FROM maps ORDER BY difficulty')
        return [{
            'id': r['id'],
            'name': r['name'],
            'difficulty': r['difficulty'],
            'is_builtin': bool(r['is_builtin'])
        } for r in self.cursor.fetchall()]

    def delete_map(self, map_id: int) -> bool:
        """מחיקת מפה (לא builtin)"""
        self.cursor.execute("SELECT is_builtin FROM maps WHERE id = ?", (map_id,))
        row = self.cursor.fetchone()
        if row and not row['is_builtin']:
            self.cursor.execute('DELETE FROM maps WHERE id = ?', (map_id,))
            self.conn.commit()
            return True
        return False

    # ========== Round Config Methods ==========

    def save_round_config(self, name: str, map_id: int,
                          total_waves: int = 5,
                          starting_money: int = 450,
                          starting_lives: int = 10,
                          tower_cost: int = 100,
                          difficulty_multiplier: float = 1.0) -> int:
        """שמירת הגדרות סיבוב"""
        self.cursor.execute('''
            INSERT INTO round_configs
            (name, map_id, total_waves, starting_money, starting_lives,
             tower_cost, difficulty_multiplier)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, map_id, total_waves, starting_money, starting_lives,
              tower_cost, difficulty_multiplier))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_round_config(self, config_id: int) -> Optional[Dict]:
        """קבלת הגדרות סיבוב"""
        self.cursor.execute('SELECT * FROM round_configs WHERE id = ?', (config_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_round_configs_for_map(self, map_id: int) -> List[Dict]:
        """קבלת כל ה-round configs למפה מסוימת"""
        self.cursor.execute('''
            SELECT * FROM round_configs WHERE map_id = ? ORDER BY name
        ''', (map_id,))
        return [dict(r) for r in self.cursor.fetchall()]

    # ========== Wave Config Methods ==========

    def save_wave_config(self, round_config_id: int, wave_number: int,
                         total_enemies: int, spawn_interval: int,
                         enemy_composition: Dict) -> int:
        """שמירת הגדרות גל"""
        # קודם נמחק הגדרה קיימת לאותו גל
        self.cursor.execute('''
            DELETE FROM wave_configs
            WHERE round_config_id = ? AND wave_number = ?
        ''', (round_config_id, wave_number))

        self.cursor.execute('''
            INSERT INTO wave_configs
            (round_config_id, wave_number, total_enemies, spawn_interval, enemy_composition)
            VALUES (?, ?, ?, ?, ?)
        ''', (round_config_id, wave_number, total_enemies,
              spawn_interval, json.dumps(enemy_composition)))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_wave_configs(self, round_config_id: int) -> List[Dict]:
        """קבלת כל הגלים ל-round config מסוים"""
        self.cursor.execute('''
            SELECT * FROM wave_configs
            WHERE round_config_id = ?
            ORDER BY wave_number
        ''', (round_config_id,))
        result = []
        for r in self.cursor.fetchall():
            d = dict(r)
            d['enemy_composition'] = json.loads(d['enemy_composition'])
            result.append(d)
        return result

    # ========== Game Stats Methods ==========

    def save_game_result(self, map_id: int, round_config_id: int,
                         score: int, waves_completed: int,
                         victory: bool, enemies_killed: int = 0,
                         towers_built: int = 0, play_time: int = 0):
        """שמירת תוצאות משחק"""
        self.cursor.execute('''
            INSERT INTO game_stats
            (map_id, round_config_id, score, waves_completed, victory,
             enemies_killed, towers_built, play_time_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (map_id, round_config_id, score, waves_completed, victory,
              enemies_killed, towers_built, play_time))
        self.conn.commit()

        # עדכון הישגים
        self._check_achievements(score=score, kills=enemies_killed,
                                  waves_completed=waves_completed,
                                  towers_built=towers_built,
                                  victory=victory)

    def get_high_scores(self, limit: int = 10) -> List[Dict]:
        """קבלת 10 התוצאות הגבוהות ביותר"""
        self.cursor.execute('''
            SELECT gs.score, gs.date_played, gs.victory, m.name as map_name
            FROM game_stats gs
            JOIN maps m ON gs.map_id = m.id
            WHERE gs.victory = 1
            ORDER BY gs.score DESC
            LIMIT ?
        ''', (limit,))
        return [{
            'score': r['score'],
            'date': r['date_played'],
            'map': r['map_name']
        } for r in self.cursor.fetchall()]

    def get_stats_summary(self) -> Dict:
        """קבלת סיכום סטטיסטיקות כללי"""
        self.cursor.execute('''
            SELECT
                COUNT(*) as total_games,
                SUM(CASE WHEN victory = 1 THEN 1 ELSE 0 END) as victories,
                SUM(score) as total_score,
                SUM(enemies_killed) as total_kills,
                SUM(towers_built) as total_towers,
                SUM(play_time_seconds) as total_play_time
            FROM game_stats
        ''')
        row = self.cursor.fetchone()
        return {
            'total_games': row['total_games'] or 0,
            'victories': row['victories'] or 0,
            'total_score': row['total_score'] or 0,
            'total_kills': row['total_kills'] or 0,
            'total_towers': row['total_towers'] or 0,
            'total_play_time': row['total_play_time'] or 0
        }

    # ========== Achievement Methods ==========

    def get_achievements(self) -> List[Dict]:
        """קבלת כל ההישגים"""
        self.cursor.execute('SELECT * FROM achievements')
        return [dict(r) for r in self.cursor.fetchall()]

    def get_unlocked_achievements(self) -> List[Dict]:
        """קבלת הישגים שנפתחו"""
        self.cursor.execute('SELECT * FROM achievements WHERE unlocked = 1')
        return [dict(r) for r in self.cursor.fetchall()]

    def _check_achievements(self, **stats):
        """בדיקה והוספת הישגים שנפתחו"""
        self.cursor.execute('SELECT * FROM achievements WHERE unlocked = 0')
        for achievement in self.cursor.fetchall():
            cond_type = achievement['condition_type']
            cond_value = achievement['condition_value']

            if cond_type in stats and stats[cond_type] >= cond_value:
                self.cursor.execute('''
                    UPDATE achievements
                    SET unlocked = 1, unlocked_at = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), achievement['id']))

        self.conn.commit()

    # ========== Player Settings Methods ==========

    def save_setting(self, key: str, value: str):
        """שמירת הגדרת שחקן"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO player_settings (setting_key, setting_value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        self.conn.commit()

    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        """קבלת הגדרת שחקן"""
        self.cursor.execute('SELECT setting_value FROM player_settings WHERE setting_key = ?',
                           (key,))
        row = self.cursor.fetchone()
        return row['setting_value'] if row else default

    def get_all_settings(self) -> Dict[str, str]:
        """קבלת כל ההגדרות"""
        self.cursor.execute('SELECT setting_key, setting_value FROM player_settings')
        return {r['setting_key']: r['setting_value'] for r in self.cursor.fetchall()}

    # ========== Round State Methods ==========

    def save_round_state(self, round_config_id: int, current_wave: int,
                         current_money: int, current_lives: int, current_score: int,
                         towers: List[Dict], enemies_killed: int,
                         time_elapsed: int) -> int:
        """שמירת מצב סיבוב פעיל, מחזיר את ה-ID של ה-round_state"""
        towers_json = json.dumps(towers)
        self.cursor.execute('''
            INSERT INTO round_states
            (round_config_id, current_wave, current_money, current_lives,
             current_score, towers_placed, enemies_killed_total, time_elapsed_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (round_config_id, current_wave, current_money, current_lives,
              current_score, towers_json, enemies_killed, time_elapsed))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_round_state(self, round_state_id: int, **kwargs):
        """עדכון חלקי של מצב סיבוב"""
        allowed_fields = {'current_wave', 'current_money', 'current_lives',
                          'current_score', 'towers_placed', 'enemies_killed_total',
                          'time_elapsed_seconds', 'is_active'}
        updates = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                if key == 'towers_placed' and isinstance(value, list):
                    value = json.dumps(value)
                updates.append(f"{key} = ?")
                values.append(value)
        if not updates:
            return
        values.append(datetime.now().isoformat())
        values.append(round_state_id)
        self.cursor.execute(f'''
            UPDATE round_states
            SET {', '.join(updates)}, saved_at = ?
            WHERE id = ?
        ''', values)
        self.conn.commit()

    def get_round_state(self, round_state_id: int) -> Optional[Dict]:
        """קבלת מצב סיבוב לפי ID"""
        self.cursor.execute('SELECT * FROM round_states WHERE id = ?', (round_state_id,))
        row = self.cursor.fetchone()
        if row:
            result = dict(row)
            result['towers_placed'] = json.loads(result['towers_placed'])
            return result
        return None

    def get_active_round_states(self) -> List[Dict]:
        """קבלת כל ה-round_states הפעילים (ניתנים להמשך)"""
        self.cursor.execute('''
            SELECT rs.id, rs.round_config_id, rs.current_wave, rs.current_score,
                   rs.current_money, rs.current_lives, rs.time_elapsed_seconds,
                   rs.saved_at, m.name as map_name
            FROM round_states rs
            JOIN round_configs rc ON rs.round_config_id = rc.id
            JOIN maps m ON rc.map_id = m.id
            WHERE rs.is_active = 1
            ORDER BY rs.saved_at DESC
        ''')
        return [dict(r) for r in self.cursor.fetchall()]

    def complete_round_state(self, round_state_id: int, victory: bool):
        """סימום סיבוב כמסתיים (הצלה/הפסד)"""
        self.cursor.execute('''
            UPDATE round_states
            SET is_active = 0, saved_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), round_state_id))
        self.conn.commit()

    def delete_round_state(self, round_state_id: int):
        """מחיקת round_state (למשחק שהסתיים או נזנח)"""
        self.cursor.execute('DELETE FROM round_states WHERE id = ?', (round_state_id,))
        self.cursor.execute('DELETE FROM wave_progress WHERE round_state_id = ?', (round_state_id,))
        self.cursor.execute('DELETE FROM tower_actions WHERE round_state_id = ?', (round_state_id,))
        self.conn.commit()

    # ========== Wave Progress Methods ==========

    def start_wave_tracking(self, round_state_id: int, wave_number: int) -> int:
        """תחילת מעקב אחר גל חדש, מחזיר את ה-ID של wave_progress"""
        self.cursor.execute('''
            INSERT INTO wave_progress (round_state_id, wave_number)
            VALUES (?, ?)
        ''', (round_state_id, wave_number))
        self.conn.commit()
        return self.cursor.lastrowid

    def complete_wave(self, round_state_id: int, wave_number: int,
                      enemies_killed: int, time_taken: int,
                      money_earned: int, damage_taken: int):
        """סימון גל כהושלם עם סטטיסטיקות"""
        self.cursor.execute('''
            UPDATE wave_progress
            SET completed = 1,
                enemies_killed = ?,
                time_taken_seconds = ?,
                money_earned = ?,
                damage_taken = ?,
                completed_at = ?
            WHERE round_state_id = ? AND wave_number = ?
        ''', (enemies_killed, time_taken, money_earned, damage_taken,
              datetime.now().isoformat(), round_state_id, wave_number))
        self.conn.commit()

    def get_wave_progress(self, round_state_id: int) -> List[Dict]:
        """קבלת התקדמות כל הגלים עבור round_state מסוים"""
        self.cursor.execute('''
            SELECT * FROM wave_progress
            WHERE round_state_id = ?
            ORDER BY wave_number
        ''', (round_state_id,))
        return [dict(r) for r in self.cursor.fetchall()]

    # ========== Tower Action Methods ==========

    def record_tower_placement(self, round_state_id: int, tower_type: str,
                               grid_x: int, grid_y: int, cost: int):
        """רישום הצבת מגדל"""
        self.cursor.execute('''
            INSERT INTO tower_actions (round_state_id, action_type, tower_type, grid_x, grid_y, cost)
            VALUES (?, 'placed', ?, ?, ?, ?)
        ''', (round_state_id, tower_type, grid_x, grid_y, cost))
        self.conn.commit()

    def record_tower_removal(self, round_state_id: int, tower_type: str,
                             grid_x: int, grid_y: int):
        """רישום הסרת מגדל"""
        self.cursor.execute('''
            INSERT INTO tower_actions (round_state_id, action_type, tower_type, grid_x, grid_y, cost)
            VALUES (?, 'removed', ?, ?, ?, 0)
        ''', (round_state_id, tower_type, grid_x, grid_y))
        self.conn.commit()

    def get_tower_history(self, round_state_id: int) -> List[Dict]:
        """קבלת היסטוריית פעולות מגדלים"""
        self.cursor.execute('''
            SELECT * FROM tower_actions
            WHERE round_state_id = ?
            ORDER BY timestamp
        ''', (round_state_id,))
        return [dict(r) for r in self.cursor.fetchall()]

    def close(self):
        """סגירת החיבור ל-DB"""
        self.conn.close()
