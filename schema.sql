--ORGANIZATION
CREATE TABLE IF NOT EXISTS organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL
);

--USERS
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    title TEXT NOT NULL,
    hire_date DATE NOT NULL,
    status TEXT CHECK(status IN ('active','on_leave','exited')) DEFAULT 'active',
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

--TEAMS
CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

--TEAM MEMBERSHIPS
CREATE TABLE IF NOT EXISTS team_memberships (
    user_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    role TEXT CHECK(role IN ('member','lead')) DEFAULT 'member',
    PRIMARY KEY (user_id, team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

--PROJECTS
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    project_type TEXT CHECK(project_type IN ('sprint','campaign','ops','backlog','support','hr','sales','product')),
    start_date DATE NOT NULL,
    end_date DATE,
    status TEXT CHECK(status IN ('active','archived')) DEFAULT 'active',
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

--SECTIONS
CREATE TABLE IF NOT EXISTS sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

--TASKS (with hierarchy)
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    parent_task_id TEXT,
    section_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    priority TEXT CHECK(priority IN ('low','medium','high')) DEFAULT 'medium',
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

--COMMENTS
CREATE TABLE IF NOT EXISTS comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

