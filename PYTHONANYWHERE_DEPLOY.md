# Deploy MindSyncAI on PythonAnywhere

PythonAnywhere is a good fit for simple Flask apps. For a free PythonAnywhere account, use SQLite. PostgreSQL on PythonAnywhere requires a paid account.

## Steps

1. Create or log in to your PythonAnywhere account.
2. Open a Bash console and clone the repo:

```bash
git clone https://github.com/tej191/MindSyncAI.git
cd MindSyncAI
```

3. Create a virtualenv and install dependencies:

```bash
mkvirtualenv --python=/usr/bin/python3.13 mindsyncai-venv
pip install -r requirements.txt
```

4. Go to the Web tab:
   - Add a new web app
   - Choose Manual configuration
   - Choose the same Python version used in the virtualenv
   - Set the virtualenv to `mindsyncai-venv`

5. Open the WSGI configuration file and replace its contents with the contents of `pythonanywhere_wsgi.py`.

6. In the WSGI file, replace:
   - `YOUR_PYTHONANYWHERE_USERNAME`
   - `SECRET_KEY`
   - `GROQ_API_KEY`

7. Reload the web app.

## Notes

- Do not set `DATABASE_URL` on a free PythonAnywhere account. The app will use SQLite at `SQLITE_PATH`.
- `api.groq.com` is currently on PythonAnywhere's free-account allowlist, so the AI assistant API should be reachable.
- Free PythonAnywhere web apps expire after 1 month if not renewed from the dashboard.
