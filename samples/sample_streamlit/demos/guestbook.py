import json
import os
import threading
from datetime import datetime, timezone

import streamlit as st

# Cloudilio keeps this folder across restarts and redeploys. Locally, it falls back to ./data.
DATA_DIR = os.environ.get("APP_DATA_DIR") or os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
GUESTBOOK = os.path.join(DATA_DIR, "guestbook.json")
MAX_ENTRIES = 200
_lock = threading.Lock()  # Several visitors can sign at the same moment


def load_entries() -> list:
    try:
        with open(GUESTBOOK, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def add_entry(name: str, message: str, rating: int) -> None:
    with _lock:
        entries = load_entries()
        entries.append({
            "name": name, "message": message, "rating": rating,
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
        os.makedirs(DATA_DIR, exist_ok=True)
        temporary = GUESTBOOK + ".tmp"
        with open(temporary, "w", encoding="utf-8") as f:
            json.dump(entries[-MAX_ENTRIES:], f)
        os.replace(temporary, GUESTBOOK)  # Never leaves a half-written file


st.title("Guestbook")
st.write(
    "Messages are saved to a file in the app's data folder, so they're still here after "
    "a restart or a redeploy, and every visitor sees the same list."
)

with st.form("sign", clear_on_submit=True):
    name = st.text_input("Name", max_chars=40)
    message = st.text_area("Message", max_chars=280)
    st.write("How do you like Streamlit?")
    rating = st.feedback("stars")
    if st.form_submit_button("Sign the guestbook", type="primary"):
        if not name.strip() or not message.strip():
            st.warning("Please fill in your name and a message.")
        else:
            add_entry(name.strip(), message.strip(), rating + 1 if rating is not None else 0)
            st.toast("Thanks for signing!", icon="🎉")

entries = load_entries()
st.subheader(f"{len(entries)} signature{'s' if len(entries) != 1 else ''}")
for entry in reversed(entries):
    with st.container(border=True):
        stars = "⭐" * entry.get("rating", 0)
        when = datetime.fromisoformat(entry["at"]).strftime("%d %b %Y, %H:%M UTC")
        st.markdown(f"**{entry['name']}** {stars}")
        st.write(entry["message"])
        st.caption(when)

st.caption(f"Saved in `{GUESTBOOK}`")
