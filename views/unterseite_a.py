st.title("Kalenderblatt 📅")

import streamlit as st
from datetime import date, timedelta
from streamlit_calendar import calendar

st.title("Kalenderblatt 📅")

# Speicher initialisieren
if "stored_events" not in st.session_state:
    st.session_state.stored_events = []

# ➕ Event hinzufügen
with st.form("event_form"):
    name = st.text_input("Name / Periode")
    event_date = st.date_input("Datum")
    follow_days = st.number_input("Follow-Up nach Tagen", value=7)

    submitted = st.form_submit_button("Speichern")

    if submitted:
        st.session_state.stored_events.append({
            "Periode": name,
            "Datum": event_date,
            "follow_days": follow_days
        })

# 📅 Events für Kalender vorbereiten
events = []

for e in st.session_state.stored_events:
    # normales Event
    events.append({
        "title": e["Periode"],
        "start": str(e["Datum"]),
        "color": "blue"
    })

    # Follow-Up berechnen
    follow_date = e["Datum"] + timedelta(days=e["follow_days"])

    events.append({
        "title": e["Periode"] + " (Follow-Up)",
        "start": str(follow_date),
        "color": "red"
    })

# 📆 Kalender anzeigen
calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "de"
}

calendar(events=events, options=calendar_options)