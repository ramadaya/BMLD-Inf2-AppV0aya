import pandas as pd
from datetime import date, timedelta
import streamlit as st 

def get_current_phase() -> str:
    """Liest Kalenderdaten aus st.session_state['data_df'] und gibt die aktuelle Zyklusphase zurück."""

    if "data_df" not in st.session_state:
        return None

    df = st.session_state["data_df"]

    if df.empty or "Typ" not in df.columns:
        return None

    calendar_df = df[df["Typ"] == "Kalender"]

    if calendar_df.empty:
        return None

    calendar_df = calendar_df.copy()
    calendar_df["Datum"] = pd.to_datetime(calendar_df["Datum"]).dt.date

    last = calendar_df.iloc[-1]

    period_start = last["Datum"]
    cycle_length = int(last["Zykluslänge"])
    period_length = int(last["Periodendauer"])

    today = date.today()
    day_of_cycle = (today - period_start).days % cycle_length + 1

    ovulation_day = cycle_length - 14

    if day_of_cycle <= period_length:
        return "menstruation"
    elif day_of_cycle <= ovulation_day - 2:
        return "follikel"
    elif day_of_cycle <= ovulation_day + 1:
        return "eisprung"
    else:
        return "luteal"

PHASE_INFO = {
    "menstruation": {
        "name": "🔴 Menstruation",
        "color": "#e63946",
        "mood": "Du brauchst Ruhe und Selbstfürsorge. Sei sanft mit dir.",
        "sports": ["Sanftes Yoga", "Spazierengehen", "Stretching"],
        "nutrition": ["Eisenreiche Lebensmittel (Spinat, Linsen)", "Dunkle Schokolade", "Ingwertee", "Warme Suppen"],
        "symptoms": ["Krämpfe möglich", "Müdigkeit", "Stimmungsschwankungen", "Kopfschmerzen möglich"]
    },
    "follikel": {
        "name": "🌱 Follikelphase",
        "color": "#f4a261",
        "mood": "Deine Energie steigt! Gute Zeit für neue Projekte.",
        "sports": ["Krafttraining", "Laufen", "HIIT", "Tanzen"],
        "nutrition": ["Leichte Salate", "Fermentierte Lebensmittel", "Beeren", "Vollkornprodukte"],
        "symptoms": ["Steigende Energie", "Bessere Stimmung", "Mehr Kreativität", "Klarerer Kopf"]
    },
    "eisprung": {
        "name": "✨ Eisprung",
        "color": "#2a9d8f",
        "mood": "Du strahlst! Höchste Energie und Kommunikationsstärke.",
        "sports": ["Intensives Training", "Gruppenclasses", "Radfahren", "Schwimmen"],
        "nutrition": ["Rohkost", "Leichte Mahlzeiten", "Zink-reiche Lebensmittel (Kürbiskerne)", "Viel Wasser"],
        "symptoms": ["Mittelschmerz möglich", "Höchste Energie", "Erhöhte Libido", "Leichter Ausfluss"]
    },
    "luteal": {
        "name": "🌙 Lutealphase",
        "color": "#6a4c93",
        "mood": "Zeit zum Runterkommen. Auf deinen Körper hören.",
        "sports": ["Pilates", "Yoga", "Leichtes Cardio", "Schwimmen"],
        "nutrition": ["Magnesium (Nüsse, Bananen)", "Komplexe Kohlenhydrate", "Vermied Koffein & Alkohol", "Dunkle Schokolade"],
        "symptoms": ["PMS möglich", "Blähungen", "Brustspannen", "Stimmungsschwankungen"]
    }
}

def calculate_cycle_phases(
    PHASE_COLORS,
    period_start: date,
    cycle_length: int = 28,
    period_length: int = 5,  
):
    """Calculate calendar events for the four cycle phases."""
    events = []

    for i in range(period_length):
        events.append({
            "title": "🔴 Menstruation",
            "start": str(period_start + timedelta(days=i)),
            "color": PHASE_COLORS["menstruation"],
        })

    ovulation_day = period_start + timedelta(days=cycle_length - 14)

    follicular_start = period_start + timedelta(days=period_length)
    follicular_end = ovulation_day - timedelta(days=1)

    for i in range((follicular_end - follicular_start).days + 1):
        events.append({
            "title": "🌱 Follikelphase",
            "start": str(follicular_start + timedelta(days=i)),
            "color": PHASE_COLORS["follikel"],
        })

    for i in range(3):
        events.append({
            "title": "🐣 Eisprung",
            "start": str(ovulation_day + timedelta(days=i)),
            "color": PHASE_COLORS["eisprung"],
        })

    luteal_start = ovulation_day + timedelta(days=3)
    next_period = period_start + timedelta(days=cycle_length)
    luteal_days = (next_period - luteal_start).days

    for i in range(luteal_days):
        events.append({
            "title": "🌙 Lutealphase",
            "start": str(luteal_start + timedelta(days=i)),
            "color": PHASE_COLORS["luteal"],
        })

    return events, next_period