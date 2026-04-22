st.title("Kalenderblatt 📅")

from datetime import date, timedelta
import streamlit as st

st.title("Kalenderblatt 📅")

stored_events = [
    {
        "Periode": "Event A",
        "Datum": date(2026, 4, 22),
        "follow_days": 7
    }
]

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

st.write(events)