from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_connection

tasks = Blueprint("tasks", __name__)

# ---------------- TASKS ---------------- #

@tasks.route("/tasks", methods=["GET", "POST"])
def task_page():

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = get_connection()
    cursor = conn.cursor()

    # -------- ADD TASK -------- #

    if request.method == "POST":

        task = request.form["task"]

        cursor.execute("""
        INSERT INTO tasks(username, task)
        VALUES(%s, %s)
        """, (username, task))

        conn.commit()

        conn.close()

        flash("Task Added Successfully!", "success")

        return redirect("/tasks")

    # -------- FETCH TASKS -------- #

    cursor.execute("""
    SELECT id, task, completed,
       created_at, completed_at
FROM tasks
WHERE username=%s
ORDER BY id DESC
    """, (username,))

    task_list = cursor.fetchall()

    conn.close()

    return render_template(
        "productivity/tasks.html",
        tasks=task_list
    )
# ---------------- COMPLETE TASK ---------------- #

@tasks.route("/complete_task/<int:task_id>")
def complete_task(task_id):

    if "username" not in session:
        return redirect("/login")
    
    username = session["username"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
UPDATE tasks
SET completed=TRUE,
    completed_at=CURRENT_TIMESTAMP
WHERE id=%s AND username=%s
""", (task_id, username)) 

    conn.commit()

    conn.close()

    flash("Task Completed!", "success")

    return redirect("/tasks")

# ---------------- DELETE TASK ---------------- #

@tasks.route("/delete_task/<int:task_id>")
def delete_task(task_id):

    if "username" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM tasks
    WHERE id=%s AND username=%s
    """, (task_id, session["username"]))

    conn.commit()

    conn.close()

    flash("Task Deleted!", "success")

    return redirect("/tasks")

