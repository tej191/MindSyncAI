from flask import Blueprint, render_template, session, redirect

focus = Blueprint("focus", __name__)

# ---------------- FOCUS PAGE ---------------- #

@focus.route("/focus")
def focus_page():

    if "username" not in session:
        return redirect("/login")

    return render_template("productivity/focus.html")