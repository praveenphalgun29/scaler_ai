import random
from datetime import datetime, timedelta
from src.utils.db import get_connection
from src.utils.hf_pool import load_pools

POOLS = load_pools()

def random_due(c):
    r = random.random()
    if r < .10: return None
    if r < .35: return c + timedelta(days=random.randint(1,7))
    if r < .75: return c + timedelta(days=random.randint(8,30))
    return c + timedelta(days=random.randint(31,90))

def create_tasks():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks")

    cur.execute("""
        SELECT p.project_id, p.project_type, s.section_id
        FROM projects p
        JOIN sections s ON p.project_id = s.project_id
        WHERE s.name='To Do'
    """)

    for pid, ptype, sec in cur.fetchall():
        for _ in range(random.randint(40,90)):
            created = datetime.utcnow() - timedelta(days=random.randint(1,180))
            due = random_due(created)
            completed = random.random() < .65

            cur.execute("""
                INSERT INTO tasks (
                    task_id, project_id, parent_task_id, section_id,
                    name, description, assignee_id, priority,
                    created_at, due_date, completed, completed_at
                )
                VALUES (
                    hex(randomblob(16)), ?, NULL, ?,
                    ?, ?, NULL, 'medium',
                    ?, ?, ?, NULL
                )
            """, (
                pid,
                sec,
                random.choice(POOLS[ptype]),
                random.choice(POOLS["descriptions"]),
                created,
                due,
                completed
            ))

    conn.commit()
    conn.close()
