import uuid
from datetime import datetime
from src.utils.db import get_connection

ORG_NAME = "Vertexloop AI"
ORG_DOMAIN = "vertexloop.ai"

def create_org():
    conn = get_connection()
    cur = conn.cursor()

    # Check if org already exists
    cur.execute("SELECT org_id FROM organizations WHERE domain = ?", (ORG_DOMAIN,))
    row = cur.fetchone()

    if row:
        conn.close()
        return row[0]

    org_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO organizations (org_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
    """, (org_id, ORG_NAME, ORG_DOMAIN, datetime.utcnow()))

    conn.commit()
    conn.close()
    return org_id
