import uuid
import random
from datetime import date, timedelta
from src.utils.db import get_connection

PROJECT_TEMPLATES = {
    "Engineering": ["Q{} Platform Sprint", "Bug Backlog Q{}", "Infra Upgrade Q{}"],
    "Marketing": ["{} Marketing Campaign", "Website Revamp {}", "Product Launch {}"],
    "Sales": ["{} Sales Pipeline", "Enterprise Deals {}", "SMB Outreach {}"],
    "Operations": ["Vendor Audit {}", "Compliance Review {}"],
    "Support": ["Customer Ticket Backlog {}", "Escalations {}"],
    "HR & Finance": ["Hiring Drive {}", "Payroll Processing {}"],
    "Product": ["Product Roadmap {}", "Feature Planning {}"]
}

PROJECT_TYPE_MAP = {
    "Engineering": "sprint",
    "Marketing": "campaign",
    "Sales": "sales",
    "Operations": "ops",
    "Support": "support",
    "HR & Finance": "hr",
    "Product": "product"
}

def create_projects():
    conn = get_connection()
    cur = conn.cursor()

    # Avoid duplicates
    cur.execute("SELECT COUNT(*) FROM projects")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    cur.execute("SELECT team_id, department FROM teams")
    teams = cur.fetchall()

    for team_id, dept in teams:
        for _ in range(random.randint(8, 15)):
            template = random.choice(PROJECT_TEMPLATES[dept])
            quarter = random.choice(["Q1", "Q2", "Q3", "Q4"])
            name = template.format(quarter)

            start = date.today() - timedelta(days=random.randint(30, 180))
            end = start + timedelta(days=random.randint(30, 120))

            project_id = str(uuid.uuid4())
            project_type = PROJECT_TYPE_MAP[dept]

            cur.execute("""
                INSERT INTO projects (project_id, team_id, name, project_type, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (project_id, team_id, name, project_type, start, end))

    conn.commit()
    conn.close()
