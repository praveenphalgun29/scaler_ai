from src.utils.init_db import init_db
from src.generators.org import create_org
from src.generators.users import create_users
from src.generators.teams import create_teams, assign_team_members
from src.generators.projects import create_projects
from src.generators.sections import create_sections
from src.generators.tasks import create_tasks
from src.generators.comments import create_comments

def main():
    init_db()
    org_id=create_org()
    create_users(org_id)
    create_teams(org_id)
    assign_team_members()
    create_projects()
    create_sections()
    create_tasks()
    create_comments()
    print("Asana dataset ready.")

if __name__=="__main__":
    main()
