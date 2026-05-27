import streamlit as st
import pandas as pd
from datetime import date, timedelta
from streamlit_calendar import calendar
from functions.data_utils import get_data_df, get_calendar_df 
from functions.cycle_utils import get_current_phase, PHASE_INFO, calculate_cycle_phases
from functions.render import render_header

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



render_header("❤️ Boyfriend", logo_width=70)


def render_calendar(calendar_df):

    if calendar_df.empty:
        st.warning("⚠️ Bitte zuerst im Kalender die Periode speichern.")
        return

    last_row = calendar_df.iloc[-1]

    events, _ = calculate_cycle_phases(
        period_start=pd.to_datetime(last_row["Datum"]).date(),
        cycle_length=int(last_row["Zykluslänge"]),
        period_length=int(last_row["Periodendauer"]),
        PHASE_COLORS=PHASE_COLORS,
    )

    for event in events:
        event["start"] = str(event["start"])

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