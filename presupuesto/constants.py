import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent.parent
DB_PATH = APP_DIR / "presupuesto.db"

RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))
ICON_PATH = RESOURCE_DIR / "assets" / "app_icon.ico"

APP_BG = "#eef2f6"
PANEL_BG = "#ffffff"
TEXT = "#1f2937"
MUTED = "#667085"
ACCENT = "#2563eb"
ACCENT_DARK = "#1d4ed8"
GREEN = "#15803d"
ORANGE = "#b45309"
RED = "#b91c1c"
CYAN = "#0891b2"
PINK = "#db2777"
PURPLE = "#7c3aed"
YELLOW = "#ca8a04"

DEFAULT_INCOME = 800000
DEFAULT_SAVINGS_PERCENT = 3.0
DEFAULT_FIXED_EXPENSES = [
    ("Hogar", 145740),
    ("Cabello", 30000),
    ("Transporte BIP/METRO", 10000),
    ("Youtube Premium", 11000),
    ("Chat GPT", 19990),
    ("Google One", 1790),
    ("Crunchyroll", 6490),
    ("Xbox Game Pass", 12000),
    ("DGO", 22900),
    ("Movistar", 20328),
]
