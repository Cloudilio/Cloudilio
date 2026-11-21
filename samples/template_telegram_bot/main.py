"""A Telegram bot that replies to messages, with a small status page.

Set TELEGRAM_BOT_TOKEN on the Environment tab (create a bot with @BotFather to get one), then deploy.
It uses long polling, so it needs no webhook or public URL, and only Python's standard library.
"""
import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
PORT = int(os.environ.get("PORT", "8000"))
IS_PREVIEW = os.environ.get("PYHOST_PREVIEW") == "1"

state = {"started": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()), "messages": 0, "last_error": None}


def api(method, **params):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(url, data=data, timeout=40) as response:
        return json.loads(response.read())


def reply_to(text):
    """Change this to make the bot do something useful."""
    text = (text or "").strip()
    if text == "/start":
        return "Hi! I'm running on Cloudilio. Send me any message and I'll echo it back."
    if text == "/help":
        return "Commands: /start, /help. Anything else gets echoed back."
    return f"You said: {text}"


def poll():
    offset = None
    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset
            updates = api("getUpdates", **params).get("result", [])
            for update in updates:
                offset = update["update_id"] + 1
                message = update.get("message") or {}
                if "text" in message:
                    api("sendMessage", chat_id=message["chat"]["id"], text=reply_to(message["text"]))
                    state["messages"] += 1
            state["last_error"] = None
        except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
            state["last_error"] = str(e)
            time.sleep(5)


class Status(BaseHTTPRequestHandler):
    def do_GET(self):
        if not TOKEN:
            body = "<h1>Telegram bot</h1><p>Add <code>TELEGRAM_BOT_TOKEN</code> on the Environment tab, then deploy.</p>"
        elif IS_PREVIEW:
            body = ("<h1>Telegram bot (preview)</h1><p>The preview doesn't talk to Telegram, so it can't answer "
                    "messages meant for the live bot. Deploy to put your changes live.</p>")
        else:
            body = (f"<h1>Telegram bot</h1><p>Running since {state['started']}. "
                    f"Messages answered: {state['messages']}.</p>"
                    + (f"<p>Last problem: {state['last_error']}</p>" if state["last_error"] else ""))
        payload = f"<!doctype html><meta charset=utf-8><body style='font-family:sans-serif;max-width:40rem;margin:2rem auto'>{body}".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    # Two copies polling the same bot would steal each other's messages, so previews don't poll
    if TOKEN and not IS_PREVIEW:
        threading.Thread(target=poll, daemon=True).start()
    print(f"Status page on port {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Status).serve_forever()
