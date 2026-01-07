import uuid
from src.utils.db import get_connection

DEFAULT_SECTIONS = ["To Do", "In Progress", "Review", "Done"]

def create_sections():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM sections")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    cur.execute("SELECT project_id FROM projects")
    projects = cur.fetchall()

    for (project_id,) in projects:
        for idx, name in enumerate(DEFAULT_SECTIONS):
            section_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO sections (section_id, project_id, name, order_index)
                VALUES (?, ?, ?, ?)
            """, (section_id, project_id, name, idx))

    conn.commit()
    conn.close()
