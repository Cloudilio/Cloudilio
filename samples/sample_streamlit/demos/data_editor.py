import pandas as pd
import streamlit as st

st.title("Editable tables")
st.write(
    "`st.data_editor` gives you a spreadsheet in one line. Edit cells, add rows at the "
    "bottom, or select rows and press Delete. The totals underneath recalculate as you go."
)

if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(
        [
            {"task": "Write the landing page", "owner": "Ada", "status": "Done", "hours": 6, "progress": 100, "urgent": False},
            {"task": "Set up payments", "owner": "Grace", "status": "In progress", "hours": 10, "progress": 60, "urgent": True},
            {"task": "Launch announcement", "owner": "Alan", "status": "Not started", "hours": 3, "progress": 0, "urgent": False},
            {"task": "Customer interviews", "owner": "Ada", "status": "In progress", "hours": 8, "progress": 25, "urgent": True},
        ]
    )

edited = st.data_editor(
    st.session_state.tasks,
    num_rows="dynamic",
    width="stretch",
    hide_index=True,
    column_config={
        "task": st.column_config.TextColumn("Task", required=True, width="large"),
        "owner": st.column_config.SelectboxColumn("Owner", options=["Ada", "Grace", "Alan"], required=True),
        "status": st.column_config.SelectboxColumn(
            "Status", options=["Not started", "In progress", "Done"], required=True, default="Not started"
        ),
        "hours": st.column_config.NumberColumn("Hours", min_value=0, max_value=200, step=1, format="%d h"),
        "progress": st.column_config.ProgressColumn("Progress", min_value=0, max_value=100, format="%d%%"),
        "urgent": st.column_config.CheckboxColumn("Urgent?"),
    },
    key="task_editor",
)

edited = edited.fillna({"hours": 0, "progress": 0, "urgent": False})
total_hours = edited["hours"].sum()
done_hours = (edited["hours"] * edited["progress"] / 100).sum()

a, b, c = st.columns(3)
a.metric("Tasks", len(edited))
b.metric("Hours planned", f"{total_hours:.0f}")
c.metric("Overall progress", f"{(done_hours / total_hours * 100) if total_hours else 0:.0f}%")

st.subheader("Hours by owner")
st.bar_chart(edited.groupby("owner")["hours"].sum())

st.download_button(
    "Download as CSV",
    edited.to_csv(index=False).encode("utf-8"),
    file_name="tasks.csv",
    mime="text/csv",
    icon=":material/download:",
)
