import sqlite3
from pathlib import Path

#Project root folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]
#Data folder path
DATA_DIR = PROJECT_ROOT / "DATA"
#SQLite database path
DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)#Create DATA folder if it doesn't exist
    print("USING DB:", DB_PATH)  #Show which DB is used
    conn = sqlite3.connect(str(DB_PATH))#Connect to SQLite DB
    conn.row_factory = sqlite3.Row#Make rows behave like dictionaries
    return conn


