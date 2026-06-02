from flask import Blueprint, render_template, request, redirect
from flask import session, flash
import sqlite3

mood = Blueprint("mood", __name__)

# ---------------- MOOD TRACKER ---------------- #

@mood.route("/mood", methods=["GET", "POST"])
def mood_page():

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # -------- CREATE TABLE -------- #

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS moods(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        mood TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------- SAVE MOOD -------- #

    if request.method == "POST":

        selected_mood = request.form["mood"]

        cursor.execute("""
        INSERT INTO moods(username, mood)
        VALUES(?, ?)
        """, (username, selected_mood))

        conn.commit()

        flash("Mood Saved Successfully!", "success")

        conn.close()

        return redirect("/mood")

    # -------- FETCH MOODS -------- #

    cursor.execute("""
    SELECT mood, created_at
    FROM moods
    WHERE username=?
    ORDER BY created_at DESC
    """, (username,))

    mood_list = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard/mood.html",
        moods=mood_list
    )