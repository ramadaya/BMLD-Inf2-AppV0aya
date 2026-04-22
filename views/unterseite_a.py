from datetime import timedelta

import streamlit as st

st.title("Kalenderblatt 📅")

events = []

for e in stored_events:
    events.append({
        "title": e["Periode"],
        "start": str(e["Datum"])
    })

    follow_date = e["Datum"] + timedelta(days=e["follow_days"])

    events.append({
        "title": e["Periode"] + " (Ovulation)",
        "start": str(follow_date),
        "color": "red"
    })