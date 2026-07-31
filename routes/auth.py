from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

auth = Blueprint("auth", __name__)

# ---------------- REGISTER ---------------- #

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(username, password)
        VALUES(%s, %s)
        """, (username, hashed_password))

        conn.commit()
        conn.close()

        flash("Registration Successful!", "success")

        return redirect("/login")

    return render_template("auth/register.html")


# ---------------- LOGIN ---------------- #

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE username=%s
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):

            session["username"] = username

            flash("Login Successful!", "success")

            return redirect("/dashboard")

        else:

            flash("Invalid Username or Password", "danger")

    return render_template("auth/login.html")


# ---------------- LOGOUT ---------------- #

@auth.route("/logout")
def logout():

    session.pop("username", None)

    flash("Logged Out Successfully!", "success")

    return redirect("/login")
