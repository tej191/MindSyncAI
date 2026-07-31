import os
import sys


project_home = "/home/YOUR_PYTHONANYWHERE_USERNAME/MindSyncAI"

if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault("SECRET_KEY", "replace-with-a-long-random-secret")
os.environ.setdefault("GROQ_API_KEY", "replace-with-your-rotated-groq-api-key")
os.environ.setdefault("SQLITE_PATH", f"{project_home}/database.db")

from app import app as application
