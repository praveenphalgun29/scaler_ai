import random
from datetime import timedelta, datetime
from src.utils.db import get_connection
from src.utils.hf_pool import load_pools

POOLS = load_pools()

def create_comments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM comments")

    # Fetch task creation times (strings)
    cur.execute("SELECT task_id, created_at FROM tasks")
    tasks = cur.fetchall()

    for tid, task_created in tasks:
        # Convert SQLite string to datetime
        task_created = datetime.fromisoformat(task_created)

        n = random.randint(1,4)
        for _ in range(n):
            body = random.choice(POOLS["comments"])
            offset = timedelta(hours=random.randint(2,336))
            created_at = task_created + offset

            cur.execute("""
                INSERT INTO comments (comment_id, task_id, author_id, body, created_at)
                VALUES (
                    hex(randomblob(16)), ?, 
                    (SELECT user_id FROM users ORDER BY RANDOM() LIMIT 1),
                    ?, ?
                )
            """, (tid, body, created_at))

    conn.commit()
    conn.close()
