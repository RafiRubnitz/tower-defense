# Tower Defense - רשימת שיפורים ומשימות לביצוע

## 📊 ניתוח מצב נוכחי

### מה קיים במשחק היום:
- ✅ מפה בסיסית אחת (מסלול L פשוט)
- ✅ סוג אויב אחד (Soldier - אדום)
- ✅ סוג מגדל אחד (BasicTower - כחול)
- ✅ מערכת גלים בסיסית (5 גלים)
- ✅ UI בסיסי (כסף, לבות, ניקוד, כפתור Restart)
- ✅ ירי אוטומטי של מגדלים

### חסרונות עיקריים:
- ❌ אין וריאציה במפות
- ❌ אין אלגוריתם קושי אמיתי
- ❌ אין סוגי אויבים שונים
- ❌ אין סוגי מגדלים שונים
- ❌ אין מערכת שדרוגים למגדלים
- ❌ אין power-ups או יכולות מיוחדות

---

## 🗺️ 1. מערכת מפות מתקדמת

### 1.1 סוגי מסלולים שונים
| סוג מסלול | תיאור | רמת קושי |
|-----------|-------|----------|
| **L-Path** | המסלול הקיים (ימינה-למטה) | קל |
| **Z-Path** | מסלול זיגזג | בינוני |
| **Spiral** | מסלול ספירלה פנימה | קשה |
| **Figure-8** | מסלול בצורת 8 | בינוני-קשה |
| **Multi-Branch** | מסלול מתפצל | קשה מאוד |
| **Circular** | מסלול מעגלי | בינוני |

### 1.2 מימוש מומלץ
```python
class MapFactory:
    @staticmethod
    def create_map(map_type: MapType) -> Map:
        """יצירת מפה לפי סוג"""
        
class MapType(Enum):
    L_PATH = "l_path"
    Z_PATH = "z_path" 
    SPIRAL = "spiral"
    FIGURE_8 = "figure8"
    MULTI_BRANCH = "multi_branch"
```

### 1.3 פיצ'רים נוספים למפות
- **מכשולים:** שדות שאי אפשר לבנות עליהם (אגמים, הרים)
- **נקודות חסימה:** מקומות אסטרטגיים לבניית מגדלים
- **קיצורי דרך:** נפתחים בגלים מסוימים
- **טריינים משתנים:** המסלול משתנה בין גלים

---

## 🎯 2. אלגוריתם קושי דינמי

### 2.1 הבעיה הנוכחית
הקוד הנוכחי מגדיר קושי ליניארי פשוט:
```python
wave.total_enemies = 5 + (i * 3)  # ליניארי מדי
wave.spawn_interval = max(30, 60 - (i * 5))  # לא מספיק מאתגר
```

### 2.2 אלגוריתם קושי מומלץ
```python
class DifficultyManager:
    def __init__(self):
        self.base_difficulty = 1.0
        self.player_performance = 0  # ניקוד ממוצע לגל
        
    def calculate_wave_difficulty(self, wave_number: int) -> WaveConfig:
        """חישוב קושי מבוסס ביצועי שחקן"""
        
        # מדדי קושי:
        # 1. כמות אויבים = base * (1.2 ^ wave_number)
        # 2. חיי אויבים = base_hp * (1.15 ^ wave_number)
        # 3. מהירות אויבים = base_speed * (1 + wave_number * 0.05)
        # 4. spawn_rate = max(15, 60 - wave_number * 3)
        
    def adjust_difficulty_based_on_performance(self):
        """התאמת קושי לפי ביצועי שחקן"""
        # אם השחקן מצליח בקלות -> להגדיל קושי
        # אם השחקן מתקשה -> להקל מעט
```

### 2.3 פרמטרי קושי
| פרמטר | נוסחה | השפעה |
|--------|-------|--------|
| כמות אויבים | `5 + 3 * wave^1.2` | גדילה מעריכית |
| חיי אויבים | `100 * 1.15^wave` | כל גל 15% יותר חזק |
| מהירות | `2.0 + wave * 0.1` | כל גל מהיר יותר |
| bounty | `15 * 1.1^wave` | פרס גדל לאט |
| spawn_interval | `max(20, 60 - wave * 4)` | קצב מהיר יותר |

