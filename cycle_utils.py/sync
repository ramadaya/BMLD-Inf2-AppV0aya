import pandas as pd
from datetime import date, timedelta
import os

FILE = "events.csv"

def get_current_phase() -> str:
    """Reads events.csv and returns the current cycle phase as a string."""
    if not os.path.exists(FILE):
        return None

    df = pd.read_csv(FILE)
    if df.empty:
        return None

    df["Datum"] = pd.to_datetime(df["Datum"]).dt.date
    last = df.iloc[-1]

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