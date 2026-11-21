# Streamlit Tour

A multi-page Streamlit app that shows what you can build with a few lines of Python,
ready to deploy on Cloudilio.

| Page | What it shows |
|---|---|
| Welcome | Widgets that update the page as you type |
| Interactive charts | Drag to select points on an Altair chart and use the selection in Python |
| Live dashboard | `st.fragment` refreshing one panel every second |
| Editable tables | `st.data_editor` with dropdowns, progress bars, live totals and CSV download |
| Chat interface | `st.chat_input`, `st.chat_message` and streamed replies |
| 3D map | A pydeck hexagon layer over thousands of points |
| Analyze a CSV | Upload a file for a summary and chart |
| Guestbook | Entries saved under `APP_DATA_DIR`, so they survive restarts and redeploys |

### Run it locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

### On Cloudilio
Cloudilio detects Streamlit from `requirements.txt` and runs
`streamlit run app.py --server.port 8000 --server.address 0.0.0.0 --server.headless true`.
Theme and upload limits come from `.streamlit/config.toml`. It runs comfortably on the
Starter plan's 512 MB.