---

## 👾 3. סוגי אויבים חדשים

### 3.1 טבלת סוגי אויבים
| סוג | HP | מהירות | bounty | יכולות מיוחדות |
|-----|-----|---------|--------|-----------------|
| **Soldier** (קיים) | 100 | 2.0 | 15 | בסיסי |
| **Tank** | 300 | 1.0 | 30 | איטי, הרבה HP |
| **Scout** | 50 | 4.0 | 20 | מהיר מאוד |
| **Boss** | 1000 | 0.8 | 100 | בוס בסוף גל |
| **Ghost** | 80 | 2.5 | 25 | חסיף חלקית למגדלים |
| **Healer** | 150 | 1.5 | 35 | מרפא אויבים קרובים |
| **Splitter** | 120 | 1.8 | 25 | מתפצל ל-2 כשמת |
| **Armored** | 200 | 1.2 | 30 | חסין לירי ראשון |

### 3.2 מימוש מומלץ
```python
class EnemyType(Enum):
    SOLDIER = "soldier"
    TANK = "tank"
    SCOUT = "scout"
    BOSS = "boss"
    GHOST = "ghost"
    HEALER = "healer"
    SPLITTER = "splitter"
    ARMORED = "armored"

class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type: EnemyType, pos: Point, level: int) -> Enemy:
        """יצירת אויב לפי סוג"""
```

### 3.3 יכולות מיוחדות
- **Healer Aura:** מרפא אויבים ברדיוס 50px
- **Spawn on Death:** משריץ 2 אויבים קטנים כשמת
- **Invisibility:** נעלם לזמן קצר
- **Shield:** חסין ל-3 פגיעות ראשונות

---

## 🏰 4. סוגי מגדלים חדשים

### 4.1 טבלת סוגי מגדלים
| סוג | מחיר | range | damage | cooldown | יכולות |
|-----|------|-------|--------|----------|---------|
| **Basic** (קיים) | 100 | 3.5 | 50 | 600ms | בסיסי |
| **Sniper** | 200 | 8.0 | 200 | 2000ms | נזק גבוה, range רחב |
| **MachineGun** | 150 | 3.0 | 15 | 100ms | ירי מהיר |
| **Splash** | 250 | 4.0 | 80 | 1000ms | נזק לאזור |
| **Slow** | 120 | 3.5 | 20 | 500ms | מאט אויבים |
| **Laser** | 300 | 5.0 | 5 | 50ms | קרן לייזר מתמדת |
| **Missile** | 350 | 6.0 | 150 | 1500ms | טיל מתעקל |
| **Ice** | 180 | 3.5 | 25 | 600ms | מקפיא לזמן קצר |

### 4.2 מימוש מומלץ
```python
class TowerType(Enum):
    BASIC = "basic"
    SNIPER = "sniper"
    MACHINE_GUN = "machine_gun"
    SPLASH = "splash"
    SLOW = "slow"
    LASER = "laser"
    MISSILE = "missile"
    ICE = "ice"

class TowerFactory:
    @staticmethod
    def create_tower(tower_type: TowerType, pos: Point) -> Tower:
        """יצירת מגדל לפי סוג"""
```

### 4.3 אפקטים מיוחדים
- **Slow Effect:** מאט אויבים ב-30% ל-2 שניות
- **Splash Damage:** נזק לכל האויבים ברדיוס 40px
- **Burn Effect:** נזק מתמשך ל-3 שניות
- **Stun:** משתק אויב ל-1 שנייה

---

## ⬆️ 5. מערכת שדרוגים

### 5.1 סוגי שדרוגים
```python
class UpgradeType(Enum):
    DAMAGE = "damage"      # +20% נזק
    RANGE = "range"        # +15% טווח
    COOLDOWN = "cooldown"  # -15% זמן טעינה
    SPECIAL = "special"    # יכולת מיוחדת
```

