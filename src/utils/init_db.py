from pathlib import Path
from src.utils.db import get_connection

def init_db():
    conn = get_connection()
    schema_path = Path(__file__).resolve().parents[2] / "schema.sql"
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
