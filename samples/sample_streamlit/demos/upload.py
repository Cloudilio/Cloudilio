import io

import numpy as np
import pandas as pd
import streamlit as st

st.title("Analyze a CSV")
st.write("Drop in a CSV file and get a summary and a chart. No file handy? Use the example.")


@st.cache_data
def example_csv() -> bytes:
    rng = np.random.default_rng(3)
    days = pd.date_range("2026-01-01", periods=120, freq="D")
    frame = pd.DataFrame(
        {
            "date": days,
            "visitors": (500 + np.arange(120) * 4 + rng.normal(0, 60, 120)).round().astype(int),
            "signups": rng.poisson(25, 120),
            "channel": rng.choice(["Search", "Social", "Email"], 120),
        }
    )
    return frame.to_csv(index=False).encode("utf-8")


uploaded = st.file_uploader("CSV file", type=["csv"])
use_example = st.toggle("Use the example file", value=uploaded is None)
st.download_button("Download the example", example_csv(), file_name="example.csv", mime="text/csv")

if uploaded is not None and not use_example:
    source = uploaded
elif use_example:
    source = io.BytesIO(example_csv())
else:
    st.stop()

try:
    frame = pd.read_csv(source)
except Exception as error:  # A bad file shouldn't crash the page
    st.error(f"Couldn't read that file as CSV: {error}")
    st.stop()

# Treat columns that look like dates as dates
for column in frame.columns:
    if frame[column].dtype == object:
        parsed = pd.to_datetime(frame[column], errors="coerce", format="mixed")
        if parsed.notna().mean() > 0.9:
            frame[column] = parsed

a, b, c = st.columns(3)
a.metric("Rows", f"{len(frame):,}")
b.metric("Columns", len(frame.columns))
c.metric("Missing values", f"{int(frame.isna().sum().sum()):,}")

tab_data, tab_summary, tab_chart = st.tabs(["Data", "Summary", "Chart"])
with tab_data:
    st.dataframe(frame, width="stretch", hide_index=True)
with tab_summary:
    st.dataframe(frame.describe(include="all").T, width="stretch")
with tab_chart:
    numeric = frame.select_dtypes("number").columns.tolist()
    if not numeric:
        st.info("This file has no number columns to chart.")
    else:
        x_options = ["(row number)"] + [col for col in frame.columns if col not in numeric]
        x = st.selectbox("X axis", x_options)
        ys = st.multiselect("Values", numeric, default=numeric[:2])
        if ys:
            chart_data = frame if x == "(row number)" else frame.set_index(x)
            st.line_chart(chart_data[ys])
