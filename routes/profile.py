from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_connection

profile = Blueprint("profile", __name__)

# ---------------- PROFILE ---------------- #

@profile.route("/profile", methods=["GET", "POST"])
def user_profile():

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        bio = request.form["bio"]
        goal = request.form["goal"]

        cursor.execute("""
        UPDATE users
        SET bio=%s, goal=%s
        WHERE username=%s
        """, (bio, goal, username))

        conn.commit()

        flash("Profile Updated!", "success")

    cursor.execute("""
    SELECT bio, goal FROM users
    WHERE username=%s
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    bio = user[0] if user[0] else ""
    goal = user[1] if user[1] else ""

    return render_template(
        "dashboard/profile.html",
        bio=bio,
        goal=goal
    )
