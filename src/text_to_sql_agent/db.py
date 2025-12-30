from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parents[2]
DB_URL = BASE_DIR / "src" / "text_to_sql_agent" / "chinook.db"

engine = create_engine(f"sqlite:///{DB_URL}")
