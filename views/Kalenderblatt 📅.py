
st.title("Kalenderblatt 📅")

import streamlit as st
from datetime import date, timedelta
from streamlit_calendar import calendar
import pandas as pd
import os

st.title("Kalenderblatt 📅")

FILE = "events.csv"

# Daten laden
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    df["Datum"] = pd.to_datetime(df["Datum"]).dt.date
else:
    df = pd.DataFrame(columns=["Periode", "Datum", "follow_days"])

# Event hinzufügen
with st.form("event_form"):
    name = st.text_input("Name / Periode")
    event_date = st.date_input("Datum")
    follow_days = st.number_input("Follow-Up nach Tagen", value=7)

    submitted = st.form_submit_button("Speichern")

    if submitted:
        new_row = pd.DataFrame([{
            "Periode": name,
            "Datum": event_date,
            "follow_days": follow_days
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Gespeichert!")

# Events für Kalender vorbereiten
events = []

for _, e in df.iterrows():
    # normales Event
    events.append({
        "title": e["Periode"],
        "start": str(e["Datum"]),
        "color": "blue"
    })

    # Follow-Up
    follow_date = e["Datum"] + timedelta(days=int(e["follow_days"]))

    events.append({
        "title": e["Periode"] + " (Follow-Up)",
        "start": str(follow_date),
        "color": "red"
    })

# Kalender anzeigen
calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "de"
}

calendar(events=events, options=calendar_options)

# Tabelle anzeigen (evtl. später löschen)
st.subheader("Gespeicherte Events")
st.dataframe(df)