import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# Standard persistent data directory
DATA_DIR = os.environ.get("APP_DATA_DIR", "/app/data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "flask_store.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO page_views DEFAULT VALUES")
    conn.commit()
    cursor.execute("SELECT count(*) FROM page_views")
    view_count = cursor.fetchone()[0]
    conn.close()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask App - Live on Cloudilio</title>
        <style>
            body {{ font-family: sans-serif; background: #f8fafc; color: #1e293b; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
            .card {{ background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); text-align: center; max-width: 480px; }}
            .badge {{ background: #dcfce7; color: #15803d; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 0.85rem; }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">&bull; RUNNING</span>
            <h1>Flask is Live!</h1>
            <p>Your Python application was deployed successfully with zero server configuration.</p>
            <p><strong>Persistent Page Views (SQLite):</strong> {view_count}</p>
            <p style="color: #64748b; font-size: 0.85rem;">Data saved in <code>{DB_PATH}</code> survives restarts.</p>
        </div>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "flask-app"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
