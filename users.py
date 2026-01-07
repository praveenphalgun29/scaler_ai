import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from src.utils.db import get_connection

fake = Faker()

DEPARTMENTS = [
    ("Engineering", 3600),
    ("Product", 800),
    ("Marketing", 800),
    ("Sales", 800),
    ("Operations", 800),
    ("Support", 800),
    ("HR & Finance", 400),
]

TITLES = {
    "Engineering": ["Software Engineer", "Senior Software Engineer", "Tech Lead", "QA Engineer", "DevOps Engineer"],
    "Product": ["Product Manager", "Associate PM"],
    "Marketing": ["Marketing Manager", "Content Strategist", "SEO Specialist"],
    "Sales": ["Sales Executive", "Account Manager"],
    "Operations": ["Operations Manager", "Compliance Officer"],
    "Support": ["Support Engineer", "Customer Success Manager"],
    "HR & Finance": ["HR Manager", "Finance Analyst"]
}

def random_hire_date():
    return fake.date_between(start_date="-3y", end_date="today")

def create_users(org_id):
    conn = get_connection()
    cur = conn.cursor()

    # Prevent duplicate generation
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    for dept, count in DEPARTMENTS:
        for _ in range(count):
            user_id = str(uuid.uuid4())   # generate ID first
            name = fake.name()
            email = f"{name.lower().replace(' ', '.')}.{user_id[:5]}@vertexloop.ai"
            title = random.choice(TITLES[dept])
            hire_date = random_hire_date()

            cur.execute("""
                INSERT INTO users (user_id, org_id, full_name, email, department, title, hire_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
            """, (user_id, org_id, name, email, dept, title, hire_date))

    conn.commit()
    conn.close()
