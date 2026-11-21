import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.title("Interactive charts")
st.write(
    "Drag across the chart to select cities. The selection comes back to Python, so "
    "the table and the summary below follow it."
)


@st.cache_data
def make_cities(count: int, seed: int) -> pd.DataFrame:
    """Made-up city data. st.cache_data runs this once per input, then reuses the result."""
    rng = np.random.default_rng(seed)
    regions = rng.choice(["North", "South", "East", "West"], count)
    population = rng.lognormal(mean=12, sigma=0.8, size=count).round()
    income = 30_000 + population ** 0.35 * 400 + rng.normal(0, 6_000, count)
    return pd.DataFrame(
        {
            "city": [f"City {i + 1}" for i in range(count)],
            "region": regions,
            "population": population.astype(int),
            "median_income": income.round(-2).astype(int),
            "parks": rng.poisson(population / 40_000 + 2),
        }
    )


left, right = st.columns([1, 3])
with left:
    count = st.slider("Number of cities", 50, 500, 200, step=50)
    seed = st.number_input("Random seed", value=7, step=1)
    regions = st.pills(
        "Regions", ["North", "South", "East", "West"],
        selection_mode="multi", default=["North", "South", "East", "West"],
    )

data = make_cities(count, int(seed))
data = data[data["region"].isin(regions or [])]

brush = alt.selection_interval(name="brush")
chart = (
    alt.Chart(data)
    .mark_circle(size=70, opacity=0.8)
    .encode(
        x=alt.X("population:Q", scale=alt.Scale(type="log"), title="Population"),
        y=alt.Y("median_income:Q", title="Median income ($)"),
        color=alt.condition(brush, "region:N", alt.value("lightgray")),
        tooltip=["city", "region", "population", "median_income", "parks"],
    )
    .add_params(brush)
)

with right:
    event = st.altair_chart(chart, on_select="rerun", key="cities")

selection = event.selection.get("brush", {}) if event else {}
if selection:
    low_pop, high_pop = selection["population"]
    low_inc, high_inc = selection["median_income"]
    chosen = data[
        data["population"].between(low_pop, high_pop)
        & data["median_income"].between(low_inc, high_inc)
    ]
    st.subheader(f"{len(chosen)} cities selected")
else:
    chosen = data
    st.subheader("All cities (drag on the chart to select some)")

a, b, c = st.columns(3)
a.metric("Total population", f"{chosen['population'].sum():,}")
b.metric("Average income", f"${chosen['median_income'].mean():,.0f}" if len(chosen) else "–")
c.metric("Parks", f"{chosen['parks'].sum():,}")

st.bar_chart(chosen.groupby("region")["population"].sum(), horizontal=True)
st.dataframe(chosen, hide_index=True, width="stretch")
