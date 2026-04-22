import streamlit as st

st.title("Kalenderblatt 📅")

events = []

for e in stored_events:
    events.append({
        "title": e["name"],
        "start": str(e["date"])
    })

    follow_date = e["date"] + timedelta(days=e["follow_days"])

    events.append({
        "title": e["name"] + " (Follow-Up)",
        "start": str(follow_date),
        "color": "red"
    })