### 5.2 עלויות שדרוג
| רמה | עלות | בונוס |
|-----|------|-------|
| Level 1 → 2 | 50$ | +20% damage |
| Level 2 → 3 | 100$ | +15% range |
| Level 3 → 4 | 150$ | -15% cooldown |
| Level 4 → 5 | 250$ | יכולת מיוחדת |

### 5.3 מימוש מומלץ
```python
class Tower:
    def upgrade(self, upgrade_type: UpgradeType) -> bool:
        """שדרג מגדל, החזר True אם הצליח"""
        cost = self.get_upgrade_cost(upgrade_type)
        if self.round_ref.money >= cost:
            self.round_ref.money -= cost
            self.apply_upgrade(upgrade_type)
            return True
        return False
    
    def get_upgrade_cost(self, upgrade_type: UpgradeType) -> int:
        """חישוב עלות שדרוג"""
        base_costs = {
            UpgradeType.DAMAGE: 50 * self.level,
            UpgradeType.RANGE: 75 * self.level,
            UpgradeType.COOLDOWN: 60 * self.level,
        }
        return base_costs.get(upgrade_type, 100)
```

---

## 🎮 6. מכניקות משחק נוספות

### 6.1 Power-Ups
| Power-Up | השפעה | מחיר |
|----------|-------|------|
| **Bomb** | פיצוץ שמשמיד כל אויב במסך | 200$ |
| **Freeze** | מקפיא את כל האויבים ל-5 שניות | 150$ |
| **Speed Boost** | מגדיל מהירות ירי ב-50% ל-10 שניות | 100$ |
| **Extra Life** | מוסיף לב אחד | 300$ |
| **Money Bag** | מוסיף 100$ | 80$ |

### 6.2 יכולות שחקן
- **Pause/Resume:** קיים (מקש SPACE)
- **Sell Tower:** מכירת מגדל ב-50% מחיר
- **Rotate Map:** סיבוב המפה (אם נתמך)
- **Slow Motion:** האטת זמן ל-5 שניות

### 6.3 הגדרות משחק
```python
class GameSettings:
    difficulty: Difficulty  # EASY, NORMAL, HARD
    starting_money: int = 450
    starting_lives: int = 10
    enable_powerups: bool = True
    enable_upgrades: bool = True
```

---

## 🎨 7. שיפורים ויזואליים

### 7.1 אנימציות
- **אנימציית ירי:** חלקיקים כשהמגדל יורה
- **אנימציית פגיעה:** הבזק כשאויב נפגע
- **אנימציית מוות:** פיצוץ/היעלמות של אויב
- **אנימציית בנייה:** אפקט כשבונים מגדל

### 7.2 אפקטים
- **חלקיקים:** Sparks, smoke, debris
- **מזג אוויר:** גשם, שלג, ערפל
- **תאורה:** הצללות, זוהר סביב מגדלים

### 7.3 UI משופר
- **תפריט ראשי:** Start, Settings, Quit
- **מסך סיום:** סטטיסטיקות מפורטות
- **מיני-מפה:** תצוגה ממוזערת של כל המפה
- **התראות:** הודעות על גלים, boss fights

---

## 🔊 8. סאונד ומוזיקה

### 8.1 אפקטים קוליים
| אירוע | סאונד |
|-------|--------|
| יריית מגדל | pew/pew |
| פגיעה באויב | hit/thud |
| מות אויב | explosion |
| בניית מגדל | build sound |
| גל מתחיל | warning siren |
| ניצחון/הפסד | victory/defeat theme |

### 8.2 מוזיקת רקע
- **תפריט:** מוזיקה רגועה
- **משחק:** מוזיקה דינמית שמתגברת עם הגלים
- **Boss:** מוזיקה מלחיצה

---

## 📁 9. ארכיטקטורה מומלצת

