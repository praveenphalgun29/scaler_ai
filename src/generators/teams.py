import uuid
import random
from src.utils.db import get_connection

ENGINEERING_TEAMS = [
    "Backend Platform", "Mobile Apps", "Frontend Web", "AI ML",
    "Data Platform", "DevOps", "QA Automation", "Infra Reliability"
]

MARKETING_TEAMS = ["Content", "SEO", "Paid Ads", "Brand"]
SALES_TEAMS = ["SMB Sales", "Enterprise Sales"]
OPS_TEAMS = ["Compliance", "Vendor Management"]
SUPPORT_TEAMS = ["Tier 1 Support", "Tier 2 Support"]
HR_TEAMS = ["Recruitment", "Payroll"]

DEPT_TEAMS = {
    "Engineering": ENGINEERING_TEAMS,
    "Marketing": MARKETING_TEAMS,
    "Sales": SALES_TEAMS,
    "Operations": OPS_TEAMS,
    "Support": SUPPORT_TEAMS,
    "HR & Finance": HR_TEAMS,
    "Product": ["Product Management"]
}

def create_teams(org_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM teams")
    cur.execute("DELETE FROM team_memberships")

    for dept, teams in DEPT_TEAMS.items():
        for team_name in teams:
            team_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO teams (team_id, org_id, name, department)
                VALUES (?, ?, ?, ?)
            """, (team_id, org_id, team_name, dept))

    conn.commit()
    conn.close()

def assign_team_members():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT team_id, department FROM teams")
    teams = cur.fetchall()

    for team_id, dept in teams:
        cur.execute("SELECT user_id FROM users WHERE department = ?", (dept,))
        users = [u[0] for u in cur.fetchall()]
        size = random.randint(8, 14)
        members = random.sample(users, min(size, len(users)))

        for i, uid in enumerate(members):
            role = "lead" if i == 0 else "member"
            cur.execute("""
                INSERT INTO team_memberships (user_id, team_id, role)
                VALUES (?, ?, ?)
            """, (uid, team_id, role))

    conn.commit()
    conn.close()
