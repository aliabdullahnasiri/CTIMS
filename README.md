CTIMS — Comprehensive Technical Overview

Project overview

CTIMS is a Flask-based Campus/College/Training Information Management System (CTIMS) built with modular blueprints for auth, admin, and API. It uses SQLAlchemy ORM, Flask-Migrate (Alembic), Flask-Login for authentication, and Flask-Bcrypt for password hashing. The app supports role-based access control (RBAC) with bitmask permissions, file uploads, and a template-driven admin interface.

Key features

- Modular Flask application factory (create_app)
- Role-based permissions (Role / Permission models, dynamic permission registration)
- User management: users, phones, files, one-to-one student/teacher/employee profiles
- Admin UI protected by permission checks
- RESTful API blueprints under /api
- Alembic migrations via Flask-Migrate
- Environment-driven configuration via .env

Repository layout (top-level)

- manage.py — development entrypoint (runs create_app())
- wsgi.py — production WSGI entrypoint
- requirements.txt — Python dependencies
- app/ — main application package
  - __init__.py — application factory and blueprint registration
  - config.py — Config class (env-driven settings)
  - const.py — derived constants
  - extensions/ — db, bcrypt, login_manager, migrate initializers
  - blueprints/ — auth, admin, api blueprints and route modules
  - models/ — SQLAlchemy models (users, roles, permissions, domain models)
  - forms/ — WTForms forms
  - templates/, static/ — UI templates and assets
- migrations/ — Alembic migrations

Architecture and component interactions

The following Mermaid diagram shows the high-level architecture and runtime interactions. Render it with any Mermaid-capable renderer (in Markdown viewers or mermaid.live).

```mermaid
flowchart LR
  subgraph Web
    Browser -->|HTTP(S)| Nginx["Nginx / Reverse Proxy"]
    Nginx -->|proxied| Gunicorn["Gunicorn / uWSGI (WSGI)"]
    Gunicorn --> FlaskApp["Flask App (create_app)"]
  end

  subgraph AppInternals
    FlaskApp --> Extensions["Flask Extensions\n(SQLAlchemy, Migrate, Bcrypt, LoginManager)"]
    FlaskApp --> Blueprints["Blueprints: /auth, /admin, /api"]
    Blueprints --> Models["SQLAlchemy Models: User, Role, Permission, File, Phone, Student, Teacher, etc."]
    Models -->|migrations| Alembic["Alembic / migrations/"]
    Blueprints --> Templates["Jinja templates (admin UI)"]
    FlaskApp --> Static["static files & uploads (app/static/uploads)"]
  end

  subgraph Persistence
    Models -->|ORM| Postgres["PostgreSQL (prod) / SQLite (dev)"]
    Static -->|files| FileStore["Local uploads or S3-compatible storage"]
  end

  Browser -->|API calls| Blueprints
  FlaskApp -.->|context_processor| Templates

  classDef infra fill:#f9f,stroke:#333,stroke-width:1px;
  Nginx,Gunicorn,Postgres class infra
```

Data model summary (ER-style)

- users (User)
  - uid (primary UID helper provided by base model)
  - user_name, email, password_hash, first_name, last_name, birthday, avatar_path
  - relationships: phones (1..*), files (1..*), roles (many-to-many), student/teacher/employee (0..1)

- roles (Role)
  - name, description, default
  - relationships: permissions (many-to-many), users (many-to-many)

- permissions (Permission)
  - name, description, permission (hex string)
  - Permission.permissions maintained at runtime; stored values are hex bitmasks

- pivot tables
  - users_roles (user_id, role_id)
  - roles_permissions (role_id, permission_id)

- supporting models
  - files (File) — file metadata + link to user
  - phones (Phone) — phone numbers per user
  - student, teacher, employee, attendance, exam, result: domain-specific tables

Security notes & recommendations

- Replace eval(self.permission) in Permission.hex_permission with int(self.permission, 16) to avoid executing arbitrary code; avoid eval entirely when parsing stored permission values.
- Ensure SECRET_KEY is set to a strong value in production environment variables; remove the weak default from production.
- Use PostgreSQL (or another robust RDBMS) in production. Keep SQLite only for local development.
- Add CSRF protection with Flask-WTF's CSRFProtect if not already enabled.
- Add rate-limiting and account lockout for login endpoints to mitigate brute-force attacks.
- Store sensitive credentials in environment variables or a secret manager (do not commit to repo).

Configuration

Key environment variables (from app/config.py):

- PROJECT_TITLE — project title (default: Flask Project)
- SECRET_KEY — Flask secret key (REQUIRED in prod)
- DATABASE_URL — SQLAlchemy DB URI (default: sqlite:///dev.db)
- SQLALCHEMY_ECHO — enable SQL echo
- UPLOAD_FOLDER — path for uploads (default: app/static/uploads)
- FLASKY_ADMIN — email that becomes auto-administrator

Setup and local development

1. Create a virtualenv (recommended Python 3.12+):

   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. Create .env file with environment overrides (example):

   SECRET_KEY=replace-with-secure-key
   DATABASE_URL=sqlite:///dev.db
   PROJECT_TITLE=CTIMS
   FLASKY_ADMIN=you@example.com

4. Initialize DB and run migrations (Flask-Migrate):

   flask db init   # only if migrations not setup
   flask db migrate -m "Initial"
   flask db upgrade

5. Run the app for development:

   python manage.py

Running tests

- Add pytest to requirements and create tests/ to cover core features: model helpers (password hashing, role/permission aggregation), auth flows, and API endpoints. Run with:

  pytest -q

Deployment suggestions

- Use Gunicorn behind Nginx. Example Gunicorn systemd service or Docker image.
- Use environment variables for configuration and secrets; enable secure HTTPS via Nginx/Cloud provider.
- Use PostgreSQL in production; enable regular backups. Use connection pooling (pgbouncer) for high scale.
- Consider storing uploads in S3-compatible storage; serve via CDN.

Developer notes & next steps

- Improve permission parsing to remove eval (security fix).
- Add Dockerfile and docker-compose for local dev and production profiles.
- Add unit and integration tests (pytest) and linting (black, isort, flake8/mypy).
- Add GitHub Actions CI: run tests and linters on push/PR.
- Consider providing OpenAPI spec for /api endpoints.

Contact & author

Developed by: Ali Abdullah Nasiri