### 9.1 מבנה קבצים חדש
```
tower_defense/
├── main.py                 # נקודת כניסה
├── game/
│   ├── __init__.py
│   ├── game.py            # מחלקת Game ראשית
│   ├── settings.py        # הגדרות משחק
│   └── states.py          # מצבי משחק (menu, playing, paused)
├── entities/
│   ├── __init__.py
│   ├── enemy.py           # כל סוגי האויבים
│   ├── tower.py           # כל סוגי המגדלים
│   ├── bullet.py          # קליעים ואפקטים
│   └── player.py          # שחקן
├── maps/
│   ├── __init__.py
│   ├── map_base.py        # מחלקת Map בסיס
│   ├── map_factory.py     # יצירת מפות
│   └── presets/           # מפות מוגדרות מראש
│       ├── l_path.py
│       ├── spiral.py
│       └── ...
├── systems/
│   ├── __init__.py
│   ├── difficulty.py      # אלגוריתם קושי
│   ├── wave_manager.py    # ניהול גלים
│   ├── upgrade_system.py  # מערכת שדרוגים
│   └── powerup_system.py  # מערכת power-ups
├── ui/
│   ├── __init__.py
│   ├── menu.py            # תפריט ראשי
│   ├── hud.py             # HUD במשחק
│   └── pause_menu.py      # תפריט השהיה
├── assets/
│   ├── images/
│   ├── sounds/
│   └── music/
└── utils/
    ├── __init__.py
    ├── point.py
    └── pathfinding.py     # אלגוריתמי מסלול
```

### 9.2 מחלקות ליבה חדשות
```python
# Difficulty Manager
class DifficultyManager:
    def calculate_enemy_stats(wave: int, enemy_type: str) -> EnemyStats
    def adjust_based_on_performance(player_stats: dict)

# Wave Manager  
class WaveManager:
    def get_wave_config(wave_number: int) -> WaveConfig
    def spawn_enemies()
    def check_wave_complete() -> bool

# Upgrade System
class UpgradeSystem:
    def get_available_upgrades(tower: Tower) -> List[Upgrade]
    def apply_upgrade(tower: Tower, upgrade: Upgrade)
    def get_upgrade_cost(tower: Tower, upgrade: Upgrade) -> int
```

---

## 📋 10. רשימת משימות לפי סדר עדיפות

### 🔴 קריטי (חובה לשיפור המשחק)
1. **תפריט ראשי** - Main Menu עם Play, Settings, Quit
2. **מערכת בחירת מפות** - מסך בחירת מפה מתוך רשימה
3. **אלגוריתם קושי דינמי** - הפיכת הגלים למאתגרים באמת
4. **3 סוגי אויבים נוספים** - Tank, Scout, Boss
5. **3 סוגי מגדלים נוספים** - Sniper, MachineGun, Splash
6. **מערכת שדרוגים בסיסית** - שדרוג נזק/טווח/מהירות

### 🟡 חשוב (משפר משמעותית את החוויה)
7. **מערכת Database** - שמירת מפות, הגדרות סיבובים, סטטיסטיקות
8. **עורך מפות** - כלי ליצירת מפות מותאמות אישית
9. **3 מפות נוספות** - Spiral, Z-Path, Figure-8
10. **Power-Ups בסיסיים** - Bomb, Freeze
11. **מסך Settings** - הגדרות קושי, ווליום, תצוגה
12. **אפקטים קוליים בסיסיים** - ירי, פגיעה, מוות

### 🟢 ניסוי (פיצ'רים מתקדמים)
13. **אנימציות וחלקיקים**
14. **סוגי אויבים מתקדמים** - Healer, Splitter, Ghost
15. **סוגי מגדלים מתקדמים** - Laser, Missile, Ice
16. **מערכת הצלה/רנקינג**
17. **מערכת אתגרים יומיים**

---

## 🎮 11. תפריט ראשי (Main Menu)

### 11.1 מבנה התפריט
```
┌─────────────────────────────────┐
│     TOWER DEFENSE               │
│     ===== ======                │
│                                 │
│        [ PLAY ]                 │
│        [ MAPS ]                 │
│      [ SETTINGS ]               │
│        [ QUIT ]                 │
│                                 │
│   High Score: 12,450            │
└─────────────────────────────────┘
```

