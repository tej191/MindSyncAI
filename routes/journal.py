from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3

journal = Blueprint("journal", __name__)

# ---------------- JOURNAL ---------------- #

@journal.route("/journal", methods=["GET", "POST"])
def journal_page():

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # -------- CREATE JOURNAL TABLE -------- #

    cursor.execute("""
   CREATE TABLE IF NOT EXISTS journals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
)
    """)

    # -------- SAVE JOURNAL ENTRY -------- #

    if request.method == "POST":

        content = request.form["content"]

        cursor.execute("""
        INSERT INTO journals(username, content)
        VALUES(?, ?)
        """, (username, content))

        conn.commit()

        flash("Journal Entry Added!", "success")

        return redirect("/journal")
    

    # -------- FETCH USER ENTRIES -------- #

    cursor.execute("""
    SELECT id,content, created_at, updated_at
    FROM journals
    WHERE username=?
    ORDER BY created_at DESC
    """, (username,))

    entries = cursor.fetchall()

    conn.close()

    return render_template(
        "productivity/journal/journal.html",
        entries=entries
    )

# ---------------- DELETE JOURNAL ---------------- #

@journal.route("/delete_journal/<int:entry_id>")
def delete_journal(entry_id):

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM journals
    WHERE id=? AND username=?
    """, (entry_id, username))

    conn.commit()

    conn.close()

    flash("Journal Entry Deleted!", "success")

    return redirect("/journal")


# ---------------- EDIT JOURNAL ---------------- #

@journal.route("/edit_journal/<int:entry_id>", methods=["GET", "POST"])
def edit_journal(entry_id):

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # -------- UPDATE ENTRY -------- #

    if request.method == "POST":

        updated_content = request.form["content"]

        cursor.execute("""
        UPDATE journals
SET content=?,
    updated_at=CURRENT_TIMESTAMP
WHERE id=? AND username=?
        """, (updated_content, entry_id, username))

        conn.commit()

        conn.close()

        flash("Journal Updated Successfully!", "success")

        return redirect("/journal")

    # -------- FETCH CURRENT ENTRY -------- #

    cursor.execute("""
    SELECT id, content, created_at
    FROM journals
    WHERE id=? AND username=?
    """, (entry_id, username))

    entry = cursor.fetchone()

    conn.close()

    return render_template(
        "productivity/journal/edit_journal.html",
        entry=entry
    )