from flask import Flask, render_template, session, redirect
from dotenv import load_dotenv
import os
from db import get_connection, init_db

load_dotenv()
from routes.auth import auth
from routes.profile import profile
from routes.journal import journal
from routes.tasks import tasks
from routes.focus import focus
from routes.mood import mood
from routes.assistant import assistant

app = Flask(__name__)



app.secret_key = os.getenv("SECRET_KEY")

# ---------------- REGISTER BLUEPRINTS ---------------- #

app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(journal)
app.register_blueprint(tasks)
app.register_blueprint(focus)
app.register_blueprint(mood)
app.register_blueprint(assistant)

init_db()
# ---------------- HOME ---------------- #

@app.route("/")
def home():

    username = session.get("username")

    return render_template(
        "index.html",
        username=username
    )

# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")
    
    username = session["username"]
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
SELECT COUNT(*)
FROM tasks
WHERE username=%s
""", (username,))
    
    total_tasks = cursor.fetchone()[0]

    cursor.execute("""
SELECT COUNT(*)
FROM tasks
WHERE username=%s AND completed=TRUE
""", (username,))
    
    completed_tasks = cursor.fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    # -------- PRODUCTIVITY SCORE -------- #

    if total_tasks == 0:

        productivity_status = "No tasks yet"

    elif completed_tasks >= pending_tasks:

        productivity_status = "🔥 Highly Productive"

    elif pending_tasks > completed_tasks:

        productivity_status = "⚠️ Falling Behind"

    else:

        productivity_status = "🙂 Balanced Progress"

    cursor.execute("""
SELECT COUNT(*)
FROM journals
WHERE username=%s
""", (username,))
    
    journal_count = cursor.fetchone()[0]

    conn.close()
    


    return render_template(
        "dashboard/dashboard.html",
        username=session["username"], total_tasks=total_tasks,
    completed_tasks=completed_tasks,
    pending_tasks=pending_tasks,
    journal_count=journal_count,
    productivity_status=productivity_status
    )

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=False)
