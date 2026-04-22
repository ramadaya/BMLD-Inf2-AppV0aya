import streamlit as st

st.title("Kalenderblatt 📅")

st.write("Diese Seite ist eine Unterseite der Startseite.")

from datetime import datetime, timedelta
import pandas as pd

# Session-State als einfache "Datenbank"
if "events" not in st.session_state:
    st.session_state.events = []

st.title("Zykluskalender")

# Eingabe
event_name = st.text_input("Periode")
event_date = st.date_input("Datum")
follow_days = st.number_input("Ovulation", value=14)

if st.button("Speichern"):
    follow_up_date = event_date + timedelta(days=follow_days)
 
    st.session_state.events.append({
        "name": event_name,
        "date": event_date,
        "type": "Periode"
    })

    st.session_state.events.append({
        "name": f"{event_name} (Follow-Up)",
        "date": follow_up_date,
        "type": "Ovulation"
    })

# Anzeige
df = pd.DataFrame(st.session_state.events)
st.dataframe(df)