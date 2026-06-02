from typing import Any

from flask import Blueprint, render_template, request, session, redirect
import sqlite3
import requests
import markdown
import os
from dotenv import load_dotenv

load_dotenv()

assistant = Blueprint("assistant", __name__)

# ---------------- AI ASSISTANT ---------------- #

@assistant.route("/assistant", methods=["GET", "POST"])
def ai_assistant():

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # -------- CREATE CHAT TABLE -------- #

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        role TEXT,

        message TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------- USER SENDS MESSAGE -------- #

    if request.method == "POST":

        user_message = request.form["message"].strip()

        if not user_message:
            return redirect("/assistant")

        # SAVE USER MESSAGE

        cursor.execute("""
        INSERT INTO chat_messages(username, role, message)
        VALUES(?, ?, ?)
        """, (username, "user", user_message))

        conn.commit()

        # GET RECENT CHAT HISTORY

        cursor.execute("""
        SELECT role, message
        FROM chat_messages
        WHERE username=?
        ORDER BY id DESC
        LIMIT 10
        """, (username,))

        previous_messages = cursor.fetchall()

        # SEND TO OLLAMA

        groq_api_key = os.getenv("GROQ_API_KEY")

        headers = {

    "Authorization": f"Bearer {groq_api_key}",

    "Content-Type": "application/json"
}   
        
        messages = [

    {
        "role": "system",
        "content": """
        You are MindSync AI.

        You help students with:
        - productivity
        - coding
        - focus
        - consistency
        - learning
        - mental wellness

        Rules:
        - give beginner friendly answers
        - explain clearly
        - format properly
        - avoid hallucinations
        """
    }
]       
        for role, message in reversed(previous_messages):

            if role == "user":

                messages.append({
            "role": "user",
            "content": message
        })

            else:

                messages.append({
            "role": "assistant",
            "content": message
        })

        payload = {

    "model": "llama-3.1-8b-instant",

    "messages": messages
}

        groq_response = requests.post(

    "https://api.groq.com/openai/v1/chat/completions",

    headers=headers,

    json=payload
)
        
        try:

            data = groq_response.json()

            raw_response = data["choices"][0]["message"]["content"]

        except Exception:

            raw_response = "Sorry, AI service is currently unavailable."
        # CONVERT MARKDOWN TO HTML

        ai_message = markdown.markdown(raw_response)

        # SAVE AI RESPONSE

        cursor.execute("""
        INSERT INTO chat_messages(username, role, message)
        VALUES(?, ?, ?)
        """, (username, "ai", ai_message))

        conn.commit()


        return redirect("/assistant")

    # -------- FETCH USER CHAT ONLY -------- #

    cursor.execute("""
    SELECT role, message, created_at
    FROM chat_messages
    WHERE username=?
    ORDER BY id ASC
    """, (username,))

    chat_history = cursor.fetchall()

    conn.close()

    return render_template(

        "assistant/assistant.html",

        chat_history=chat_history
    )

# -------- CHAT CLEAR BUTTON -------- #

@assistant.route("/clear_chat")
def clear_chat():

    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM chat_messages
    WHERE username=?
    """, (username,))

    conn.commit()
    conn.close()

    return redirect("/assistant")



