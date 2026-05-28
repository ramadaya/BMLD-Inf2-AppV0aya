import streamlit as st 
import pandas as pd


SYMPTOM_COLS = [
    "⚡️ Energie",
    "😣 Schmerzen",
    "🧠 Fokus",
    "🍫 Heißhunger",
    "😴 Müdigkeit",
    "😊 Stimmung",
]

def get_phase_name_for_date(selected_date):
    data_df = st.session_state["data_df"]

    if data_df.empty or "Typ" not in data_df.columns:
        return None

    calendar_df = data_df[data_df["Typ"] == "Kalender"].copy()
    calendar_df = calendar_df.dropna(
        subset=["Datum", "Zykluslänge", "Periodendauer"]
    )

    if calendar_df.empty:
        return None

    calendar_df["Datum"] = pd.to_datetime(
        calendar_df["Datum"],
        errors="coerce"
    ).dt.date

    last = calendar_df.iloc[-1]

    period_start = last["Datum"]
    cycle_length = int(last["Zykluslänge"])
    period_length = int(last["Periodendauer"])

    selected_date = pd.to_datetime(selected_date).date()
    day_of_cycle = ((selected_date - period_start).days % cycle_length) + 1
    ovulation_day = cycle_length - 14

    if day_of_cycle <= period_length:
        return "🔴 Menstruation"

    if day_of_cycle <= ovulation_day - 1:
        return "🌱 Follikelphase"

    if day_of_cycle <= ovulation_day + 2:
        return "✨ Eisprung"

    return "🌙 Lutealphase"

def get_symptoms_df():
    data_df = st.session_state["data_df"]

    if data_df.empty or "Typ" not in data_df.columns:
        return pd.DataFrame(columns=["Typ", "Datum", "Phase"] + SYMPTOM_COLS)

    return data_df[data_df["Typ"] == "Symptom"].copy()