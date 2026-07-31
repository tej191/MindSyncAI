# Deploy MindSyncAI on Koyeb

MindSyncAI is ready for a Koyeb GitHub deployment as a Python Flask web service.

## Required Koyeb setup

1. Create a free PostgreSQL Database Service in Koyeb.
2. Copy the database connection string from the database Connection Details page.
3. Create a new Web Service from GitHub:
   - Repository: `tej191/MindSyncAI`
   - Branch: `main`
   - Builder: Buildpack
   - Instance: Free, if available
   - Exposed port: use Koyeb's generated `PORT`
4. Add these environment variables to the Web Service:
   - `DATABASE_URL`: the Koyeb PostgreSQL connection string
   - `SECRET_KEY`: a long random secret value
   - `GROQ_API_KEY`: your rotated Groq API key
5. Deploy.

## Why this works

- `requirements.txt` includes Flask, Gunicorn, and `psycopg2-binary`.
- `Procfile` starts the app with `gunicorn --bind :$PORT app:app`.
- `db.py` creates the PostgreSQL tables on app startup.

## Optional SQLite data migration

After setting `DATABASE_URL` locally, run:

```powershell
venv\Scripts\python.exe scripts\migrate_sqlite_to_postgres.py
```
