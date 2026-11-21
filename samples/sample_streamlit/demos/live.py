import time
from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.title("Live dashboard")
st.write(
    "The panel below is an `st.fragment` that reruns itself every second. Only that "
    "panel refreshes, so the controls here keep their values while it updates."
)

running = st.toggle("Live updates", value=True)
volatility = st.slider("Volatility", 0.1, 3.0, 1.0)

if "prices" not in st.session_state:
    st.session_state.prices = pd.DataFrame(
        {"Server A": [100.0], "Server B": [100.0], "Server C": [100.0]},
        index=[datetime.now()],
    )


@st.fragment(run_every=1.0 if running else None)
def live_panel():
    prices = st.session_state.prices
    if running:
        step = np.random.normal(0, volatility, size=3)
        new_row = pd.DataFrame([prices.iloc[-1].values + step], columns=prices.columns,
                               index=[datetime.now()])
        prices = pd.concat([prices, new_row]).tail(60)  # Keep the last minute
        st.session_state.prices = prices

    latest, previous = prices.iloc[-1], prices.iloc[max(len(prices) - 2, 0)]
    cols = st.columns(3)
    for col, name in zip(cols, prices.columns):
        col.metric(f"{name} requests/s", f"{latest[name]:.1f}", f"{latest[name] - previous[name]:+.1f}")
    # Altair, so the y axis fits the data instead of starting at zero
    long = prices.rename_axis("time").reset_index().melt("time", var_name="server", value_name="requests/s")
    chart = (
        alt.Chart(long)
        .mark_line(strokeWidth=2)
        .encode(
            x=alt.X("time:T", title=None),
            y=alt.Y("requests/s:Q", scale=alt.Scale(zero=False)),
            color="server:N",
        )
        .properties(height=320)
    )
    st.altair_chart(chart)
    st.caption(f"Last updated {time.strftime('%H:%M:%S')}")


live_panel()

if st.button("Reset"):
    del st.session_state.prices
    st.rerun()
