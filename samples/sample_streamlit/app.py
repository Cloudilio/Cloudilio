"""Cloudilio sample: a tour of what Streamlit can do.

Each page lives in demos/. Run it locally with:
    pip install -r requirements.txt
    streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="Streamlit on Cloudilio", page_icon="✨", layout="wide")

pages = {
    "Start here": [
        st.Page("demos/home.py", title="Welcome", icon=":material/waving_hand:", default=True),
    ],
    "Demos": [
        st.Page("demos/charts.py", title="Interactive charts", icon=":material/insights:"),
        st.Page("demos/live.py", title="Live dashboard", icon=":material/monitor_heart:"),
        st.Page("demos/data_editor.py", title="Editable tables", icon=":material/table_edit:"),
        st.Page("demos/chat.py", title="Chat interface", icon=":material/chat:"),
        st.Page("demos/map.py", title="3D map", icon=":material/map:"),
        st.Page("demos/upload.py", title="Analyze a CSV", icon=":material/upload_file:"),
        st.Page("demos/guestbook.py", title="Guestbook (saved data)", icon=":material/menu_book:"),
    ],
}

st.navigation(pages).run()
