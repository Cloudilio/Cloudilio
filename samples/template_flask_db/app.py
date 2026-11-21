"""A Flask app that saves a form to a database: a small guestbook.

Entries are stored in SQLite inside APP_DATA_DIR, the folder Cloudilio keeps across deploys and restarts.
"""
import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, g, redirect, render_template, request, url_for

DATA_DIR = os.environ.get("APP_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
os.makedirs(DATA_DIR, exist_ok=True)
DATABASE = os.path.join(DATA_DIR, "guestbook.db")

app = Flask(__name__)


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute(
            "CREATE TABLE IF NOT EXISTS entries ("
            "id INTEGER PRIMARY KEY, name TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)"
        )
    return g.db


@app.teardown_appcontext
def close_db(_error):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()[:80]
        message = request.form.get("message", "").strip()[:1000]
        if not name or not message:
            error = "Please fill in both your name and a message."
        else:
            db().execute(
                "INSERT INTO entries (name, message, created_at) VALUES (?, ?, ?)",
                (name, message, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")),
            )
            db().commit()
            return redirect(url_for("index"))
    entries = db().execute("SELECT * FROM entries ORDER BY id DESC LIMIT 100").fetchall()
    return render_template("index.html", entries=entries, error=error,
                           preview=os.environ.get("PYHOST_PREVIEW") == "1")


@app.route("/health")
def health():
    db().execute("SELECT 1")
    return {"status": "ok"}
