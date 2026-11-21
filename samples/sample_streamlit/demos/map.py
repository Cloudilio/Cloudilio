import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

st.title("3D map")
st.write(
    "pydeck draws large datasets on a map with the GPU. Each column counts the made-up "
    "taxi pickups in its area. Hold right-click (or Ctrl and drag) to tilt and rotate."
)

CITIES = {
    "New York": (40.7380, -73.9900),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6812, 139.7671),
    "San Francisco": (37.7749, -122.4194),
}

c1, c2, c3 = st.columns(3)
city = c1.selectbox("City", list(CITIES))
points = c2.slider("Pickups", 1_000, 20_000, 8_000, step=1_000)
radius = c3.slider("Column size (m)", 50, 400, 150, step=50)

lat, lon = CITIES[city]


@st.cache_data
def pickups(lat: float, lon: float, count: int) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    # A few busy neighbourhoods plus background noise
    centres = rng.normal([lat, lon], 0.015, size=(6, 2))
    picks = centres[rng.integers(0, 6, count)] + rng.normal(0, 0.006, size=(count, 2))
    return pd.DataFrame(picks, columns=["lat", "lon"])


data = pickups(lat, lon, points)

st.pydeck_chart(
    pdk.Deck(
        map_style=None,  # Streamlit's own base map, no API key needed
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=11, pitch=50, bearing=-15),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position="[lon, lat]",
                radius=radius,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
                pickable=True,
                coverage=0.9,
            )
        ],
        tooltip={"text": "{elevationValue} pickups"},
    ),
    height=520,
)
st.caption(f"{points:,} points around {city}, generated in Python and drawn in your browser.")