### 11.2 מסכים נדרשים
| מסך | תיאור | רכיבים |
|-----|-------|--------|
| **Main Menu** | תפריט ראשי | Title, Play, Maps, Settings, Quit, High Score |
| **Map Selection** | בחירת מפה | רשימת מפות, Preview, Start Button, Back |
| **Settings** | הגדרות משחק | Difficulty, Volume, Fullscreen, Back |
| **Pause Menu** | השהיית משחק | Resume, Restart, Settings, Quit |
| **Game Over** | סיום משחק | Score, Restart, Main Menu |
| **Victory** | ניצחון | Score, Stars, Restart, Main Menu |

### 11.3 מימוש מומלץ
```python
class GameState(Enum):
    MAIN_MENU = "main_menu"
    MAP_SELECTION = "map_selection"
    SETTINGS = "settings"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class MenuManager:
    def __init__(self, game):
        self.current_state = GameState.MAIN_MENU
        self.buttons = {}
        
    def handle_event(self, event):
        """טפל בקליקים על כפתורים"""
        
    def draw(self, win):
        """צייר את המסך הנוכחי"""
        
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        
    def draw(self, win):
        color = (100, 100, 100) if self.hovered else (80, 80, 80)
        pygame.draw.rect(win, color, self.rect)
        # render text...
```

---

## 🗄️ 12. מערכת Database

### 12.1 טבלאות נדרשות

#### טבלת מפות (maps)
```sql
CREATE TABLE maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    width INTEGER DEFAULT 40,
    height INTEGER DEFAULT 30,
    path_data TEXT NOT NULL,  -- JSON array of path points
    obstacles TEXT,           -- JSON array of obstacle positions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_builtin BOOLEAN DEFAULT 0,
    difficulty INTEGER DEFAULT 1
);
```

#### טבלת הגדרות סיבוב (round_configs)
```sql
CREATE TABLE round_configs (
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
```

#### טבלת גלים (wave_configs)
```sql
CREATE TABLE wave_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_config_id INTEGER,
    wave_number INTEGER,
    total_enemies INTEGER,
    spawn_interval INTEGER,
    enemy_composition TEXT,  -- JSON: {"soldier": 5, "tank": 2, ...}
    FOREIGN KEY (round_config_id) REFERENCES round_configs(id)
);
```

#### טבלת סטטיסטיקות (game_stats)
```sql
CREATE TABLE game_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    map_id INTEGER,
    round_config_id INTEGER,
    score INTEGER,
    waves_completed INTEGER,
    enemies_killed INTEGER,
    towers_built INTEGER,
    play_time_seconds INTEGER,
    date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    victory BOOLEAN,
    FOREIGN KEY (map_id) REFERENCES maps(id),
    FOREIGN KEY (round_config_id) REFERENCES round_configs(id)
);
```

#### טבלת הישגים (achievements)
```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    condition_type TEXT,      -- e.g., "score", "kills", "waves"
    condition_value INTEGER,
    unlocked BOOLEAN DEFAULT 0,
    unlocked_at TIMESTAMP
);
```

