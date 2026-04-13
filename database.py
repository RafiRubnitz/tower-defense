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

            # יצירת הגדרות גלים
            for wave in range(1, 11):
                enemy_comp = {"soldier": max(1, wave)}
                if wave >= 3:
                    enemy_comp["tank"] = max(0, wave - 2)
                if wave >= 5:
                    enemy_comp["scout"] = max(0, wave - 4)
                if wave % 5 == 0:
                    enemy_comp["boss"] = 1

                self.save_wave_config(
                    round_config_id=config_id,
                    wave_number=wave,
                    total_enemies=sum(enemy_comp.values()),
                    spawn_interval=max(20, 60 - wave * 4),
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

    def close(self):
        """סגירת החיבור ל-DB"""
        self.conn.close()
