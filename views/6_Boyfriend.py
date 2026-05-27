import streamlit as st
import pandas as pd
from datetime import date, timedelta
from streamlit_calendar import calendar
from functions.render import get_data_df, get_calendar_df 
from functions.cycle_utils import get_current_phase, PHASE_INFO

PHASE_COLORS = {
    "menstruation": "#e63946",
    "follikel": "#f4a261",
    "eisprung": "#2a9d8f",
    "luteal": "#6a4c93",
}

PHASE_TIPPS = {
    "menstruation": {
        "title": "🔴 Menstruation",
        "texts": [
            "Schokolade oder Lieblingssnacks mitbringen",
            "Wärmflasche oder Heizkissen anbieten",
            "Kuscheln oder einfach da sein",
            "Geduldig zuhören und Verständnis zeigen",
        ],
    },
    "follikel": {
        "title": "🌱 Follikelphase",
        "texts": [
            "Spaziergänge oder Dates vorschlagen",
            "Gemeinsame Pläne machen",
            "Neue Aktivitäten ausprobieren",
            "Motivation und gute Laune unterstützen",
        ],
    },
    "eisprung": {
        "title": "✨ Eisprung",
        "texts": [
            "Blumen oder kleine Aufmerksamkeiten schenken",
            "Komplimente machen",
            "Ein schönes Date planen",
            "Achtsam sein: Schwangerschaft ist möglich",
        ],
    },
    "luteal": {
        "title": "🌙 Lutealphase",
        "texts": [
            "Mehr Ruhe und Verständnis zeigen",
            "Emotionalen Support geben",
            "Geduldig bleiben",
            "Einen entspannten Filmabend vorschlagen",
        ],
    },
}


def render_header():
    col1, col2 = st.columns([1, 5])

    with col1:
        st.image("docs/logo.png", width=70)

    with col2:
        st.title("❤️ Boyfriend")


def calculate_cycle_phases(
    period_start: date,
    cycle_length: int = 28,
    period_length: int = 5,
):
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

    for i in range((next_period - luteal_start).days):
        events.append({
            "title": "🌙 Lutealphase",
            "start": str(luteal_start + timedelta(days=i)),
            "color": PHASE_COLORS["luteal"],
        })

    return events


def render_calendar(calendar_df):
    if calendar_df.empty:
        st.warning("⚠️ Bitte zuerst im Kalender die Periode speichern.")
        return

    last_row = calendar_df.iloc[-1]

    events = calculate_cycle_phases(
        period_start=last_row["Datum"],
        cycle_length=int(last_row["Zykluslänge"]),
        period_length=int(last_row["Periodendauer"]),
    )

    calendar_options = {
        "initialView": "dayGridMonth",
        "locale": "de",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek",
        },
    }

    calendar(events=events, options=calendar_options)


def render_partner_tips(phase):
    if phase is None:
        st.info(
            "Noch keine aktuelle Phase vorhanden. "
            "Bitte zuerst im Kalender deine Periode speichern."
        )
        return

    info = PHASE_INFO[phase]
    text = PHASE_TIPPS[phase]

    items = "".join(f"<li>{item}</li>" for item in text["texts"])

    st.markdown(f"## Tipps für die {text['title']}")

    st.markdown(
        f"""
        <div style="background-color:{info['color']}22;
                    border-left: 5px solid {info['color']};
                    padding: 1rem;
                    border-radius: 8px;">
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


render_header()

st.markdown(
    """
    Diese Seite hilft Partnerinnen und Partnern zu verstehen,
    wie sie in den verschiedenen Zyklusphasen unterstützen können.
    """
)
data_df = get_data_df()

calendar_df = get_calendar_df(data_df)
render_calendar(calendar_df)

phase = get_current_phase()
render_partner_tips(phase)