### 12.2 מימוש מומלץ
```python
import sqlite3
import json
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "tower_defense.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """יצירת הטבלאות אם לא קיימות"""
        self.cursor.executescript('''
            -- כל ה-CREATE TABLE למעלה
        ''')
        self.conn.commit()
    
    # Maps
    def save_map(self, name: str, path: List[tuple], 
                 obstacles: List[tuple] = None, 
                 width: int = 40, height: int = 30):
        path_json = json.dumps(path)
        obstacles_json = json.dumps(obstacles) if obstacles else '[]'
        self.cursor.execute('''
            INSERT INTO maps (name, width, height, path_data, obstacles)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, width, height, path_json, obstacles_json))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_map(self, map_id: int) -> Optional[Dict]:
        self.cursor.execute('SELECT * FROM maps WHERE id = ?', (map_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0], 'name': row[1], 'width': row[2], 
                'height': row[3], 'path': json.loads(row[4]),
                'obstacles': json.loads(row[5])
            }
        return None
    
    def get_all_maps(self) -> List[Dict]:
        self.cursor.execute('SELECT id, name, difficulty FROM maps')
        return [{'id': r[0], 'name': r[1], 'difficulty': r[2]} 
                for r in self.cursor.fetchall()]
    
    # Round configs
    def save_round_config(self, name: str, map_id: int,
                          total_waves: int = 5,
                          starting_money: int = 450,
                          starting_lives: int = 10) -> int:
        self.cursor.execute('''
            INSERT INTO round_configs (name, map_id, total_waves, 
                                        starting_money, starting_lives)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, map_id, total_waves, starting_money, starting_lives))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def save_wave_config(self, round_config_id: int, wave_number: int,
                         total_enemies: int, spawn_interval: int,
                         enemy_composition: Dict):
        self.cursor.execute('''
            INSERT INTO wave_configs 
            (round_config_id, wave_number, total_enemies, 
             spawn_interval, enemy_composition)
            VALUES (?, ?, ?, ?, ?)
        ''', (round_config_id, wave_number, total_enemies, 
              spawn_interval, json.dumps(enemy_composition)))
        self.conn.commit()
    
    def get_round_config(self, config_id: int) -> Dict:
        """קבלת הגדרות סיבוב כולל כל הגלים"""
        # implementation...
    
    # Stats
    def save_game_result(self, map_id: int, config_id: int,
                         score: int, waves_completed: int,
                         victory: bool, **kwargs):
        self.cursor.execute('''
            INSERT INTO game_stats 
            (map_id, round_config_id, score, waves_completed, 
             victory, enemies_killed, towers_built, play_time_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (map_id, config_id, score, waves_completed, victory,
              kwargs.get('enemies_killed', 0),
              kwargs.get('towers_built', 0),
              kwargs.get('play_time', 0)))
        self.conn.commit()
    
    def get_high_scores(self, limit: int = 10) -> List[Dict]:
        self.cursor.execute('''
            SELECT score, date_played, maps.name as map_name
            FROM game_stats
            JOIN maps ON game_stats.map_id = maps.id
            WHERE victory = 1
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        return [{'score': r[0], 'date': r[1], 'map': r[2]} 
                for r in self.cursor.fetchall()]
    
    def close(self):
        self.conn.close()
```

### 12.3 מפות ברירת מחדל
ה-DB יכיל 3 מפות מובנות:
```python
def insert_builtin_maps(db: Database):
    # L-Path (הקיימת)
    l_path = [(i, 15) for i in range(20)] + [(20, j) for j in range(15, 30)]
    db.save_map("Classic L-Path", l_path, is_builtin=True)
    
    # Z-Path
    z_path = ([(i, 5) for i in range(0, 40)] + 
              [(39-i, 15) for i in range(0, 40)] +
              [(i, 25) for i in range(0, 40)])
    db.save_map("Zigzag Challenge", z_path, is_builtin=True, difficulty=2)
    
    # Spiral
    spiral = []  # מסלול ספירלה
    db.save_map("Spiral Madness", spiral, is_builtin=True, difficulty=3)
```

---

## 🎯 סיכום והמלצות

### מה לשפר קודם?
1. **אלגוריתם קושי** - זה הדבר הכי חשוב. המשחק הנוכחי קל מדי וצפוי.
2. **וריאציה באויבים** - להוסיף לפחות 2-3 סוגים שונים.
3. **וריאציה במגדלים** - לתת לשחקן יותר אפשרויות אסטרטגיות.
4. **שדרוגים** - לאפשר התקדמות ותחושת שיפור.

### למה זה חשוב?
- **אלגוריתם קושי** גורם לשחקנים להישאר מעורבים
- **וריאציה** מונעת שעמום ומעודדת ניסיון אסטרטגיות חדשות
- **שדרוגים** נותנים תחושת התקדמות וסיפוק

### הערכת זמנים משוערת:
- אלגוריתם קושי: 2-3 שעות
- סוגי אויבים חדשים: 3-4 שעות
- סוגי מגדלים חדשים: 4-5 שעות
- מערכת שדרוגים: 2-3 שעות
- מפות נוספות: 3-4 שעות

**סה"כ למינימום viable משופר: ~15 שעות עבודה**
