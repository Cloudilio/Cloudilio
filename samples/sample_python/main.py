import os
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Standard persistent data directory allocation
DATA_DIR = os.environ.get("APP_DATA_DIR")
if not DATA_DIR:
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

try:
    os.makedirs(DATA_DIR, exist_ok=True)
except Exception:
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(DATA_DIR, exist_ok=True)

ACTIVITY_LOG_FILE = os.path.join(DATA_DIR, "worker_activity.log")

# Background worker thread state
worker_state = {
    "iterations": 0,
    "last_run": time.strftime("%Y-%m-%d %H:%M:%S"),
    "status": "active"
}


def background_worker_task():
    """Simulates a continuous background Python task (bot, scraper, or worker loop)."""
    while True:
        try:
            worker_state["iterations"] += 1
            now_str = time.strftime("%Y-%m-%d %H:%M:%S")
            worker_state["last_run"] = now_str
            with open(ACTIVITY_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{now_str}] Worker cycle #{worker_state['iterations']} completed.\n")
        except Exception as e:
            print(f"Worker task error: {e}", file=sys.stderr)
        time.sleep(5)


# Pure Python HTTP Server (no external web framework required)
class GeneralPythonHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean logging
        pass

    def do_GET(self):
        if self.path in ("/health", "/healthz"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "healthy", "service": "general-python-worker"}')
            return

        # Main Status & Dashboard Page
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # Read last 5 activity lines
        recent_activity = []
        if os.path.exists(ACTIVITY_LOG_FILE):
            try:
                with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    recent_activity = lines[-5:]
            except Exception:
                pass

        activity_html = "".join([f"<div style='font-family: monospace; font-size: 0.85rem; color: #475569;'>{line.strip()}</div>" for line in recent_activity]) or "<span style='color: #94a3b8;'>Starting first task cycle...</span>"

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>General Python App - Live on Cloudilio</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #1e293b; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }}
        .card {{ background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); max-width: 520px; width: 100%; text-align: center; }}
        .badge {{ background: #dcfce7; color: #15803d; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 0.85rem; display: inline-block; margin-bottom: 1rem; }}
        .metric-box {{ background: #f1f5f9; border-radius: 8px; padding: 1rem; margin: 1.25rem 0; text-align: left; }}
        .metric-title {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; font-weight: 600; margin-bottom: 0.5rem; }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">&bull; RUNNING</span>
        <h1 style="margin: 0 0 0.5rem 0; font-size: 1.75rem;">General Python App is Live!</h1>
        <p style="color: #64748b; margin-top: 0; font-size: 0.95rem;">
            Executing standard Python 3.12 without requiring any external web frameworks.
        </p>

        <div class="metric-box">
            <div class="metric-title">Background Worker Status</div>
            <div><strong>Cycles Completed:</strong> {worker_state['iterations']}</div>
            <div><strong>Last Active:</strong> {worker_state['last_run']} UTC</div>
            <div style="margin-top: 0.5rem;"><strong>Persistent Log Path:</strong> <code style="font-size: 0.75rem;">{ACTIVITY_LOG_FILE}</code></div>
        </div>

        <div class="metric-box">
            <div class="metric-title">Recent Task Output</div>
            {activity_html}
        </div>

        <p style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 0;">
            Health Check: <a href="/health" style="color: #3b82f6;">/health</a> &bull; Process: <code>python main.py</code>
        </p>
    </div>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))


def main():
    port = int(os.environ.get("PORT", 8000))

    # Launch background worker thread
    worker_thread = threading.Thread(target=background_worker_task, daemon=True)
    worker_thread.start()
    print(f"Background worker thread launched. Logging to {ACTIVITY_LOG_FILE}")

    # Launch HTTP Server on PORT
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, GeneralPythonHandler)
    print(f"General Python Server listening on http://0.0.0.0:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    main()
