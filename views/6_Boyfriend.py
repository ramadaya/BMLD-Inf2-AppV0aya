import streamlit as st
from datetime import date, timedelta
from streamlit_calendar import calendar
import pandas as pd
import os
from functions.cycle_utils import get_current_phase, PHASE_INFO

# --- Cycle phase calculation ---
def calculate_cycle_phases(period_start: date, cycle_length: int = 28, period_length: int = 5):
    """
    Returns a list of calendar events for all 4 cycle phases.
    Default: 28-day cycle, 5-day period.
    """
    events = []

    # Phase 1: Menstruation
    for i in range(period_length):
        events.append({
            "title": "🔴 Menstruation",
            "start": str(period_start + timedelta(days=i)),
            "color": "#e63946"
        })

    # Phase 2: Follicular phase (after period until ovulation)
    follicular_start = period_start + timedelta(days=period_length)
    follicular_end = period_start + timedelta(days=12)  # ~Day 6–12
    for i in range((follicular_end - follicular_start).days + 1):
        events.append({
            "title": "🌱 Follikelphase",
            "start": str(follicular_start + timedelta(days=i)),
            "color": "#f4a261"
        })

    # Phase 3: Ovulation (~Day 13–15)
    ovulation_day = period_start + timedelta(days=cycle_length - 14)  # LH surge offset
    for i in range(3):
        events.append({
            "title": "🐣 Eisprung",
            "start": str(ovulation_day + timedelta(days=i)),
            "color": "#2a9d8f"
        })

    # Phase 4: Luteal phase (after ovulation until next period)
    luteal_start = ovulation_day + timedelta(days=3)
    next_period = period_start + timedelta(days=cycle_length)
    luteal_days = (next_period - luteal_start).days
    for i in range(luteal_days):
        events.append({
            "title": "🌙 Lutealphase",
            "start": str(luteal_start + timedelta(days=i)),
            "color": "#6a4c93"
        })

    return events, next_period

# --- Load saved data ---
# --- Load saved data from shared data_df ---
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame()

df = st.session_state["data_df"]

# Nur Kalender-Einträge nehmen
if not df.empty and "Typ" in df.columns:
    df = df[df["Typ"] == "Kalender"]
else:
    df = pd.DataFrame(columns=["Typ", "Datum", "Zykluslänge", "Periodendauer"])
all_events = []
if not df.empty:
    df["Datum"] = pd.to_datetime(df["Datum"]).dt.date

# --- Build calendar events ---
if df.empty:
    st.warning("⚠️ Bitte trage deine Periode ein, um den Kalender anzuzeigen.")

else:
    all_events = []

    # Only use the last entry for the calendar
    last_row = df.iloc[-1]
    phase_events, _ = calculate_cycle_phases(
        period_start=last_row["Datum"],
        cycle_length=int(last_row["Zykluslänge"]),
        period_length=int(last_row["Periodendauer"])
    )
    all_events = phase_events

# --- Display calendar ---
calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "de",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    }
}

calendar(events=all_events, options=calendar_options)

phase = get_current_phase()

if phase is None:
    st.info("Noch keine aktuelle Phase vorhanden. Bitte zuerst im Kalender deine Periode speichern.")

else:
    info = PHASE_INFO[phase]

    PHASE_TIPPS = {
        "menstruation": {
            "title":"🔴 Menstruation",
            "texts": [
                "Schokolade oder Lieblingssnacks",
                "Wärmflasche oder Heizkissen gegen Krämpfe",
                "Kuscheln",
                "Einfach zuhören und da sein"
            ]
        },

        "follikel": {
            "title": "🌱 Follikelphase",
            "texts": [
                "Unternehmungen vorschlagen (Spaziergänge, Dates)",
                "Trips planen",
                "Neue Aktivitäten ausprobieren"
            ]
        },

        "eisprung": {
            "title": "✨ Eisprung",
            "texts": [
                "ACHTUNG Schwangerschaft möglich!!!",
                "Blumen schenken",
                "Komplimente machen",
                "Dates planen"
            ]
        },

        "luteal": {
            "title": "🌙 Lutealphase",
            "texts": [
                "Mehr Ruhe & Verständnis",
                "Emotionaler Support",
                "Geduldig sein",
                "Film schauen und zu Hause entspannen"
            ]
        }
    }

    text = PHASE_TIPPS[phase]
    items = "".join(f"<li>{item}</li>" for item in text["texts"])

    st.markdown(
        f"""
        <div style="background-color:{info['color']}22; 
                    border-left: 5px solid {info['color']}; 
                    padding: 1rem; 
                    border-radius: 8px;">
            <h3>{text['title']}</h3>
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True
    )