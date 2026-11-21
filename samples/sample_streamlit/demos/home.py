import os
import platform

import streamlit as st

st.title("✨ Streamlit on Cloudilio")
st.write(
    "Streamlit turns a Python script into an interactive web app: no HTML, CSS or "
    "JavaScript. Every widget is one line of Python, and the page reruns from top to "
    "bottom whenever someone changes something. This app is a short tour."
)

col1, col2, col3 = st.columns(3)
col1.metric("Python", platform.python_version())
col2.metric("Streamlit", st.__version__)
col3.metric("Saved data folder", "Ready" if os.environ.get("APP_DATA_DIR") else "Local")

st.subheader("Try it: the whole page reacts as you type")
name = st.text_input("Your name", placeholder="Ada")
mood = st.select_slider("How's your day?", ["😫", "😕", "😐", "🙂", "🤩"], value="🙂")
if name:
    st.success(f"Hi {name} {mood}! That greeting is one `if` statement in Python.")

st.subheader("What's in this tour")
st.markdown(
    """
| Page | Shows off |
|---|---|
| **Interactive charts** | Drag to select points on a chart and read the selection back in Python |
| **Live dashboard** | A section that refreshes itself every second without reloading the page |
| **Editable tables** | A spreadsheet-style editor with progress bars, dropdowns and live totals |
| **Chat interface** | A chat app with streamed replies, the building block for AI assistants |
| **3D map** | Thousands of points drawn as 3D columns with pydeck |
| **Analyze a CSV** | Upload a file and get a summary and chart instantly |
| **Guestbook** | Messages saved to disk, so they survive restarts and redeploys |
"""
)

with st.expander("How this app is deployed on Cloudilio"):
    st.markdown(
        """
- Cloudilio sees `streamlit` in `requirements.txt` and runs `streamlit run app.py`.
- Theme and upload limits come from `.streamlit/config.toml`.
- Files written to the folder in the `APP_DATA_DIR` environment variable are kept
  across restarts and redeploys. Everything else in the container is read-only,
  apart from a small `/tmp`.
"""
    )
